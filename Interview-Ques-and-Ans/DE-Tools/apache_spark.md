## How Spark do parallellism

- Number Partition = Number of Parallel Task
    - Eg. 5 Executor with 5 core  each -> 25 Partition/Parallel-task.
- Shuffle Partition 
    - Holds the data after processing it
    - Each partition holds more then the size of normal

```py

Example, 

Processing 1 TB of data

number of executor from 10 to 100 
number of core per executor 5
total Partition size = 100 * 5 = 500 partition
sql.shuffle.partition = 1500

1 TB => 1 * 1024 * 1024 => 1,048,576 MB / 128 => 8192 partition required

So, 
    - Input : 8192 / 500 => 16.3 cycle
    - Processing : 1500 / 500 => 3 cycle (1500 each partition holds -> 1,048,576 MB / 1500 => ~700 MB of data)
    
    Total ~20 cycle required to complete the task.  

```


