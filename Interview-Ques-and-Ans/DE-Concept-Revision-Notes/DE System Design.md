
# 6 Step Framework

## 1. Requirement Gathering
- Who is the Consumer
- V's of Problem 
    - Volume - Size
    - Velocity - Frequency of data (Streaming, Batch)
    - Varity - Structured, Semi-Structured, Unstructured
    - Veracity - [SLA](./DE%20Concepts.md#SLA--Service-Level-Agreement-)
    - Value - Raw to Business ready data.

- Types:

    - Functional
        - Who is the end user 
        - What do they actually Need : Agg, Raw, historicla snapshot
        - How are they going to access : From sql, BI tools, Rest API etc..

    - Non-Functional
        - How the system should behave
        - Latency SLA, Volume, Availability, Data Retention

## 2. Pipeline Design
- Tool selection : Airflow, Oozie etc..
- Batch or Streaming Pipeline

## 3. Data Modelling
- Source
- Transformation Layer (Medallion Architecture)
- Star / Snowflake Schema : Fact, Dim, Sub-Dim
- CDC : SCD Types

## 4. Storage & File Format
- Storage Layer selection and its optimization Technique (Partition, Bucketing, Clustering etc.)
- File selection (CSV, Json, Parquet, Avro, ORC, Iceberg, Delta Lake etc..)

## 5. Data Quality & Observability
- DQ dimensions
- Data Contract : SLA
- Pipeline Observability
- Output : Healthy and correct

## 6. Scalability, Backfill & Dataops
- Can system handle 10x load
- Handling Failure Gracefully
- Reconciliation : Reprocess n days of data
- Idempotency
- Schema Evalution and Drift






## [Click Stream To BI](./Click%20Stream%20To%20BI.md)