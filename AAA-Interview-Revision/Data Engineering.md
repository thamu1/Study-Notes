# Data Engineering Revision

---

## Core Data Engineering

* ETL vs ELT - ETL transforms data before loading, while ELT loads raw data first and transforms it in the warehouse/lake.
* Batch Processing vs Stream Processing - Batch handles data in chunks at intervals, while stream processes events continuously in near real time.
* Data Pipeline - A data pipeline moves data from source systems to storage and analytics systems through a defined sequence of steps.
* Data Lake vs Data Warehouse - A data lake stores raw data at low cost in varied formats, while a warehouse stores structured, query-optimized data for analytics.
* Lakehouse - A lakehouse combines the scalability of a data lake with the reliability and performance of a warehouse.
* Schema-on-Read vs Schema-on-Write - Schema-on-read infers structure during query time, while schema-on-write defines it before writing.
* OLTP vs OLAP - OLTP supports transactional, real-time operations, while OLAP supports analytical querying across large datasets.
* Data Integration - Data integration combines data from different sources into one consistent, usable format.
* Data Engineering Life Cycle - The lifecycle includes ingestion, storage, processing, transformation, orchestration, quality checks, and serving data.
* Full Load vs Incremental Load - Full load copies all data each run, while incremental load only captures new or changed records to save time and cost.
* Data Quality, Data Validation, Data Lineage - These ensure data is accurate, trusted, and traceable from source to downstream use.
* Data Governance, Data Catalog, Metadata Management - Governance and cataloging manage data ownership, access, definitions, and discoverability.
* Idempotency, Retry, Backoff, Reprocessing - These are safeguards to make pipelines reliable and safe when jobs fail or repeat.
* Partitioning, Bucketing, Clustering - These optimize query performance and data organization by reducing the amount of data scanned.
* Reconciliation, Data Auditing, Data Completeness - Reconciliation compares source and target data to detect missing, duplicated, or mismatched records.
* Slowly Changing Dimensions (SCD Type 1, 2, 3) - SCDs manage how dimension attributes change over time while preserving historical context.
* Fact Table vs Dimension Table - Fact tables store measurable business events, while dimension tables store descriptive attributes.
* Star Schema vs Snowflake Schema - Star schema is simpler and denormalized, while snowflake schema is more normalized and structured.
* CDC (Change Data Capture) - CDC captures incremental data changes from source systems to keep downstream systems up to date.
* ACID Transactions - ACID guarantees atomicity, consistency, isolation, and durability for reliable data operations.
* Medallion Architecture - Bronze, Silver, and Gold layers organize raw, cleaned, and curated data for progressive refinement.
* Data Mesh - Data mesh decentralizes data ownership to domain teams while using shared standards and platform capabilities.

## Data Sources and Ingestion

* CSV, JSON, XML, Parquet, Avro, ORC, Delta, Iceberg, Hudi - These are common data formats used to store and exchange structured and semi-structured datasets.
* JDBC, API Extraction, Webhooks, File-based Ingestion - These are common ingestion methods for pulling data from databases, services, and files.
* Batch Ingestion vs Real-time Ingestion - Batch ingestion loads data periodically, while real-time ingestion streams fresh data continuously.
* Micro-batch Processing - Micro-batch processes data in short intervals, balancing near-real-time responsiveness with the simplicity of batch systems.
* Push vs Pull Mechanism - Push sends data to consumers, while pull lets consumers request data from producers when needed.
* Kafka, RabbitMQ, Pub/Sub, Event Hubs, Kinesis - These are messaging and event streaming platforms that move data between producers and consumers.
* Producer, Consumer, Topic, Partition, Offset, Broker - These are core Kafka concepts that enable distributed event streaming.
* Connector, Kafka Connect, Debezium - Connectors help move data in and out of systems with minimal custom code, and Debezium captures database changes.
* Source System, Staging Area, Raw Layer, Curated Layer - Data typically flows from source systems into staging, then raw, and finally curated analysis-ready layers.
* Data Extraction, Transformation, Loading - This is the traditional ETL flow for moving and preparing data for consumption.
* Streaming Ingestion, Event-driven Architecture - Streaming ingestion handles data in motion, and event-driven systems react to events asynchronously.
* Dead Letter Queue (DLQ) - DLQ stores failed messages for debugging, replay, and later recovery without blocking the main pipeline.

## Storage and Data Platforms

