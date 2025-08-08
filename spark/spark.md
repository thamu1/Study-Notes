
# Apache Spark Notes

## 📝 Introduction

- **Apache Spark** is an open-source unified analytics engine for large-scale data processing.
- Released in **2009**.
- Supports **Java**, **Scala**, **Python**, **R**.

---

## 🚀 Core Modules

- **Spark SQL** and **DataFrame**
- **Spark Structured Streaming**
- **Spark MLlib**
- **Spark GraphX**

---

## ⚙️ Spark Workflow

1. Submit the Spark application.
2. **Spark Context** initializes:
    - **DAG Scheduler**:
        - Unsolved query plan → Optimized logical plan → Physical plan.
    - **Task Scheduler**:
        - Splits jobs into tasks.
3. Resource negotiation.
4. Instruct available workers.
5. Executors register with Driver.
6. Driver monitors and plans future tasks.

---

## 🧭 Deployment Modes

| Mode       | Description |
|------------|-------------|
| **Cluster** | Driver and executor run on cluster machines. Best for **production**. |
| **Client**  | Driver runs on **local** machine. Best for **development**. |
| **Standalone** | Self-managed mode. Best for **testing**. Java must be installed. |

---

## 🌟 Features of Spark

- Faster than Hadoop MapReduce.
- **Transformations** and **Actions**.
- **Lazy Execution** (executes on action).
- **In-Memory Computation** (RAM).
- **Fault Tolerance** (data lineage and DAG).

---

## 🔁 Data Abstractions

### 1. RDD (Resilient Distributed Dataset)

- Fault tolerance, parallelism, distributed computing.
- Created by:
    - `sc.parallelize(collection)`
    - Reading from Hadoop.

### 2. DataFrame

- Distributed collection of data organized into rows and columns.
- Similar to a relational table.
- Immutable and in-memory.

### 3. Dataset

- Combines RDD and DataFrame features.
- Supports compile-time type safety.
- Uses **encoders** for serialization.

---

## 🏗️ Spark Architecture

### Master

- Starts SparkContext.
- Coordinates with Cluster Manager and Workers.
- Schedules tasks, manages resources, monitors tasks.

### Worker Node

- Runs executor processes.
- Executes tasks and reports to driver.
- Performs: data processing, storage, networking.

---

## 📊 DAG in Spark

- **DAG**: Directed Acyclic Graph (no loops).
- Represents transformation lineage of RDDs.
- Enables **fault tolerance** via lineage.

---

## 🔄 Apache Streaming

- Input Sources: Kafka, etc.
- Converts streaming data into micro-batches.
- Uses **round-robin** method.

### Types:

- **Reliable**: Acknowledges source, replication enabled.
- **Unreliable**: No acknowledgment to source.

---

## 🔁 Replication vs Coalesce

| Feature     | Replication | Coalesce |
|-------------|-------------|----------|
| Function    | Increase or decrease partitions | Only reduces partitions |
| Shuffle     | Full shuffle | Minimal shuffle |
| Performance | Slower       | Faster (less shuffle) |

---

## 📦 Shared Variables

### Broadcast Variables

- Cached read-only data on each node.
- Optimizes joins (small ↔ large RDDs).
- Reduces network traffic.
- Limit: ~10MB.

### Accumulators

