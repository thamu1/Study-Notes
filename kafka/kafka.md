Apache Kafka: 
-------------

  - Open source,
  - Designed to handle High throughput, Low latency data streaming across distributed system.

Use cases:
-----------
  - real Time analytics
  - Log aggregation
  - Messaging system
  - Event sourcing
  - Data pipeline between Microservies

Key Concepts:
-------------
  - Producer : Sends/produce data to kafka topics
  - Consumenr: Reads/consumes data from kafka topics
  - Broker : A kafka server that `stores and serves` messages
  - Topic : A category to which msg are sent and from which they are consumed/Reads.
  - Partition : Large topic to small topics for scalability and parallel processing.
  - Offset : Partition's unique ID
  - Consumer Group : A group of consumer that share load while consuming a topic

Kafka Architecture:
-------------------

![image](https://github.com/user-attachments/assets/dd448cdc-e472-4571-89a5-0aed6ddcaf09)


Kafka workflow:
---------------
  - Producers write data to topic
  - Each topic is splt into partitions
  - Brokers store the data in partitions
  - Consumer Subscribe to the topic and read data from the partitions
  - Kafka keeps track of the offset each consumer is at.

  Producer -> write data to Topic (split into small partitions) -> store partiiton in Broker -> Consumer read data.

Difference Between Kafka and Spark streaming:
-----

  Kafka:
  --
    - Distributed event streaming platform.
    - Used for Ingest, store(data topics in broker) and forward.
    - Input from apps, sensors, logs etc -> No data processing -> Output to Apps, services.
    - Scalability : Partition topic across multiple Brokers
    - Fault tolerant : By replication
    
  
  Spark
  ---
    - Stream processing engine. It perform computation on the data.
    - Used for Processing, transforming and analyzing
    - Input from kafka, socket, file streams etc -> data processing by Spark Driver + Executors -> output to Databases, Kafka, Dashboards.
    - Scalability : Data across cluster using RDDs/Datasets.
    - Fault Tolerant : By Data lineage and checkpointing


    | Kafka                      | Spark Streaming            |
    | -------------------------- | -------------------------- |
    | Messaging & storage system | Processing system          |
    | Event source & buffer      | Event processor            |
    | Doesn't analyze data       | Analyzes data in real-time |


  Kafka with Spark:
  ---
    Kafka -> Spark Streaming (Processing) -> Database/Kafka/Dashboard



    
    




