* Data Warehouse: Snowflake, BigQuery, Redshift, Synapse - These are cloud-native analytical platforms optimized for querying large structured datasets.
* Data Lake: S3, ADLS, GCS - These are object stores that hold large volumes of raw data at low cost.
* Object Storage vs Block Storage vs File Storage - Object storage is ideal for unstructured data, while block and file storage are better for structured workloads and direct file access.
* Distributed Storage, HDFS - Distributed storage spreads data across multiple nodes for resilience and scalability.
* Lakehouse Architecture - A lakehouse adds transactional and analytical features to data lakes so they behave more like warehouses.
* Delta Lake, Apache Iceberg, Apache Hudi - These open table formats add reliability, schema handling, and ACID transactions to data lakes.
* Parquet, Columnar Storage, Row-based Storage - Parquet is a columnar format that is efficient for analytical queries, while row-based storage is better for transactional systems.
* Compression, File Formats, File Layout - Compression and layout choices reduce storage cost and improve read performance.
* Data Tiers, Hot/Warm/Cold Storage - Storage tiers balance cost and retrieval speed based on how frequently data is accessed.
* Indexing, Materialized Views, Query Plan, Statistics - These improve warehouse performance by reducing scan volume and helping the optimizer choose efficient query paths.
* Storage Optimization and Cost Control - Efficient storage design reduces costs while preserving performance and accessibility.

## Data Processing and Transformation

* MapReduce - MapReduce splits work across clusters and processes large datasets in parallel.
* Spark Architecture - Driver, Executor, Cluster Manager, DAG Scheduler - Spark uses these components to coordinate distributed computation and optimize execution plans.
* Spark Transformations - map, filter, flatMap, reduceByKey, groupBy, join, aggregate - These define how data is transformed and combined in distributed processing.
* Spark Actions - collect, count, take, save, foreach - Actions trigger execution and return results or write outputs.
* PySpark, Spark SQL, Spark DataFrame, Dataset - These are Spark interfaces for data engineering and analytics across Python and SQL workloads.
* Apache Flink, Stream Processing, Stateful Computation - Flink is a stream processing engine that supports low-latency and stateful event processing.
* Hive, Trino, Presto - These are query engines used for distributed SQL analytics over large datasets.
* SQL Transformations - SELECT, JOIN, GROUP BY, HAVING, UNION, DISTINCT - These are core SQL patterns used to filter, combine, and summarize data.
* Window Functions - ROW_NUMBER(), RANK(), DENSE_RANK(), SUM() OVER() - Window functions compute results across rows while preserving row-level detail.
* CTE, Subquery, Common Table Expression - CTEs and subqueries make complex SQL logic cleaner and easier to read.
* NULL handling - COALESCE, IS NULL, CASE WHEN - These handle missing values and transform null logic in SQL.
* Deduplication, Merge, Upsert - These operations remove duplicates and ensure the latest data is stored correctly.
* Data Enrichment, Data Normalization, Denormalization - These add context and reshape data for reporting, modeling, and downstream consumption.
* Data Testing, Unit Tests, Integration Tests, Regression Tests - Pipeline testing validates correctness, failure handling, and downstream compatibility across changes.
* Aggregate Tables, Reporting Tables - Aggregate tables precompute metrics to improve dashboard and reporting performance.
* Repartition, Coalesce, Shuffle, Broadcast Join - These are Spark optimization techniques for data movement and join performance.

## Data Modeling and Warehousing

* Fact Table, Dimension Table, Surrogate Key - Fact tables store events and metrics, dimension tables store descriptive attributes, and surrogate keys uniquely identify records.
* Star Schema, Snowflake Schema, Galaxy Schema - These are common warehouse modeling patterns that balance simplicity and normalization.
* Primary Key, Foreign Key, Referential Integrity - These enforce relationships and consistency between tables.
* Data Mart, Semantic Layer - A data mart is a focused analytics store, and a semantic layer provides business-friendly metrics and definitions.
* Slowly Changing Dimensions (SCD) - SCDs track historical changes in dimensions such as customer or product attributes.
* Normalized vs Denormalized Models - Normalized models reduce redundancy, while denormalized models improve read performance for analytics.
* Grain of the Fact Table - Grain defines the level of detail represented by each fact row, such as one row per order or per day.
* One-to-One, One-to-Many, Many-to-Many Relationships - These describe how entities relate in relational data models.
* Business Keys, Natural Keys, Composite Keys - Keys help identify records and join data reliably across systems.
* Dimensional Modeling, Kimball, Inmon - These are widely used architectural approaches for designing data warehouses and marts.
* Data Contracts, Schema Evolution - Data contracts define agreed data structure and expectations, while schema evolution handles changes in formats over time.
* Partition Pruning, Predicate Pushdown - These optimize queries by scanning only relevant partitions and filtering data as early as possible.

