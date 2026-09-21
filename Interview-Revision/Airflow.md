# Airflow Revision

---

## What Is Apache Airflow?

* Apache Airflow is an open-source platform for developing, scheduling, and monitoring workflows
* A workflow is written as Python code and represented as a DAG (Directed Acyclic Graph)
* A DAG contains tasks and the dependencies that control their order
* Airflow orchestrates work; it is not normally the system that performs the heavy data processing itself
* Good use cases: batch ETL/ELT, data quality checks, ML pipelines, scheduled reports, and event-driven workflows
* Airflow is a good fit when work has clear tasks, dependencies, retries, monitoring, and a start/end
* Airflow is not usually the best choice for low-latency streaming, a simple cron job, or a long-running service
* Airflow 3.x documentation currently describes the Airflow 3 public interface and Task SDK
* Airflow 3 public interface: prefer `airflow.sdk`; avoid depending on internal modules or direct metadata database access

## Airflow 3 Architecture

* Simple flow:
	* DAG bundle -> DAG processor -> metadata database -> scheduler -> executor -> worker/task
	* User/UI/API -> API server -> metadata database and task execution API
	* Waiting task -> triggerer -> scheduler -> worker when the event occurs
* Required components in Airflow 3:
	* API server: provides the web UI and REST API; tasks use the task execution API to communicate with Airflow
	* Scheduler: decides which DAG runs and task instances are ready, then submits work to the executor
	* DAG processor: parses DAG files from DAG bundles and serializes DAG definitions into the metadata database
	* DAG bundle: source location for DAG files; local files, Git, and other bundle backends can be used
	* Metadata database: stores DAGs, task states, runs, connections, variables, XCom metadata, and scheduling information
	* Executor: configured in the scheduler; decides whether tasks run locally, on workers, in containers, or in another system
* Optional components:
	* Workers: execute tasks when using a remote executor such as Celery or Kubernetes
	* Triggerer: runs asynchronous triggers for deferrable operators and frees worker slots while tasks wait
	* Plugins: extend Airflow with custom UI, operators, hooks, listeners, timetables, or triggers
	* Message broker: commonly needed by queued executors such as CeleryExecutor
* Airflow 3 architecture change: the DAG processor is a required standalone component; the scheduler should not directly execute DAG-author code
* Airflow 3 task execution: a worker starts a new subprocess for each task instance and the task process does not directly access the metadata database
* Distributed deployment:
	* DAG processor and workers need the DAG bundle
	* Scheduler and triggerer mainly use the metadata database and do not need direct DAG bundle access
	* Versioned DAG bundles can help the scheduler and workers use the same DAG version
* Basic deployment: API server, scheduler, DAG processor, and local executor on one machine
* Production deployment: external metadata database, remote executor, remote logs, secrets backend, health checks, and multiple Airflow components

## Architecture Example

* Suppose a daily pipeline loads sales data:
	* DAG author commits `sales_dag.py` to Git
	* DAG bundle makes the file available to the DAG processor
	* DAG processor parses the Python and stores the serialized DAG in the metadata database
	* Scheduler creates a DAG run and checks task dependencies
	* Executor sends ready tasks to a worker or container
	* Worker runs each task in a subprocess and reports state through the task execution API
	* API server shows the DAG graph, task states, logs, and retries in the UI

## Core Terms

* DAG: definition of the workflow; it is a reusable blueprint, not one execution
* DAG Run: one execution of a DAG for a particular schedule or manual trigger
* Task: one unit of work inside a DAG
* Task Instance: one execution of one task inside one DAG run
* Operator: a reusable task template, for example `BashOperator` or `PythonOperator`
* Sensor: a task that waits for an external condition
* TaskFlow task: a Python function turned into a task using `@task`
* Dependency: an upstream/downstream relationship between tasks
* XCom: small metadata passed between tasks; not a data lake or file store
* Connection: stored configuration/credentials for an external system
* Variable: small environment or configuration value stored by Airflow
* Param: validated input value supplied when triggering a DAG
* Pool: named group of limited slots used to protect an external resource
* Provider: separately packaged integration for systems such as Google Cloud, AWS, databases, and Slack
* Asset: a logical data product or external dataset that can create dependencies and trigger DAGs
* Trigger: asynchronous event watcher used by a deferrable operator
* Timetable: scheduling logic that determines when a DAG run is created and what data interval it represents

## Airflow 3 Public Interface

