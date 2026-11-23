# Spark:

Back To : [SQL Optimization](./SQL%20Optimization.md)

## Config + Concept Optimization

- Enable AQE - `spark.sql.(adaptive & adaptive.skewJoin).enabled = True`
- When skewed -> repartition(<increase number></increase>), AQE, salting (apply random key)
- Allocate appropriate memory (executor, driver)
- when reading RDBMS or zip -> repartition immediately because all the data goes to 1 partition.
- Broadcase join
- Cost based optimization : `spark.sql.cbo.enabled`
- enable off heap memory -> `spark.memory.offHeap.(enabled + size) = (true + 300mb)`
- Enough memory to -> `spark.executor.memoryOverhead=1G`
- Partitioning + clustering + Bucketing
- Cache() & persist() + unpersist()
- df.explain or df.groupBy().explain() -> see the plan

## While reading data from Kafka:

- **minOffsetsPerTrigger + maxOffsetsPerTrigger** -> to control how many records Spark pulls per topic-partition in a single micro-batch. This guarantees predictable batch processing times and prevents OOM crashes
- `startingOffsets` and `endingOffsets`: Use `"latest"` for real-time production pipelines, or `"earliest"` if you need to replay historical data from the beginning of the Kafka retention window

## Reading data from RDBMS

```SQL
# python - pyspark 
df = spark.read.format("jdbc") \
.option("url", "jdbc:postgresql://localhost:5432/mydb") \
.option("dbtable", "massive_order_table") \
.option("partitionColumn", "order_id") \  # Must be numeric, date, or timestamp
.option("lowerBound", "1") \              # Minimum value of the partition column
.option("upperBound", "10000000") \       # Maximum value of the partition column
.option("numPartitions", "20") \          # Number of concurrent DB connections/Spark tasks
.option("user", "username") \
.option("password", "password") \
.load()
```

## While Reading Zip File

- Unlike formats like Gzip or Bzip2, **standard `.zip` files are completely non-splittable in Hadoop/Spark.** Spark cannot divide a single `.zip` file across multiple executors; one executor task must read and decompress the entire file from start to finish on a single core.

### - Solution:

- **Many Small Zip Files:** If you have hundreds of smaller `.zip` files instead of one giant file, Spark _can_ parallelize them by assigning one file per task. Ensure your partition count matches or exceeds the file count using `spark.sql.files.minPartitions`.
- **Pre-Decompression Step:** For massive enterprise workflows, the best approach is to decouple decompression from your main Spark processing engine. Use a lightweight orchestration script (e.g., Airflow bash task or a simple Python script running `zipfile`) to unpack the files into an object store (S3/ADLS/GCS) as raw text or CSV before Spark starts its job.
- **Avoid Nested Zips:** Never process zip files containing thousands of small nested files inside Spark. It balloons driver metadata memory, leading to an immediate **Driver OOM (Out of Memory)** error.
- **Native Splittable Alternatives:** If you control the upstream data generation, immediately migrate away from `.zip` to **Snappy-compressed Parquet** or **Gzip-compressed text files (`.gz`)** combined with an architecture that writes multiple smaller files instead of one monolith.


# Spark Code Samples:

```py

read a JSON file with explicit schema + multi-line JSON.

explicit_schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("city", StringType(), True)
])

spark.read.schema(explicit_schema).option('multiline', "true").json('path')

```

```py

3.Given a nested JSON dataset, flatten it into a flat schema using Spark SQL functions such as explode and column dot-notation.

nested_json_data = [{
    "company": "TechCorp",
    "location": {"city": "San Francisco", "state": "CA"},
    "employees": [
        {"name": "Alice", "skills": ["Python", "Spark"]},
        {"name": "Bob", "skills": ["Java", "Scala"]}
    ]
}]


df = spark.createDataFrame(nested_json_data)

df2 = df.selectExpr("company", "location.city", "location.state", explode("employee").alias("emp"))
df2.selectExpr("company", "city", "state", "emp.name", "explode(emp.skills)")

```