## Orchestration and Pipelines

* Airflow, DAG, Task, Operator, Sensor, Trigger Rule - Airflow orchestrates jobs using DAGs, tasks, and scheduling logic.
* Cron Scheduling, Scheduled Jobs, Backfills - Cron and backfills allow periodic execution and recovery of historical pipeline runs.
* Task Dependency, Parallelism, Concurrency - These control how jobs are ordered and executed efficiently in distributed systems.
* XCom, Hooks, Connections, Variables - Airflow uses these to share data and manage external system access.
* Retry, Catchup, SLA, Alerting - These features make pipelines resilient, visible, and accountable when issues occur.
* Taskflow API, Decorators, Pipeline DAGs - These streamline workflow definition and readability in modern orchestration.
* Workflow Management, Job Scheduling - Workflow management ensures jobs run in the correct order and timing.
* Dependency Management, Triggering Logic, DAG Design - Good DAG design ensures tasks run only when prerequisites are satisfied and pipelines remain maintainable.
* Workflow Orchestration vs ETL Tools - Orchestration manages execution and dependencies, while ETL tools focus on data movement and transformation.
* Data Pipeline Monitoring, Job Health Checks - Monitoring checks if pipelines are running successfully and within expected service levels.
* CI/CD for Data Pipelines - CI/CD automates testing, deployment, and validation of pipeline code and infrastructure.

## Streaming and Real-Time Data

* Stream Processing vs Batch Processing - Stream processing handles data continuously, while batch processing handles it in grouped intervals.
* Event Time vs Processing Time vs Ingestion Time - These define when an event occurred, when it was processed, and when it entered the system.
* Kafka Topics, Partitions, Replication, Offsets, Consumer Groups - Kafka uses these concepts to scale, distribute, and track event streams.
* Exactly Once, At Least Once, At Most Once - These describe delivery guarantees for stream processing and messaging systems.
* Watermarking, Event Time Windowing - Watermarking helps handle late-arriving data by tracking event-time progress in streams.
* Tumbling Window, Hopping Window, Sliding Window, Session Window - These are common time-windowing patterns used for aggregations in streaming pipelines.
* Stateful Aggregation, Windowed Aggregation - Stateful aggregation maintains context across events, while windowed aggregation computes results over defined time intervals.
* Kafka Streams, Flink, Spark Streaming - These are technologies used to process streaming data in real time.
* Stateful Processing, Checkpointing - Stateful processing retains information across events, and checkpointing helps recover from failures.
* Latency, Throughput, Backpressure - These measure real-time system performance and the pressure caused by traffic spikes.
* Rebalancing, Consumer Lag, Partition Skew - These are operational challenges in distributed streaming systems that affect consumption and throughput.

## Big Data and Distributed Systems

* Hadoop, HDFS, YARN, MapReduce - Hadoop is a distributed data processing ecosystem built around storage, resource management, and parallel computation.
* Distributed Computing, Horizontal Scaling, Vertical Scaling - Distributed systems scale by adding more machines or increasing machine capacity.
* Fault Tolerance, Data Replication, Resource Management - Fault tolerance ensures systems continue running even if components fail.
* Cluster, Node, Worker, Master, Scheduler - These are key components of distributed computing infrastructure.
* MPP Architecture (Massively Parallel Processing) - MPP systems distribute workloads across many nodes to accelerate large analytical queries.
* Data Skew, Shuffle, Join Optimization - Data skew and shuffle can slow distributed jobs, so optimization is important for performance.
* Caching, Persistence, Serialization - These improve performance by reusing data and reducing overhead in distributed tasks.
* Parallelism, Data Locality - Parallelism spreads work across machines, and data locality improves efficiency by processing data where it is stored.
* Scalability, Availability, Consistency - These are core properties of distributed systems and influence system design.
* CAP Theorem - CAP states that a distributed system can provide at most two of consistency, availability, and partition tolerance.
* High Availability, Disaster Recovery - High availability keeps systems online, while disaster recovery restores them after major outages.