* Recommended imports for DAG authors:
	* `from airflow.sdk import DAG, task, dag, Asset, Param, TaskGroup`
	* `from airflow.sdk import get_current_context, Connection, Variable`
* Providers remain the normal source for integrations:
	* `from airflow.providers.standard.operators.bash import BashOperator`
	* `from airflow.providers.standard.operators.empty import EmptyOperator`
* Do not build new code around internal paths such as `airflow.models.*` or direct metadata ORM models
* Do not query the metadata database directly from task code in Airflow 3
* Use the Task Context, stable REST API, or the Python API client for supported access
* Airflow 3 public interfaces include `DAG`, `BaseOperator`, `BaseSensorOperator`, `@dag`, `@task`, `@asset`, `TaskGroup`, `Connection`, `Variable`, and context helpers
* Classes or methods not documented as public may change without backward compatibility

## Creating a DAG

* A DAG usually defines `dag_id`, `start_date`, `schedule`, `catchup`, tags, default arguments, and tasks
* Airflow 3 example using the recommended SDK:

	```python
	import pendulum

	from airflow.sdk import DAG, task
	from airflow.providers.standard.operators.bash import BashOperator

	with DAG(
		dag_id="daily_sales",
		start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
		schedule="@daily",
		catchup=False,
		tags=["sales", "example"],
	):
		extract = BashOperator(
			task_id="extract",
			bash_command="echo extracting sales",
		)

		@task
		def transform():
			print("transforming sales")

		load = BashOperator(
			task_id="load",
			bash_command="echo loading sales",
		)

		extract >> transform() >> load
	```
* DAGs can also be created with the `DAG(...)` constructor or the `@dag` decorator
* A function decorated with `@dag` must be called and assigned at module level so Airflow can discover the DAG
* Every task must belong to a DAG, either through a context manager, decorator, dependency, or explicit `dag=`
* A Python file can contain multiple DAGs, but keep large DAG collections split when parsing becomes slow
* DAG files are imported repeatedly by the DAG processor; module-level code must be cheap and deterministic

## DAG Parsing and Discovery

* Airflow parses DAG files to discover top-level DAG objects
* Avoid database queries, network calls, large computations, and expensive imports at module level
* Put external calls inside task functions or operator execution methods
* Use `.airflowignore` to skip helper files and directories; Airflow 3 defaults to glob-style patterns
* Keep dynamic DAG generation stable: task IDs and topology should not change randomly between parses
* A DAG object created only inside a function and never returned/called at module level may not be discovered
* Test a DAG file with `python dags/my_dag.py` to catch syntax and import errors
* Use `dag.test()` for a simulated DAG run during local development
* Use `ruff check dags/ --select AIR3` to identify Airflow 3-specific migration and style issues

## Tasks, Operators, and TaskFlow

* Operators are reusable classes that perform a type of work
* Common operators:
	* `BashOperator`: runs a shell command
	* `PythonOperator`: runs a Python callable
	* Provider operators: submit work to BigQuery, Kubernetes, Databricks, databases, cloud storage, and APIs
	* `EmptyOperator`: useful for grouping or joining dependencies without work
* TaskFlow uses Python functions as tasks:

	```python
	from airflow.sdk import task

	@task
	def extract() -> list[int]:
		return [10, 20, 30]

	@task
	def total(values: list[int]) -> int:
		return sum(values)

	total(extract())
	```
* Calling a TaskFlow function while defining the DAG creates a task; the function body runs later on a worker
* A returned value is stored as an XCom and becomes an `XComArg` for downstream dependencies
* Use `multiple_outputs=True` or return a dictionary when several small values must be passed
* Keep returned XCom values small; store large data in object storage, a database, or a warehouse and pass its URI/table/partition
* Choose an existing provider operator before writing custom task code

## Dependencies

* `upstream >> downstream` means downstream waits for upstream
* `downstream << upstream` expresses the same relationship in reverse
* Lists allow fan-out and fan-in:
	* `extract >> [clean, validate] >> load`
* `chain(a, b, c)` creates a readable linear chain
* `cross_downstream([a, b], [c, d])` creates every upstream-to-downstream combination
* A DAG must be acyclic; a dependency path cannot eventually point back to an earlier task
* Airflow schedules a task only when its dependency conditions and concurrency limits allow it

## DAG-to-DAG Dependencies