- Used for aggregation (e.g., error count).
- Writable by executors, read-only by driver.
- Example:
  ```scala
  val acc = sc.accumulator(0)
  
---

## 🔄 Shuffling

* Redistributes data across partitions.
* Involves:

  * `groupByKey()`
  * `reduceByKey()`
  * `join()`
* Can cause network I/O and memory pressure.

---

## 🧵 YARN Integration

* **YARN** = Yet Another Resource Negotiator.
* Manages cluster resources and workloads.
* Flow:

  * App submit → Resource Manager allocates → Containers run tasks.

---

## 💾 Persistence Levels

| Level             | Description                  |
| ----------------- | ---------------------------- |
| MEMORY\_ONLY      | Store in RAM only            |
| MEMORY\_AND\_DISK | RAM, spill to disk if needed |
| MEMORY\_ONLY\_SER | Serialized, stored in memory |
| DISK\_ONLY        | Store only on disk           |
| OFF\_HEAP         | Outside JVM heap memory      |

Usage:

```scala
df.persist(StorageLevel.MEMORY_AND_DISK)
```

---

## 📐 Executor Memory Calculation

* Nodes = 10
* Cores/Node = 15
* RAM/Node = 61 GB
* Optimal concurrent tasks per executor = 5

### Calculation:

```text
Executors/Node = 15 / 5 = 3
Total Executors = 10 * 3 = 30
```

### Memory Overhead Formula:

```text
max(executor_memory * 0.1, 384MB)
```

---

## 🧬 Spark SQL

* Performs relational data processing.

* Components:

  * Data Source API
  * DataFrame API
  * Catalyst Optimizer
  * SQL Service

* Supports formats like JSON, Hive, Parquet.

* Supports JDBC/ODBC.

---

## 🗂️ Spark + Hadoop Integration

* **HDFS**: Spark reads/writes distributed storage.
* **MapReduce**: Can co-exist with Spark.
* **YARN**: Used as a resource manager.

---

## 🧪 Vectors in MLlib

### Sparse Vector

* Stores only non-zero values.
* Efficient for high-dimensions.

```scala
Vectors.sparse(5, Array(0, 4), Array(1.0, 2.0))
```

### Dense Vector

* Stores all values.

```scala
Vectors.dense(1.0, 2.0, 3.0)
```

---

## 🧼 Automatic Cleanup

* Triggered using:

```text
spark.cleaner.ttl
```

* Helps manage metadata and storage.

---

## 💡 Caching in Spark Streaming

* DStream can be cached using `cache()` or `persist()`.
* Benefits:

  * Cost-efficient
  * Time-saving
  * Supports multiple jobs

---

## 🔗 Piping with External Scripts

* Use external tools via `pipe()`.

```scala
val data = sc.makeRDD(List("hi", "hello"))
val scriptPath = "/home/path/echo.sh"
val pipedRDD = data.pipe(scriptPath)
```

**Shell Script:**

```bash
echo "Running shell"
while read LINE; do 
  echo ${LINE}
done
```

---

## ❓ Interview Questions & Answers

1. **What component processes SparkSQL code?**
   ➤ **Executor Nodes**

2. **What is on top of Spark Core?**
   ➤ **SparkSQL**

3. **Component using fast scheduling for streaming analytics?**
   ➤ **Spark Streaming**

4. **True or False: DataFrame has no RDD features?**
   ➤ **False**

5. **How much faster than Mahout?**
   ➤ **10x**

6. **How to create DataFrame?**
   ➤ **Hive tables, External DBs**

7. **Why is Spark faster than MapReduce?**
   ➤ **DAG engine, in-memory computation**

8. **What is the Spark Driver?**
   ➤ **SparkContext**

9. **Command to submit Spark job?**

   ```bash
   ./spark-submit --class 'com.interviewbit.SparkExample' --master local[4] spark_example.jar input_name output_result
   ```

10. **Import SparkContext:**

```scala
import org.apache.spark.SparkContext
```

11. **True about SparkContext?**
    ➤ Only one active per JVM

12. **For counters or sums in Spark?**
    ➤ **Accumulators**

13. **head() method in Scala?**
    ➤ Returns the first element

14. **Supported SparkSQL data types?**
    ➤ `ArrayType`, `MapType`, `StructType`, `ObjectType`

15. **Dominant supervision platform?**
    ➤ **YARN**

---

## 📏 Estimate DataFrame Memory

Use `SizeEstimator` to prevent job crashes:

```scala
import org.apache.spark.util.SizeEstimator
val size = SizeEstimator.estimate(yourDF)
println(s"DataFrame size = ${size / 1000000} MB")
```

---

---
<img width="884" height="717" alt="image" src="https://github.com/user-attachments/assets/9a40a24e-91be-4ddb-93c2-a2cc85b3b3f6" />

---



		
		
		
		
		
		
