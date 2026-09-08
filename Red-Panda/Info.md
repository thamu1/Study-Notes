
Redpanda and Redpanda Connect Study Guide
==========================================

This guide covers a local Redpanda cluster running with Docker Compose, the
`rpk` command-line tool, and Redpanda Connect pipelines.

Contents:
---------

- [Redpanda overview](#redpanda-overview)
- [Tips and tricks](#tips-and-tricks)
- [Architecture and how it works](#redpanda-architecture-and-how-it-works)
- [Docker Compose setup](#docker-compose-setup)
- [Redpanda Connect commands](#redpanda-connect-commands)
- [rpk commands](#run-rpk-commands)
- [Learning workflow](#learning-workflow)
- [Core streaming concepts](#core-streaming-concepts)
- [Troubleshooting](#configuration-troubleshooting)

How to use this guide:
-----------------------

1. Start the local cluster with `docker compose up -d`.
2. Run the quick checks in the tips section.
3. Follow the learning workflow to create a topic, produce records, and consume them.
4. Use the Connect sections to generate and validate pipeline configurations.

Redpanda overview:
-------------------

Redpanda is a Kafka-compatible event-streaming platform. Applications publish
events to topics, and other applications consume those events. Redpanda stores
the events reliably and allows multiple consumers to process them independently.
It provides Kafka-compatible APIs while being distributed as a single Redpanda
service.

Example: an order service publishes an `order-created` event to the
`orders` topic. A billing service and a notification service can consume that
topic independently and react to the same event.

```text
Order service -> orders topic -> Billing service
                              -> Notification service
```

In this project, Redpanda listens on `localhost:19092` from the host, while
other containers on the Compose network connect to `redpanda-0:9092`. The
Redpanda Console is available at [http://localhost:8080](http://localhost:8080).

Tips and tricks:
----------------

| Tip | Why it helps | Example |
| --- | --- | --- |
| Use the correct broker address | Host applications use the published port; containers use the Compose service name. | `localhost:19092` from the host, `redpanda-0:9092` from another container |
| Check the cluster before debugging clients | It quickly separates broker problems from application problems. | `docker compose exec redpanda-0 rpk cluster health` |
| Give topics meaningful names | Topic names describe the event stream and make operations easier. | `orders`, `payments`, `user-events` |
| Use keys for related events | Records with the same key are routed to the same partition, preserving their order. | Use `customer_id` or `order_id` as the key |
| Choose partitions for parallelism | More partitions allow more consumers in a group to work concurrently. | Create a topic with `--partitions 3` |
| Do not expect ordering across partitions | Ordering is guaranteed only inside one partition. | Do not rely on global ordering in a multi-partition topic |
| Use separate consumer groups for separate services | Each group receives its own view of the topic. | `billing-group` and `notification-group` can both consume `orders` |
| Inspect lag when consumers fall behind | Lag shows the distance between produced records and committed offsets. | `docker compose exec redpanda-0 rpk group describe <group>` |
| Validate Connect configs before running them | Linting catches YAML and component-field errors early. | `MSYS_NO_PATHCONV=1 docker run --rm -v "$(pwd -W):/work" docker.redpanda.com/redpandadata/connect:latest lint /work/config.yaml` |
| Use `--help` as a version-aware reference | CLI options can change between Redpanda releases. | `docker compose exec redpanda-0 rpk topic create --help` |
| Use `MSYS_NO_PATHCONV=1` in Git Bash | It prevents Git Bash from rewriting container paths such as `/work/config.yaml`. | `MSYS_NO_PATHCONV=1 docker run ...` |
| Keep data while stopping services | `down` stops and removes containers but keeps the named volume. | `docker compose down` |
| Reset data deliberately | `down -v` deletes the Redpanda volume and all local topics/messages. | `docker compose down -v` |
| Make consumers idempotent | At-least-once delivery can retry a message after a restart. | Ignore duplicate event IDs or enforce uniqueness in the target database |
| Use resources for repeated Connect components | Named resources avoid copying large processor configurations. | `processor_resources` with `resource: enrich-order` |

Quick checks:
-------------

```bash
# See whether the services are running
docker compose ps

# Check broker metadata
docker compose exec redpanda-0 rpk cluster info

# List topics
docker compose exec redpanda-0 rpk topic list

# Follow Redpanda logs
docker compose logs -f redpanda-0
```


Redpanda architecture and how it works:
----------------------------------------

Redpanda is made up of brokers. A broker accepts client requests, stores event
records, and serves records to consumers. A production cluster normally has
multiple brokers; this project runs one broker for local learning.

| Component | Responsibility | In this project |
| --- | --- | --- |
| Producer | Publishes records to a topic. | `rpk topic produce`, Benthos, or an application |
| Kafka API | Accepts Kafka-compatible producer and consumer requests. | `localhost:19092` from the host; `redpanda-0:9092` inside Compose |
| Broker | Stores records and serves reads and writes. | The `redpanda-0` service |
| Topic | Logical stream of related records. | For example, `orders` |
| Partition | Ordered, append-only log within a topic. | Topics can have one or more partitions |
| Replica | Copy of a partition on another broker for fault tolerance. | One broker means no redundancy here |
| Consumer | Reads records from a topic. | `rpk topic consume` or an application |
| Consumer group | Shares partitions across multiple consumers and tracks offsets. | Managed with `rpk group` |
| Redpanda Console | Web UI for inspecting and managing the cluster. | `http://localhost:8080` |

Message flow:
------------

1. A producer connects to a Kafka API listener and sends a record to a topic.
2. Redpanda chooses a partition. A record with a key is usually routed by its
  key, while records without a key can be distributed across partitions.
3. The partition leader appends the record to its log. Records in a partition
  keep their order and receive an offset.
4. Redpanda acknowledges the producer according to the configured delivery
  and acknowledgement settings.
5. Consumers fetch records from the partition using their offsets. A consumer
  can read the same record again by seeking to an earlier offset.
6. A consumer group commits offsets so it can resume from its previous position.

Example flow:
------------

```text
Producer
  |
  |  order-created event
  v
orders topic
  |
  +--> partition 0 --> billing-consumer
  |
  +--> partition 1 --> notification-consumer
```

Topics are split into partitions for parallelism. Within one consumer group,
each partition is assigned to only one active consumer at a time. Different
consumer groups can independently read the same topic, which is why billing
and notifications can process the same `order-created` event separately.

Storage and reliability:
-------------------------

Redpanda persists records in partition logs on disk. In a multi-broker cluster,
partitions can have replicas. The leader handles normal reads and writes while
followers replicate the log; if a broker fails, a replica can become the new
leader. The Raft consensus protocol coordinates cluster metadata and replicated
state.

This local Compose setup has one broker and replication factor `1`. It is useful
for learning, but it does not provide high availability: if `redpanda-0` stops,
there is no second broker to take over.



Docker Compose setup:
---------------------

The Compose file starts one Redpanda broker and Redpanda Console. The broker
uses port `19092` for host access and port `9092` for other Compose services.

```yaml

networks:
  redpanda_network:
    name: local_redpanda_network
    driver: bridge
volumes:
  redpanda-0: null
services:
  redpanda-0:
    image: docker.redpanda.com/redpandadata/redpanda:latest
    command:
      - redpanda
      - start
      - --kafka-addr internal://0.0.0.0:9092,external://0.0.0.0:19092
      - --advertise-kafka-addr internal://redpanda-0:9092,external://localhost:19092
    ports:
      - 19092:19092
    networks:
      - redpanda_network

  console:
    image: docker.redpanda.com/redpandadata/console:latest
    entrypoint: /app/console
    ports:
      - 8080:8080
    environment:
      - KAFKA_BROKERS=redpanda-0:9092
    networks:
      - redpanda_network
    depends_on:
      - redpanda-0

```


Run Docker:
------------

```bash
docker compose up -d
```

Open the Console at [http://localhost:8080/overview](http://localhost:8080/overview).



To run the Test Config file:

Run the Redpanda Connect configuration from Git Bash:

```bash
MSYS_NO_PATHCONV=1 docker run --rm \
  -v "$(pwd -W)/config.yaml:/benthos.yaml" \
  docker.redpanda.com/redpandadata/connect:latest \
  run /benthos.yaml
```


Redpanda Connect commands:
---------------------------

Redpanda Connect is the stream-processing tool that reads a YAML pipeline and
executes its inputs, processors, and outputs. The commands in this table run
the Connect binary from the Docker image, not the Redpanda broker container.

| Command | What it is used for | Example |
| --- | --- | --- |
| `create` | Generate a new configuration from an input/processor/output expression. | `docker run --rm docker.redpanda.com/redpandadata/connect:latest create generate/bloblang/stdout > generated-config.yaml` |
| `list` | List available inputs, processors, outputs, and other components. | `docker run --rm docker.redpanda.com/redpandadata/connect:latest list` |
| `lint` | Check configuration syntax and report errors without running the pipeline. | `MSYS_NO_PATHCONV=1 docker run --rm -v "$(pwd -W):/work" docker.redpanda.com/redpandadata/connect:latest lint /work/config.yaml` |
| `echo` | Print the normalized configuration after it has been parsed. | `MSYS_NO_PATHCONV=1 docker run --rm -v "$(pwd -W):/work" docker.redpanda.com/redpandadata/connect:latest echo /work/config.yaml` |
| `dry-run` | Parse the config and test plugin connections without processing messages normally. | `MSYS_NO_PATHCONV=1 docker run --rm -v "$(pwd -W):/work" docker.redpanda.com/redpandadata/connect:latest dry-run /work/config.yaml` |
| `run` | Start a pipeline using a configuration file. | `MSYS_NO_PATHCONV=1 docker run --rm -v "$(pwd -W):/work" docker.redpanda.com/redpandadata/connect:latest run /work/config.yaml` |
| `test` | Execute unit tests declared for Connect configurations or templates. | `docker run --rm docker.redpanda.com/redpandadata/connect:latest test --help` |
| `template` | Create, inspect, or lint custom Connect templates. | `docker run --rm docker.redpanda.com/redpandadata/connect:latest template --help` |
| `blobl` | Execute a Bloblang mapping against JSON or other input from standard input. | `printf '{"name":"Ada"}\n' \\| docker run --rm -i docker.redpanda.com/redpandadata/connect:latest blobl 'root.greeting = "Hello " + this.name'` |

Generate a small version of a pipeline containing the same components as this
project:

```bash
docker run --rm \
  docker.redpanda.com/redpandadata/connect:latest \
  create --small generate/bloblang,sql_raw/stdout > generated-config.yaml
```

The `create` expression uses this format:

```text
input/processors/output
```

For example, `stdin/bloblang,log/stdout` creates a pipeline with a `stdin`
input, two processors, and a `stdout` output. Use `list` to discover valid
component names.

Reusable processor resources:
--------------------------------

For a reusable processor, define a labeled resource and reference it from the
pipeline:

```yaml
processor_resources:
  - label: enrich-order
    mapping: |
      root = this
      root.processed = true
      root.processed_at = now()

pipeline:
  processors:
    - resource: enrich-order
```

The resource can be used more than once without copying its configuration:

```yaml
pipeline:
  processors:
    - resource: enrich-order
    - resource: enrich-order
```

Resources can also be stored in another file, such as
`processor-resources.yaml`:

```yaml
processor_resources:
  - label: enrich-order
    mapping: |
      root = this
      root.processed = true
```

Import that file when running the main configuration:

```bash
MSYS_NO_PATHCONV=1 docker run --rm \
  -v "$(pwd -W):/work" \
  docker.redpanda.com/redpandadata/connect:latest \
  run -r /work/processor-resources.yaml /work/config.yaml
```

Custom templates:
------------------

Connect also supports custom component templates. This feature is experimental
and may change between releases. A template can define fields and use a
Bloblang mapping to generate a processor, input, output, or other component.

Example `templates/add-source.yaml`:

```yaml
name: add_source
type: processor

fields:
  - name: source
    type: string
    default: orders

mapping: |
  root.mapping = "root = this; root.source = \\"" + this.source + "\\""
```

Import custom templates when running a config:

```bash
MSYS_NO_PATHCONV=1 docker run --rm \
  -v "$(pwd -W):/work" \
  docker.redpanda.com/redpandadata/connect:latest \
  run -t "/work/templates/*.yaml" /work/config.yaml
```

Validate a custom template:

```bash
MSYS_NO_PATHCONV=1 docker run --rm \
  -v "$(pwd -W):/work" \
  docker.redpanda.com/redpandadata/connect:latest \
  template lint /work/templates/add-source.yaml
```

The `-r` option imports resource files, while `-t` imports custom template
files. These are different mechanisms: resources reuse an already configured
component, while templates define a configurable component schema.

Using the Connect plugin through `rpk`:
---------------------------------------

On Linux or WSL, `rpk` can install and manage the Redpanda Connect plugin:

```bash
rpk connect install
rpk connect --version
rpk connect create generate/bloblang/stdout > generated-config.yaml
rpk connect lint config.yaml
rpk connect run config.yaml
rpk connect upgrade
rpk connect uninstall
```

The Docker commands above are recommended for this Windows project because they
run the exact Connect version from the container. The `rpk connect` plugin is a
separate binary from the Redpanda broker's `rpk` commands.


Run `rpk` commands:
-------------------

All commands below run `rpk` inside the Redpanda broker container. Start the
cluster first with `docker compose up -d`.

The general pattern is:

`docker compose exec redpanda-0 rpk <command>`

Basic command discovery:
------------------------

| Command | What it is used for | Example |
| --- | --- | --- |
| `rpk --help` | List the top-level command groups and global flags. | `docker compose exec redpanda-0 rpk --help` |
| `rpk version` | Show the installed Redpanda and `rpk` versions. | `docker compose exec redpanda-0 rpk version` |
| `rpk topic --help` | Show all topic commands. | `docker compose exec redpanda-0 rpk topic --help` |
| `rpk topic create --help` | Show the flags and syntax for creating topics. | `docker compose exec redpanda-0 rpk topic create --help` |
| `rpk --print-tree` | Print the complete command tree as JSON. | `docker compose exec redpanda-0 rpk --print-tree` |

Cluster information and administration:
----------------------------------------

| Command | What it is used for | Example |
| --- | --- | --- |
| `cluster info` | Display the cluster ID and broker metadata. | `docker compose exec redpanda-0 rpk cluster info` |
| `cluster health` | Check the health of the Redpanda cluster. | `docker compose exec redpanda-0 rpk cluster health` |
| `cluster brokers` | Manage broker decommissioning and recommissioning. | `docker compose exec redpanda-0 rpk cluster brokers --help` |
| `cluster partitions list` | List partitions and their broker assignments. | `docker compose exec redpanda-0 rpk cluster partitions list` |
| `cluster config` | Read or change cluster configuration properties. | `docker compose exec redpanda-0 rpk cluster config --help` |
| `cluster logdirs` | Inspect broker log directories. | `docker compose exec redpanda-0 rpk cluster logdirs --help` |
| `cluster maintenance` | Put brokers into or take them out of maintenance mode. | `docker compose exec redpanda-0 rpk cluster maintenance --help` |
| `cluster upgrade` | Manage or inspect a Redpanda version upgrade. | `docker compose exec redpanda-0 rpk cluster upgrade --help` |

Topics:
-------

| Command | What it is used for | Example |
| --- | --- | --- |
| `topic list` | List topics in the cluster. | `docker compose exec redpanda-0 rpk topic list` |
| `topic create` | Create one or more topics. | `docker compose exec redpanda-0 rpk topic create my-topic --partitions 3 --replicas 1` |
| `topic describe` | Show partitions, replicas, leaders, and topic configuration. | `docker compose exec redpanda-0 rpk topic describe my-topic` |
| `topic alter-config` | Add, change, or remove topic configuration values. | `docker compose exec redpanda-0 rpk topic alter-config my-topic --help` |
| `topic add-partitions` | Increase the number of partitions in a topic. | `docker compose exec redpanda-0 rpk topic add-partitions my-topic --num 3` |
| `topic analyze` | Analyze topic partition distribution and performance-related details. | `docker compose exec redpanda-0 rpk topic analyze my-topic` |
| `topic describe-storage` | Inspect the storage status of a topic. | `docker compose exec redpanda-0 rpk topic describe-storage my-topic` |
| `topic trim-prefix` | Remove records from the beginning of a topic. | `docker compose exec redpanda-0 rpk topic trim-prefix my-topic --help` |
| `topic delete` | Delete a topic and all of its records. Use carefully. | `docker compose exec redpanda-0 rpk topic delete my-topic` |
| `topic produce` | Interactively write records to a topic. | `docker compose exec redpanda-0 rpk topic produce my-topic` |
| `topic consume` | Interactively read records from a topic. | `docker compose exec redpanda-0 rpk topic consume my-topic` |

Consumer groups:
----------------

| Command | What it is used for | Example |
| --- | --- | --- |
| `group list` | List consumer groups. | `docker compose exec redpanda-0 rpk group list` |
| `group describe` | Show group members, offsets, and consumer lag. | `docker compose exec redpanda-0 rpk group describe my-consumer-group` |
| `group seek` | Move a consumer group's offsets forward or backward. Stop consumers first. | `docker compose exec redpanda-0 rpk group seek my-consumer-group --help` |
| `group offset-delete` | Delete committed offsets for a consumer group. | `docker compose exec redpanda-0 rpk group offset-delete my-consumer-group --help` |
| `group delete` | Delete a consumer group. | `docker compose exec redpanda-0 rpk group delete my-consumer-group` |

Schema Registry:
----------------

| Command | What it is used for | Example |
| --- | --- | --- |
| `registry subject` | List or delete schema subjects. | `docker compose exec redpanda-0 rpk registry subject list` |
| `registry schema` | Register, retrieve, inspect, or delete schemas. | `docker compose exec redpanda-0 rpk registry schema --help` |
| `registry compatibility-level` | View or change schema compatibility rules. | `docker compose exec redpanda-0 rpk registry compatibility-level --help` |
| `registry mode` | View or change Schema Registry mode. | `docker compose exec redpanda-0 rpk registry mode --help` |
| `registry context` | Manage Schema Registry contexts. | `docker compose exec redpanda-0 rpk registry context --help` |

Security and access control:
---------------------------

| Command | What it is used for | Example |
| --- | --- | --- |
| `security user` | Create and manage SASL users. | `docker compose exec redpanda-0 rpk security user --help` |
| `security acl` | Create, list, and delete Kafka ACLs. | `docker compose exec redpanda-0 rpk security acl --help` |
| `security role` | Manage Redpanda roles. | `docker compose exec redpanda-0 rpk security role --help` |
| `security secret` | Manage secrets for Redpanda Cloud clusters. | `docker compose exec redpanda-0 rpk security secret --help` |

Local process and diagnostics:
-----------------------------

| Command | What it is used for | Example |
| --- | --- | --- |
| `redpanda check` | Check whether the local system meets Redpanda requirements. | `docker compose exec redpanda-0 rpk redpanda check` |
| `check` | Run production-readiness checks for a deployment. | `docker compose exec redpanda-0 rpk check` |
| `debug` | Collect or inspect diagnostic information. | `docker compose exec redpanda-0 rpk debug --help` |
| `iotune` | Measure filesystem performance and generate IO settings. | `docker compose exec redpanda-0 rpk iotune --help` |
| `redpanda start` / `stop` | Start or stop a locally managed Redpanda process. | `docker compose exec redpanda-0 rpk redpanda --help` |

Other command groups:
---------------------

| Command group | What it is used for | Example |
| --- | --- | --- |
| `cloud` | Interact with Redpanda Cloud. | `docker compose exec redpanda-0 rpk cloud --help` |
| `connect` | Install, upgrade, or uninstall the Redpanda Connect plugin. | `docker compose exec redpanda-0 rpk connect --help` |
| `container` | Manage local Redpanda container clusters. | `docker compose exec redpanda-0 rpk container --help` |
| `generate` | Generate configuration templates for related services. | `docker compose exec redpanda-0 rpk generate --help` |
| `k8s` | Interact with Redpanda clusters running on Kubernetes. | `docker compose exec redpanda-0 rpk k8s --help` |
| `plugin` | List, install, update, and remove `rpk` plugins. | `docker compose exec redpanda-0 rpk plugin --help` |
| `profile` | Manage `rpk` connection profiles. | `docker compose exec redpanda-0 rpk profile --help` |
| `shadow` | Manage Redpanda Shadow Links. | `docker compose exec redpanda-0 rpk shadow --help` |
| `sql` | Interact with a Redpanda SQL cluster. | `docker compose exec redpanda-0 rpk sql --help` |
| `transform` | Develop and manage Redpanda data transforms. | `docker compose exec redpanda-0 rpk transform --help` |

Learning workflow:
-------------------

Follow this sequence to practice the complete producer-to-consumer flow.

```bash
# 1. Start Redpanda and Console
docker compose up -d

# 2. Check the broker
docker compose exec redpanda-0 rpk cluster info

# 3. Create a topic
docker compose exec redpanda-0 rpk topic create orders --partitions 2 --replicas 1

# 4. Produce JSON records from Git Bash
printf '{"order_id":"A100","status":"created"}\n' | \
  docker compose exec -T redpanda-0 rpk topic produce orders

# 5. Consume the records in another terminal
docker compose exec redpanda-0 rpk topic consume orders

# 6. Inspect the topic
docker compose exec redpanda-0 rpk topic describe orders
```

Stop the services but keep the Redpanda data volume:

```bash
docker compose down
```

Remove the services and their stored data when resetting the exercise:

```bash
docker compose down -v
```

Core streaming concepts:
-------------------------

| Concept | Explanation | What to observe |
| --- | --- | --- |
| Record | One event stored in a topic. It normally contains a value and may have a key, headers, and timestamp. | Produce JSON messages to `orders`. |
| Key | Determines partition placement and helps preserve ordering for related records. | Use the same key for related events. |
| Partition | An ordered log. Ordering is guaranteed within one partition, not across the whole topic. | Create two partitions and inspect their assignments. |
| Offset | The position of a record inside a partition. Offsets are not global topic IDs. | Inspect consumer progress and group offsets. |
| Consumer group | A set of consumers sharing work. A partition is assigned to one active group member at a time. | Compare `group list` and `group describe`. |
| Lag | The distance between the newest record and a consumer group's committed offset. | Run `rpk group describe <group>`. |
| Retention | The policy controlling how long or how much data Redpanda keeps. | Inspect topic configuration with `topic describe`. |
| Replication | Copies partitions to other brokers for fault tolerance. | This project has one broker and replication factor `1`, so it has no redundancy. |
| Tombstone | A record with a key and a null value, commonly used to represent deletion in compacted topics. | Review `cleanup.policy` before using compaction. |

Ordering example:
------------------

If events for customer `C001` must remain ordered, publish them with the same
key. Redpanda routes records with the same key to the same partition, where
their order is maintained:

```text
key=C001: order-created -> payment-authorized -> order-shipped
             partition 1, in this order
```

Different keys can be routed to different partitions and processed in parallel.
There is no ordering guarantee between records in different partitions.

Consumer groups and offsets:
-----------------------------

Consumers do not delete a record after reading it. A consumer group stores its
progress as committed offsets, so another group can read the same records
independently. This also allows a group to replay records by moving its offsets
backward with `rpk group seek`.

```bash
docker compose exec redpanda-0 rpk group list
docker compose exec redpanda-0 rpk group describe my-consumer-group
docker compose exec redpanda-0 rpk group seek my-consumer-group --help
```

Delivery and error handling:
-----------------------------

At-least-once processing can deliver a record more than once when a consumer
restarts after processing but before committing its offset. Consumers should
therefore be safe to retry, often by using an event ID or database uniqueness
constraint for idempotency. Exactly-once behavior requires coordinated client
and broker configuration; it should not be assumed from a basic setup.

For Redpanda Connect, failed messages can be logged, retried, caught, filtered,
or sent to a dead-letter output. A simple retry and fallback pattern is:

```yaml
pipeline:
  processors:
    - try:
        - http:
            url: https://example.com/orders
            verb: POST
        - mapping: |
            root = deleted()
      catch:
        - log:
            level: ERROR
            message: 'Order processing failed: ${! error() }'
```

Configuration interpolation:
-----------------------------

Keep environment-specific values outside the YAML file by using defaults:

```yaml
input:
  kafka:
    addresses:
      - ${KAFKA_BROKER:localhost:19092}
    topics:
      - ${KAFKA_TOPIC:orders}
    consumer_group: ${KAFKA_GROUP:orders-local}
```

Bloblang basics:
---------------

Bloblang is the mapping language used by Redpanda Connect processors. `this`
refers to the input message and `root` refers to the output message.

```bloblang
root = this
root.order_id = this.order_id.string()
root.total = this.price.number() * this.quantity.number()
root.processed_at = now()
```

Test a mapping without a running pipeline:

```bash
printf '{"order_id":"A100","price":12.5,"quantity":2}\n' | \
  docker run --rm -i docker.redpanda.com/redpandadata/connect:latest \
  blobl 'root = this; root.total = this.price * this.quantity'
```

Configuration troubleshooting:
-------------------------------

| Problem | Check |
| --- | --- |
| Container cannot find `/benthos.yaml` in Git Bash | Use `MSYS_NO_PATHCONV=1` and mount a Windows-form host path from `$(pwd -W)`. |
| Connect starts but exits immediately | A finite input such as `generate` with `count: 1` has completed normally. |
| Connect reports an unknown field | Run `lint` and compare the field with `list` or the component documentation. |
| A topic command cannot connect | Check `docker compose ps`, then run `docker compose exec redpanda-0 rpk cluster info`. |
| A host application cannot connect | Use `localhost:19092`; use `redpanda-0:9092` only from a container on `redpanda_network`. |
| A consumer sees no messages | Check the topic name, consumer-group offsets, and whether another consumer group is being used. |
| Data disappeared after a reset | `docker compose down -v` deletes the named volume and its Redpanda data. |

Useful validation commands:
----------------------------

```bash
# Validate the Compose file
docker compose config -q

# Check Connect YAML before running it
docker run --rm -v "${PWD}:/work" \
  docker.redpanda.com/redpandadata/connect:latest \
  lint /work/config.yaml

# Inspect the parsed Connect configuration
docker run --rm -v "${PWD}:/work" \
  docker.redpanda.com/redpandadata/connect:latest \
  echo /work/config.yaml

# View service logs
docker compose logs -f redpanda-0
```