* A DAG-to-DAG dependency means one DAG starts or waits for another DAG
* First ask whether both workflows should be one DAG; one DAG is usually easier to view, schedule, retry, and debug
* Keep separate DAGs when they have different schedules, different owners, independent deployment, or a reusable upstream workflow
* Two common Airflow patterns:
	* Triggering: `TriggerDagRunOperator` starts the downstream DAG
	* Waiting: `ExternalTaskSensor` waits for a DAG or task in another DAG to finish
* Use an asset instead when the real dependency is “run after this dataset is updated,” not “run after this particular DAG run”

### Simple Example: Trigger One DAG from Another

* Scenario: `sales_extract` finishes loading raw data, then starts `sales_transform`
* The upstream DAG sends a small configuration dictionary through `conf`:

	```py
	import pendulum

	from airflow.sdk import DAG
	from airflow.providers.standard.operators.empty import EmptyOperator
	from airflow.providers.standard.operators.trigger_dagrun import TriggerDagRunOperator

	with DAG(
		dag_id="sales_extract",
		start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
		schedule="@daily",
		catchup=False,
	):
		extract = EmptyOperator(task_id="extract_sales")

		trigger_transform = TriggerDagRunOperator(
			task_id="trigger_sales_transform",
			trigger_dag_id="sales_transform",
			conf={
				"source": "mysql",
				"partition": "{{ data_interval_start | ds }}",
			},
			wait_for_completion=True,
			deferrable=True,
		)

		extract >> trigger_transform
	```
* The downstream DAG can read the configuration from `dag_run.conf` at task runtime:

	```py
	import pendulum

	from airflow.sdk import DAG, get_current_context, task

	with DAG(
		dag_id="sales_transform",
		start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
		schedule=None,
		catchup=False,
	):
		@task
		def transform_sales() -> None:
			context = get_current_context()
			dag_run = context["dag_run"]
			run_conf = dag_run.conf or {}

			source = run_conf.get("source", "unknown")
			partition = run_conf.get("partition")
			print(f"Transforming {source} partition {partition}")

		transform_sales()
	```
* What happens:
	* `sales_extract` runs `extract_sales`
	* `TriggerDagRunOperator` creates a run of the DAG whose ID is `sales_transform`
	* `conf` passes JSON-like values to the new DAG
	* `wait_for_completion=True` keeps the trigger task waiting until the target DAG finishes
	* `deferrable=True` allows the trigger task to wait using the triggerer instead of occupying a worker slot
* If the controller should only start the target and continue immediately, omit `wait_for_completion`
* `trigger_dag_id` must exactly match the target DAG's `dag_id`
* Do not pass large datasets through `conf`; pass a table name, partition, object-storage URI, or job ID

### Simple Example: Wait for Another DAG or Task

* Scenario: `daily_report` should run only after the `sales_extract` DAG's `load_sales` task succeeds

	```py
	import pendulum

	from airflow.sdk import DAG
	from airflow.providers.standard.operators.empty import EmptyOperator
	from airflow.providers.standard.sensors.external_task import ExternalTaskSensor

	with DAG(
		dag_id="daily_report",
		start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
		schedule="@daily",
		catchup=False,
	):
		wait_for_extract = ExternalTaskSensor(
			task_id="wait_for_sales_extract",
			external_dag_id="sales_extract",
			external_task_id="load_sales",
			allowed_states=["success"],
			failed_states=["failed", "skipped"],
			timeout=60 * 60,
			mode="reschedule",
		)

		build_report = EmptyOperator(task_id="build_report")

		wait_for_extract >> build_report
	```
* To wait for the whole external DAG instead of one task, omit `external_task_id`:
	* `ExternalTaskSensor(task_id="wait_for_extract", external_dag_id="sales_extract", ...)`
* `allowed_states` says which external states release the sensor
* `failed_states` says which external states make the sensor fail
* `mode="reschedule"` releases the worker slot between checks
* Use `deferrable=True` when the provider sensor supports it and a triggerer is running
* By default, the sensor tries to match the relevant logical date; make sure both DAGs use compatible schedules and data intervals
* When the upstream and downstream schedules do not line up, use the sensor's date-mapping options such as `execution_delta` or `execution_date_fn` where appropriate

### Triggering vs Waiting