## Cloud Data Engineering

* AWS - S3, Glue, EMR, Redshift, Athena, Lambda, Kinesis - AWS offers scalable storage, transformation, analytics, and serverless streaming services.
* Azure - ADLS Gen2, Data Factory, Synapse, Databricks, Event Hubs - Azure provides managed data lake, ETL, analytics, and streaming capabilities.
* GCP - BigQuery, Cloud Storage, Pub/Sub, Dataflow, Dataproc - GCP offers fully managed analytics and streaming services for large-scale data engineering.
* IAM, RBAC, VPC, Private Endpoints, Security Groups - These control identity, access, and network isolation in cloud environments.
* Cloud Storage Tiers, Lifecycle Policies, Cost Optimization - These manage storage cost by balancing access frequency and retention strategies.
* Serverless vs Managed Services - Serverless services run without infrastructure management, while managed services simplify operations but still require configuration.
* Data Platform as a Service - A hosted data platform gives teams managed infrastructure and tools without full operational overhead.
* Infrastructure as Code (Terraform, CloudFormation) - IaC defines infrastructure declaratively so it can be reproduced and version-controlled.
* Containers, Docker, Kubernetes - Containers package applications for portability, and Kubernetes orchestrates them across clusters.
* Multi-Cloud and Hybrid Architecture - Multi-cloud and hybrid designs combine services across providers or on-prem environments for flexibility and resilience.

## Data Quality, Security and Governance

* Data Validation, Null Checks, Duplicate Detection - Data validation ensures input quality and consistency before data is used downstream.
* Data Profiling, Data Drift, Schema Drift - Profiling and drift analysis reveal changes in data patterns and structures that may break pipelines.
* Data Observability, Monitoring, Alerting - Observability helps teams detect failures, delays, and anomalies early.
* Data Lineage, Traceability, Audit Trail - Lineage shows where data came from and how it changed, supporting auditability and debugging.
* PII, Data Masking, Encryption at Rest, Encryption in Transit - These protect sensitive information during storage and transmission.
* GDPR, CCPA, Data Retention Policies - These are privacy and retention regulations that shape how data is managed.
* Access Control, Role-based Access, Data Sharing - These define who can read, modify, or share data and under what conditions.
* Data Catalog, Metadata Management - Data catalogs organize metadata so teams can discover and understand data assets.
* Monitoring SLA, Data Freshness, Completeness, Accuracy - These measure whether pipelines meet business expectations for timeliness and quality.
* Great Expectations, dbt Tests, Soda, DataHub - These are widely used tools for data testing, cataloging, and observability.
* PII Masking, Data Retention, Access Logging - These enforce privacy controls and help audit who accessed sensitive data and when.

## Tools and Technologies

* Python, SQL, PySpark, Spark SQL - These are core languages and frameworks for building and querying data pipelines.
* Pandas, NumPy - These libraries are widely used for data manipulation and numerical analytics in Python.
* Airflow, dbt, Spark, Kafka, Flink - These tools support orchestration, transformation, processing, and streaming workloads.
* Git, GitHub, GitLab, Bitbucket - Version control systems help teams collaborate on code and pipeline changes.
* Docker, Kubernetes - Containers and orchestration simplify deployment, scaling, and environment consistency.
* Terraform, CI/CD, Jenkins, GitHub Actions - These automate infrastructure provisioning and deployment workflows.
* Bash, Shell Scripting - Shell scripts help automate tasks, testing, and operational processes.
* Jupyter Notebook, VS Code - These are common tools for exploration, development, and validation.
* REST APIs, Authentication, OAuth, API Keys - APIs enable programmatic access to data and services while enforcing security.
* JDBC, ODBC - These database connectivity standards let applications interact with relational data stores.

## Interview Terms and Concepts

