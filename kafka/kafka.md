Apache Kafka: 
-------------

  - Open source, Messaging System responsible for Transferring data from one service to another service.
  - Designed to handle High throughput, Low latency data streaming across distributed system.
  - Published and Subscriber Architecture.

Use cases:
-----------
  - real Time analytics
  - Log aggregation
  - Messaging system
  - Event sourcing
  - Data pipeline between Microservies

<img width="593" alt="image" src="https://github.com/user-attachments/assets/ee95ff8b-c129-46d9-a8b6-84734ab45827" />


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
---------------------------------------------

  Kafka:
  ------
    - Distributed event streaming platform.
    - Used for Ingest, store(data topics in broker) and forward.
    - Input from apps, sensors, logs etc -> No data processing -> Output to Apps, services.
    - Scalability : Partition topic across multiple Brokers
    - Fault tolerant : By replication
    
  
  Spark:
  ------
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
  -----------------
    Kafka -> Spark Streaming (Processing) -> Database/Kafka/Dashboard

Kafka Events:
-------------
  - Piece of data that represents Specific action in a System.
  - Characterstics:
    - Type : Events Immutable & can include any type of data.
        Eg: Placing an order not reversible, But can cancel by another Event Trigger.
    - Size : Events are small in Size. Produce and consume asynchronously.
    - Ordered : Event partitions are strictly Ordered based on their offset(unique ID).
    - Retained : Events are Retained for a configurable period of time.

Event Payload vs Event Metadata:
--------------------------------

<img width="1782" alt="Screenshot 2025-05-02 at 5 57 32 PM" src="https://github.com/user-attachments/assets/704e6528-aa88-4a1e-a643-f54dba7fa0e5" />

 - Event Payload:
   - Actual content of the message - The data that being transmitted.
   - JSON (Common for readability)
   - Avro, Protobuf or Thrift (Schema enforcement and compactness)
   - Plain Text or Binary data.

 - Event Metadata:
   - It's data about data. Attached automatically by kafka and useful for consumer.
     
     - Kafka specific Metadata:
       - Topic : The name of the kafka topic
       - Partition : The partition number within the topic
       - Offset : Unique ID within the Partition
       - Timestamp : When the message was produced or logged.
       - Key : A value used to determine partitioning and message grouping.
       - Headers : Optional key-value pairs
         
     - User-Defined metadata: (Custom metadata)
       - Correlation ID / Trace ID (Distributed tracing)
       - Event Type or version
       - Schema version
       - Produver application name or ID


  <img width="713" alt="Event payload and Event metadata" src="https://github.com/user-attachments/assets/be836943-b03e-4747-b6c0-016a109b99de" />

Kafka API:
----------
  - Producer API : sends msg to kafka
  - Consumer API : reads msg from kafka
  - Stream API : Read, Transform/change the Topic/Msg
  - Connect API : Used to connect with External System.

Kafka Cluster:
---------------

  - Group of Broker/server working together.
  - It store and manage streams of data(topic) in a distributed.
  - It has multiple brokers(server) for fault tolerance and scalability.
  - Brokers(servers) commnicate with each other to ensure data consistency and availability.

Kafka Architecture:
-------------------

  - Kafka cluster can be deployed in On-Premises or in the cloud.
  - Kafka manager tool used to manage and monitor cluster health.
  - Kafka uses `Zookeeper` for managing cluster. Client can discover brokers by Zookeeper.
  - Kafka Broker(Server) use disk storage for persistent msg storage.
  - topics are divided into partitions spread across brokers for parellel processing.
  - Clients(producer and consumers) connect to any borker in the cluster.
  - Cluster can be expanded by adding more brokers(server) or Partitions.

Topic:
------
  - Think of a Kafka Topic as a Virtual Mailbox or folder where messages(like mails) are stored and organized.

  Eg: Kafka (Whole Library) -> Topic (Book category)
  
  - Distributed:
    - Kafka Topic `Distributed across multiple brokers` in a kafka cluster, ensuring scalability and Fault tolerance.
      
  - Partitioned:
    - Topic can be `partitioned into multiple partitions`, allowing parallel processing and efficient data storage.

  - Ordered:
    - Messages within partition are strictly ordered by their offset(Unique ID), ensuring message order within a partition.
   
  - Persistent:
    - Messages in kafka topic are stored on disk, allowing them to be retained even after consumer have processed them.
    - Based on Confiuration.
    - Different type of Msg file (JSON, Avro etc)
   
Replica:
---------
  - Kafka replica are copies of data stored across multiple servers/Brokers in the Kafka cluster.
  - Enable: Fault tolerance
  - Leader Replica Model : Each partition in kafka has one leader replica and one or more follower replica.
  - Leader Handles writes : Leader handle all write request for partition and replicate data to followers.
  - Follwer Sync data : Follower replicas sync data with the leader to stay-up-to-date.


Schema:
--------
  - Structure of your data. Specifies the field, their data types and any constrints of the data.
  - MetaData is used for `Serialization and DeSerialization`
  - The Schema information will be stored in the Schema registry.
  - While sending the msg(Topic) the Schema-information-UniqueId will also send along with msg.
  - Consumer access the Schema information from Schema Registry using UniqueId.

  ##Pros##:
    - Compactness : 

<img width="1597" alt="image" src="https://github.com/user-attachments/assets/65cb183e-5ad7-46f8-a0fb-619a1ad3657c" />



  
  
  
  
  



  





    
    




