* Use `TriggerDagRunOperator` when the current DAG is responsible for starting the next DAG
* Use `ExternalTaskSensor` when the current DAG can start independently but must wait for an external DAG/task result
* Triggering creates a new target DAG run; waiting observes an existing target DAG run
* `wait_for_completion=True` combines both behaviors: trigger the target, then wait for it
* Avoid circular dependencies such as DAG A waiting for DAG B while DAG B waits for DAG A
* Make the target DAG idempotent because it may be triggered manually, retried, or triggered again after a failure
* Use unique and meaningful run configuration values so the target knows which partition or business date to process

### DAG-to-DAG Tips and Traps

* A task dependency such as `task_a >> task_b` works only inside one DAG; it does not connect tasks in two different DAG files
* Do not import one DAG file into another to create a cross-DAG dependency; use an operator, sensor, asset, or REST API
* A sensor can wait forever if the target DAG is paused, missing, scheduled for a different interval, or failed without a matching `failed_states` setting
* Set `timeout` and choose a failure strategy; do not leave production sensors waiting indefinitely
* The target DAG's `schedule=None` is useful when it should run only when triggered by another DAG or an external system
* For one upstream DAG and many independent consumers, assets can be cleaner than many sensors
* For complex fan-out/fan-in orchestration, consider one DAG or an external workflow/event system rather than a large chain of trigger operators
* Use `ExternalTaskMarker` when clearing a parent task should optionally clear its dependent task in another DAG
* Official references: [DAG dependencies](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html#dag-dependencies), [TriggerDagRunOperator](https://airflow.apache.org/docs/apache-airflow-providers-standard/stable/operators/trigger_dag_run.html), and [ExternalTaskSensor](https://airflow.apache.org/docs/apache-airflow-providers-standard/stable/sensors/external_task_sensor.html)

## Task States and Retries

* Common task states: `none`, `scheduled`, `queued`, `running`, `success`, `failed`, `upstream_failed`, `skipped`, `up_for_retry`, `deferred`, `removed`, `up_for_reschedule`
* A failed task can retry when `retries` is greater than zero
* Useful retry settings: `retries`, `retry_delay`, `retry_exponential_backoff`, `max_retry_delay`, and `execution_timeout`
* Retry-safe task: repeating it produces the same intended result without duplicates or corruption
* Use upsert/merge, partition-specific writes, unique keys, and external job IDs for idempotency
* `depends_on_past=True` makes a task depend on its previous DAG run; use carefully with backfills and failures
* `wait_for_downstream=True` adds a stronger cross-run dependency and can reduce parallelism

## DAG Runs, Logical Date, and Data Interval

* A DAG run is one instance of a DAG
* A scheduled DAG run usually processes a completed data interval, not the current clock time
* For `@daily`, a run commonly processes one day and is created after that interval ends
* `logical_date` identifies the start of the data interval for scheduled runs; it is not necessarily the actual start time
* `data_interval_start` and `data_interval_end` identify the data window the task should process
* Manual runs may have a data interval that differs from the supplied logical date; do not assume they are equal
* Use data interval values for partitioned data instead of `datetime.now()`
* `catchup=False` is the normal default in Airflow 3 and avoids creating every old interval when a DAG is enabled
* `catchup=True` creates missed scheduled runs from the start date
* Backfill is a deliberate way to run historical intervals
* `max_active_runs` limits concurrent DAG runs; use it to protect downstream systems

## Scheduling

* `schedule="@daily"`: common preset
* Cron schedule: `schedule="0 2 * * *"`
* Timedelta schedule: `schedule=timedelta(hours=6)`
* One-time DAG: `schedule="@once"`
* Manually triggered DAG: `schedule=None`
* Continuous scheduling: `schedule="@continuous"` where supported by the deployment and use case
* Use timezone-aware dates, commonly `pendulum.datetime(..., tz="UTC")`
* Airflow 3 uses `schedule`, not the removed `schedule_interval` argument
* A timetable is useful when cron or a timedelta cannot express the data interval or trigger rules
* Trigger timetables describe when to trigger; data-interval timetables also describe the interval being processed
* Asset-aware and event-driven scheduling can start a DAG when upstream data assets are updated

## Trigger Rules and Branching

* Default trigger rule: `all_success`; all direct upstream tasks must succeed
* Common trigger rules:
	* `all_success`: every upstream succeeds
	* `all_done`: every upstream reaches a terminal state
	* `one_success`: at least one upstream succeeds
	* `one_failed`: at least one upstream fails
	* `none_failed`: upstream tasks succeed or are skipped
	* `none_failed_min_one_success`: no failure and at least one success; useful after branching
	* `always`: no upstream state requirement
* Branching chooses which downstream task IDs continue; non-selected branches are skipped
* Airflow 3 TaskFlow branching:

	```python
	from airflow.sdk import task

	@task.branch
	def choose_path(is_valid: bool) -> str:
		return "load" if is_valid else "notify"
	```
* A join after branching often needs `none_failed_min_one_success`, not `all_success`, because skipped branches otherwise cascade
* Setup and teardown tasks model resource creation and cleanup; teardown tasks can run even when work fails

## Dynamic Task Mapping

* Dynamic task mapping creates task instances at runtime from a list or dictionary
* Use `.expand()` when the number of items is known only during a DAG run:

	```python
	from airflow.sdk import task

	@task
	def get_files() -> list[str]:
		return ["a.csv", "b.csv", "c.csv"]

	@task
	def process_file(path: str) -> str:
		return f"processed {path}"

	process_file.expand(path=get_files())
	```
* `.partial()` sets arguments shared by every mapped task; `.expand()` supplies mapped arguments
* Mapped task instances have a `map_index`; inspect individual map indexes when debugging
* Use mapping for data-driven work, not for generating an unstable DAG topology during parsing
* Put a reasonable limit on mapped task counts; thousands of task instances can stress the scheduler and metadata database

## Sensors and Deferrable Operators

* A sensor waits until a condition is true, such as a file, API response, partition, or external DAG run
* Sensor modes:
	* `poke`: keeps a worker slot while waiting
	* `reschedule`: releases the worker between checks and runs again later
	* Deferrable: moves waiting logic to the triggerer and releases the worker slot
* Deferrable operators need at least one running triggerer
* A trigger is small asynchronous Python code that waits for an event and yields a `TriggerEvent`
* When the event arrives, the scheduler sends the task back to a worker to resume
* Do not use blocking calls such as `time.sleep()` inside an async trigger; use `await` and asynchronous operations
* Deferral does not preserve local Python variables; pass state through resume arguments, XCom, or durable storage
* Deferrable mode is useful for long waits and external jobs; it is not automatically available inside a normal `@task` function

## Assets and Event-Driven Scheduling

* An asset is a named data product or external resource identified by a URI
* An asset producer updates/emits an asset event after creating or changing data
* A downstream DAG can schedule on one or more assets instead of polling with a sensor
* Asset dependencies make data lineage and scheduling relationships visible
* Use assets when the real dependency is “run after this dataset is updated”
* Use a sensor or deferrable operator when the task must wait for an external condition that is not modeled as an asset
* Asset expressions can combine conditions with `&` and `|` depending on the scheduling design

## XCom, Variables, Params, Connections

* XCom is for small task-to-task values such as IDs, paths, counts, and status information
* Do not use XCom for dataframes, large files, model binaries, or full query results
* Variables are global configuration values; do not use them for task-to-task communication
* Params are DAG-run inputs and can be validated with JSON schema; use them for controlled manual or API inputs
* Connections store external system details and credentials; use a `conn_id` instead of hardcoding secrets
* Use a secrets backend for sensitive connections and variables
* Read Variables and Connections at task execution time, not during DAG parsing
* In Airflow 3 use `airflow.sdk` or Task Context instead of direct database model access

### Simple Example: Read XCom, Variable, and Param

* Important: the DAG file is parsed many times, but values should usually be read when the task runs
* `XCom`: task-to-task value; the first task pushes/returns it and the second task pulls it
* `Variable`: Airflow-wide configuration value; create `environment_name` in the Airflow UI or CLI before running this example
* `Param`: value supplied when triggering the DAG; the default below is used when no value is supplied

	```py
	import pendulum

	from airflow.sdk import DAG, Param, Variable, get_current_context, task
    from airflow.models.xcom_arg import XComArg

	with DAG(
		dag_id="read_airflow_values",
		start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
		schedule=None,
		catchup=False,
		params={
			"customer_id": Param(101, type="integer"),
			"run_mode": Param("full", type="string", enum=["full", "incremental"]),
		},
	):
		@task
		def create_xcom_value() -> dict:
			# Returning a small value automatically creates an XCom with key "return_value".
			return {"source": "mysql", "row_count": 250}

		@task
		def read_values() -> None:
			# Get the runtime context for this task.
			context = get_current_context()
			task_instance = context["ti"]

            xcom_pull_value = XComArg(XComArg(create_xcom_value))

			# 1. Read an XCom returned by the upstream task.
			xcom_value = task_instance.xcom_pull(
				task_ids="create_xcom_value",
				key="return_value",
			)
			source_name = xcom_value["source"]
			row_count = xcom_value["row_count"]

			# 2. Read a DAG Param supplied when the DAG is triggered.
			params = context["params"]
			customer_id = params["customer_id"]
			run_mode = params["run_mode"]

			# 3. Read an Airflow Variable at task runtime.
			environment_name = Variable.get("environment_name", default="dev")

			print(f"Source: {source_name}")
			print(f"Rows: {row_count}")
			print(f"Customer: {customer_id}")
			print(f"Mode: {run_mode}")
			print(f"Environment: {environment_name}")

		create_xcom_value() >> read_values()
	```

	```py
	from airflow.sdk import Connection, get_current_context, task

	@task
	def read_connection() -> None:
		context = get_current_context()
		connection_id = "my_mysql"
		connection = Connection.get(connection_id)

		host = connection.host
		port = connection.port
		database = connection.schema
		print(f"Connecting to {host}:{port}/{database}")
	```

* Do not print `connection.login`, `connection.password`, or secret values in task logs
* Do not write `Variable.get(...)`, `Connection.get(...)`, or database/API calls at the top level of the DAG file because the DAG processor executes that code during every parse
* For a templated operator field, an alternative is `{{ var.value.environment_name }}` or `{{ params.run_mode }}`, but use `get_current_context()` when the value is needed as a Python variable inside a task

## Jinja Templates and Context

* Operators can mark fields as templated and use Jinja expressions such as `{{ ds }}` and `{{ data_interval_start }}`
* Common context values: `dag_run`, `logical_date`, `data_interval_start`, `data_interval_end`, `task_instance`, `run_id`, `params`, `var`, and `conn`
* Template example:
	* `bash_command="echo processing {{ data_interval_start }} to {{ data_interval_end }}"`
* Do not use Jinja to build unsafe SQL or shell commands from untrusted input; validate and parameterize values
* In a TaskFlow function, use typed context arguments or `get_current_context()` when runtime context is needed

## Executors

* The executor controls where and how task instances run; executor logic runs inside the scheduler process
* `LocalExecutor`: local subprocesses, simple single-machine production, limited scaling
* `CeleryExecutor`: workers pull tasks from a central broker; useful for distributed persistent workers
* `KubernetesExecutor`: creates a pod for each task; strong isolation and per-task resources, with pod startup overhead
* Cloud batch/container executors: submit work to services such as AWS Batch or ECS through providers
* Starting in Airflow 2.10, multiple executors can be configured and selected per DAG/task; Airflow 3 removes the old statically coded hybrid executors
* Choose based on task isolation, startup latency, workload shape, cost, autoscaling, and operational skills
* Pools limit use of shared resources regardless of executor

## Operators, Hooks, and Providers

* Operator: defines a unit of work and executes it
* Hook: reusable connection/client interface to an external system
* Provider package: ships operators, hooks, sensors, triggers, transfers, and notifications for an integration
* Use provider hooks/operators rather than opening raw credentials or clients in every task
* Common provider examples: Google Cloud, Amazon, Microsoft Azure, Kubernetes, Docker, Snowflake, Slack, HTTP, MySQL, and Postgres
* Keep provider versions compatible with the Airflow version and test upgrades in staging
* Custom operator pattern: subclass the public `BaseOperator`, define constructor arguments, declare template fields, and implement `execute()`
* Do not do network calls or expensive work in a custom operator constructor; do it in `execute()`

## Parallelism and Resource Controls

* `parallelism`: total task instances that a scheduler may run across the environment
* `max_active_tasks`/task concurrency: limits active tasks for a DAG
* `max_active_runs`: limits simultaneous runs of one DAG
* Pool: limits tasks competing for a named external resource; set `pool_slots` for expensive tasks
* `priority_weight` helps choose work when capacity is limited
* Executor queues or task-level executor selection can route work to specific workers
* Worker resources may be controlled with executor-specific settings, Kubernetes resources, or pools
* More parallelism is not always faster; external APIs, databases, slots, memory, and downstream limits can become bottlenecks

## Idempotency and Data Engineering Practices

* Treat a task like a database transaction: it should leave a complete, valid result or fail without partial output
* Make tasks safe to retry and rerun
* Prefer upsert/merge over blind insert when retries can duplicate data
* Write to a specific partition based on `data_interval_start` and `data_interval_end`
* Never depend on “latest data” during a backfill if the task should process a historical interval
* Use atomic staging plus rename/merge where the target system supports it
* Pass object-storage paths, table names, and job IDs through XCom rather than large datasets
* Do not rely on local files between tasks; remote executors may run downstream tasks on another machine
* Do not use `datetime.now()` for business results; use the DAG run’s data interval

## Security

* Use RBAC/auth managers and least-privilege roles
* Store credentials in Connections backed by a secrets backend, not in DAG source code
* Use short-lived cloud credentials and service-account impersonation where possible
* On Google Cloud, prefer Workload Identity or service-account impersonation over long-lived key files
* Protect the metadata database, Fernet key, JWT signing key, API server, and log storage
* Do not print secrets, tokens, connection extras, or sensitive task input in logs
* Use authorized interfaces: `airflow.sdk`, stable REST API, Python client, and provider APIs
* Treat DAG source as executable code; restrict who can write DAG bundles and plugins
* Separate deployment manager, DAG author, and operations permissions when teams need isolation

## Logging, Monitoring, and Alerting

* Task logs should explain inputs, important decisions, external job IDs, and output locations without exposing secrets
* Store logs remotely in production so logs survive worker replacement; common destinations include GCS, S3, Elasticsearch, or cloud logging
* Monitor scheduler heartbeat, DAG processor health, API server health, worker capacity, triggerer capacity, metadata database, task failures, retries, queue time, and DAG duration
* Add failure and retry callbacks or provider notifiers for important pipelines
* Use task timeouts and deadline alerts for workflows that must finish within a time limit
* Inspect the Grid view for run history and the Graph view for dependencies
* A DAG can be marked successful based on leaf tasks; be careful with `all_done` leaf tasks that can hide upstream failures
* Use a watcher task when a teardown/cleanup task would otherwise make a failed DAG appear successful

## Testing DAGs

* DAG loader test: `python dags/example.py`
* Parse test: load the DAG and assert `dagbag.import_errors == {}`
* Structure test: assert task IDs, dependencies, schedules, retries, and trigger rules
* Unit test task functions and custom operators without needing a full DAG run
* Use `dag.test()` for a local simulated run with an Airflow metadata database
* Test templated fields with representative dates and parameters
* Test retries, timeouts, branching, mapped tasks, skipped tasks, and failure callbacks
* Use a staging environment with non-production datasets, buckets, credentials, and APIs
* Test idempotency by rerunning the same data interval

## CLI and API Essentials

* Initialize/migrate metadata database: `airflow db migrate`
* Start components in a development environment using the Airflow quick-start commands or your deployment tool
* List DAGs: `airflow dags list`
* Trigger a DAG: `airflow dags trigger dag_id`
* Test an individual task: `airflow tasks test dag_id task_id 2026-01-01`
* Test a whole DAG locally with `dag.test()` inside the DAG module; verify CLI commands against the installed Airflow 3 minor version
* List tasks: `airflow tasks list dag_id`
* Clear and rerun task instances: `airflow tasks clear dag_id`
* Backfill historical intervals with the Airflow 3 backfill command and explicit reprocessing options
* Use the stable REST API for programmatic integrations instead of scraping the UI
* Verify exact CLI flags against `airflow <command> --help` for the installed Airflow 3 minor version

## Airflow 3 Migration Notes

* Use `airflow.sdk` as the primary DAG authoring namespace
* Replace `schedule_interval` with `schedule`
* Replace old `airflow.datasets.Dataset` imports with the Airflow 3 asset interface where appropriate
* Standard-provider operators may have moved from old core import paths; use the provider documentation
* Do not rely on direct metadata database access from task code
* Do not import or use internal `TaskInstance` models as a public task API; use Task Context
* Airflow 3 separates DAG parsing from scheduling more strongly; ensure the DAG processor and workers can access the required DAG bundle
* Check provider compatibility independently from core Airflow
* Run migration tooling, back up the metadata database, test in staging, and review release notes before production upgrades

## Common Airflow Interview Questions

* DAG vs DAG Run: DAG is the workflow definition; DAG Run is one execution
* Task vs Task Instance: Task is the definition; Task Instance is one run of that task
* Scheduler vs Executor: scheduler decides what is ready; executor decides where/how to run it
* Operator vs Sensor: operator performs work; sensor waits for a condition
* XCom vs Variable: XCom is task-to-task runtime data; Variable is global configuration
* Airflow vs Spark: Airflow orchestrates; Spark processes distributed data
* `poke` vs `reschedule` vs deferrable: worker-held polling vs released worker between checks vs triggerer-based asynchronous waiting
* `execution_date` vs logical date: `execution_date` is the old name; logical date represents the scheduled data interval start
* Catchup vs backfill: catchup automatically creates missed intervals; backfill deliberately runs a requested historical range
* Why DAGs should be idempotent: retries and reruns are normal, so repeated execution must not corrupt or duplicate data
* Why avoid top-level code: every parse executes it, slowing the DAG processor and potentially causing side effects
* Why use pools: to protect databases, APIs, and other limited external resources
* Why use TaskFlow: less boilerplate, automatic XCom wiring, and dependencies inferred from function calls
* Why use dynamic task mapping: the number of task instances can be based on runtime data without generating unstable DAG files

## Airflow Tricks and Tips

* Use `pendulum` timezone-aware dates and prefer UTC for storage and scheduling
* Always set an explicit `schedule` and `catchup` choice; do not rely on defaults in interview or production examples
* Use meaningful, stable `dag_id` and `task_id` values because they identify historical state
* Never put secrets directly in DAG Python code or templates
* Never assume two tasks run on the same worker
* Never pass large data through XCom
* Use task-level logging, not `print`, for production diagnostics when possible
* Use `data_interval_start` to choose input/output partitions
* Add retries only when the task is safe to retry
* Prefer provider operators and hooks over custom API code
* Use a deferrable operator for long waits instead of holding a worker slot
* Use `none_failed_min_one_success` for many branch joins
* Use `TaskGroup` to organize a large graph, not to hide an unclear design
* Keep task work atomic and use staging tables/files for partial results
* Pin Airflow and provider versions with the official constraints approach
* Make DAG parsing fast enough that changes appear reliably in the UI

## Airflow Traps to Remember

* A DAG file is parsed repeatedly; top-level code is not task runtime code
* Calling a TaskFlow function in the DAG file creates a task; it does not run the Python function immediately
* A task return value is an XCom, not a shared Python variable
* A DAG run can start after the data interval ends; logical date is not “now”
* Manual trigger intervals may not equal the supplied logical date
* `catchup=True` can create many historical runs unexpectedly
* `all_success` after a branch can skip a join; use an appropriate trigger rule
* A sensor in `poke` mode can consume a worker slot while idle
* A deferrable task needs a running triggerer and cannot depend on local variables after deferral
* Retrying a plain `INSERT` can duplicate rows
* Local files may not be available to a downstream task on a remote executor
* Airflow Variables are not a replacement for a secrets backend
* The metadata database schema and UI HTML are not public interfaces
* `schedule_interval` and many old import paths are Airflow 2-era patterns; verify Airflow 3 migration guidance
* A successful teardown leaf can make a DAG run appear successful even when an upstream task failed
* More workers do not fix a database, API rate limit, scheduler parsing, or pool bottleneck

## Quick Revision Summary

* Airflow = workflow orchestration platform
* DAG = workflow blueprint
* DAG Run = one execution
* Task = unit of work
* Scheduler = decides what is ready
* Executor = decides where work runs
* Worker = runs task code
* DAG processor = parses DAG Python in Airflow 3
* API server = UI, REST API, and task communication boundary
* Triggerer = waits asynchronously for deferred tasks
* XCom = small task metadata
* Connection = external system credentials/configuration
* Variable = global configuration
* Asset = data dependency/event
* Pool = resource concurrency limit
* Best design = small, idempotent, observable tasks with explicit dependencies and safe retries

## Official Airflow 3+ References

* [Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/)
* [Architecture overview](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/overview.html)
* [DAGs](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html)
* [DAG runs and data intervals](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dag-run.html)
* [TaskFlow API](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/taskflow.html)
* [Executors](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/index.html)
* [Deferrable operators and triggers](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/deferring.html)
* [Timetables and scheduling](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/timetable.html)
* [Public Interface for Airflow 3.0+](https://airflow.apache.org/docs/apache-airflow/stable/public-airflow-interface.html)
* [Production deployment](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/production-deployment.html)
* [Best practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)
* [Airflow 3 upgrade guide](https://airflow.apache.org/docs/apache-airflow/stable/installation/upgrading_to_airflow3.html)