* Latency - Latency is the delay between data generation and data availability for use.
* Throughput - Throughput is the amount of data processed or transferred over time.
* Scalability - Scalability is the ability to handle increased workload by adding resources or partitioning work.
* Reliability - Reliability is the probability that a system performs correctly and consistently over time.
* Fault Tolerance - Fault tolerance is the ability to continue operating despite partial failures.
* Durability - Durability means data is preserved even after failures or restarts.
* Availability - Availability is the proportion of time a system remains accessible and operational.
* Consistency - Consistency ensures data and state match expected rules across systems or reads.
* Data Freshness - Data freshness measures how quickly data reflects current business reality.
* Query Performance - Query performance measures how fast a system can process and return analytical requests.
* Micro-batch - Micro-batch is a small periodic batch process used to reduce the latency of near-real-time data pipelines.
* Data Completeness - Completeness indicates whether all required data is present and no critical pieces are missing.
* Data Accuracy - Accuracy reflects whether data correctly represents the real-world truth it intends to model.
* Incremental Load - Incremental load updates only changed or new records instead of reloading all data.
* Full Refresh - A full refresh reloads the complete dataset, usually for a complete rebuild or reprocessing.
* Reprocessing - Reprocessing repeats a pipeline or transformation to correct bad data or recover from failure.
* Backfill - Backfill loads historical data into a system to fill gaps or rebuild datasets.
* Data Drift - Data drift is a change in the distribution or meaning of incoming data over time.
* Pipeline SLA - SLA defines the expected performance and availability commitments for data pipelines.
* Observability - Observability is the ability to monitor, diagnose, and understand system behavior.
* Cost Optimization - Cost optimization reduces infrastructure and processing spend while maintaining functionality.
* Idempotency - Idempotency ensures repeated execution of a task produces the same result without duplicate side effects.
* Partitioning - Partitioning splits data into smaller chunks to improve parallel processing and query speed.
* Deduplication - Deduplication removes repeated records so data quality and storage efficiency improve.
* Checkpointing - Checkpointing saves progress in stream processing so jobs can resume after failures.
* Schema Registry - A schema registry stores and validates data schemas for streaming and integration systems.
* Data Contract - A data contract defines the expected structure, semantics, and quality standards for data producers and consumers.
* Hot Path vs Cold Path - Hot path handles real-time critical workloads, while cold path handles slower background or archival processing.

## Important Data Engineering Questions to Revise

* What is the difference between ETL and ELT? - ETL transforms before load, while ELT loads raw data first and transforms in the warehouse or lake.
* What are the differences between a data lake and a data warehouse? - A lake stores raw and varied data cheaply, while a warehouse is optimized for structured analytics and reporting.
* What is the difference between full load and incremental load? - Full load copies all source records each time, while incremental load captures only records that changed since the last run.
* What is a medallion architecture? - Medallion architecture organizes data into Bronze, Silver, and Gold layers for raw, trusted, and business-ready data.
* How do you optimize a warehouse query? - Use partition pruning, appropriate indexes or materialized views, proper file formats, and statistics to reduce scan volume and improve performance.
* How do you handle late-arriving data in a streaming pipeline? - Use event-time processing, watermarking, and reprocessing or window updates to account for late events.
* Explain Kafka architecture and consumer groups. - Kafka partitions messages across brokers and consumer groups allow parallel consumption without duplication across group members.
* What is the difference between batch and stream processing? - Batch processes data in intervals, while stream processes events continuously with lower latency.
* How do you ensure idempotent writes in a pipeline? - Use unique keys, deduplication logic, and upsert patterns to avoid duplicate side effects during retries.
* What is a Slowly Changing Dimension and when is it used? - It tracks historical changes in dimension values such as customer status or product category over time.
* What is a fact table and what is a dimension table? - A fact table stores transactions or metrics, while a dimension table stores descriptive attributes used for filtering and grouping.
* How do you optimize Spark jobs? - Reduce shuffles, use efficient joins, repartition appropriately, cache where needed, and optimize file formats.
* What is data lineage and why is it important? - Data lineage shows where data came from and how it changed, which is essential for debugging, auditability, and trust.
* How do you monitor pipeline health and quality? - Use metrics, alerts, freshness checks, row counts, null checks, and SLA monitoring to detect issues early.
* What is schema evolution and why does it matter? - Schema evolution handles format changes without breaking downstream jobs or consumers.
* What is CDC and when would you use it? - CDC captures incremental changes from source systems when you need near-real-time data synchronization or replication.
* What are partitioning and bucketing in data engineering? - Partitioning splits data by column values, and bucketing groups rows for efficient query access and joins.
* How do you handle duplicate records in ingestion? - Use deduplication keys, record hashes, idempotent writes, and validation rules to remove or prevent duplicates.
* How do you design a scalable data pipeline? - Use modular design, distributed systems, retries, monitoring, partitioning, and decoupled components to handle growing data volume.

---

