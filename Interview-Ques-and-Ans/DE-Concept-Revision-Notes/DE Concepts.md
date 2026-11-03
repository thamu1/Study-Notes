# DE Concepts:

## Partitioning vs Clustering

### Partitioning

- Physically divide distinct segments based on specific column value.
- eg: Date Vice data
- Split table by Rows
- Best for Filter records (partition pruning)
- Low cardinality Column

### Clustering:

- Physically arrange the data in a order
- Best for filtering, join, ordering, grouping.
- High cardinality column with many distinct values in a column

```sql
-- Bigquery
create or replace table <table-name>
(col datatype, )
partition by <time-series-column or int range column>
cluster by <any type limited to 4 column>
```

- refer more on the following : [[Bigquery Optimization]]

## Indexing:

- Similar to Clustering It either sort phycally or maintain index table seperately.
- It will create a lookup pointer to map
- Types: cluster Index, Non cluster Index

### Cluster Index:

- A clustered index physically reorders the data rows in the table based on the index key
- `create index <index-name> on <table>(column)`

### Non Cluster Index:

- A non-clustered index leaves the table rows alone and builds a completely separate lookup structure (like a pointer map) to find the data
- Like, index at the back of a textbook
- `create noncluster index <index-name> on <table>(column)`

## Star vs Snowflake Schema

### Fact Table

- Foreign Keys + Measures/Metrics (e.g., `Product_ID`, `Store_ID`, `Date_ID` + `Quantity_Sold`, `Revenue`)
- Loaded after the Dim tables

| Star Schema                                | Snowflake Schema                     |
| ------------------------------------------ | ------------------------------------ |
| DeNormalized with Fact and Dimension Table | Normalized with Fact + Dim + Sub Dim |
| Faster because require few join            | Slower because require more join     |

### Dim Table

- Contains Detailed information of particular thing (e.g, Students information)

### Factless fact Table

- With no numerical Measure but with all the foreign key information
