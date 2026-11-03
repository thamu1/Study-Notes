# Bigquery Optimization

Back To : [[SQL Optimization]]

## Partition by

- allowed only 1 column
- int range or timestamp field
- 4000 partition / table.
- `partition by   <date: purchase_date> or   range_bucket(customer_id, generate_array(0, 100, 1))   Option(partition_expiration_days = 3,   require_partition_filter = TRUE))`

## cluster by

- allowed 4 column
- High cardinality

## Storage Billing Model: **Logical & Physical**

### - Logical

- Charges for original file size - 1TB
- Best while store a lot of time-travel data.

### - Physical

- Charges for compressed - 100 GB
- Pay extra for time-travel storage ($2 - $3 more) + per GB cost is higher still overall cheaper
- `bq update --storage_billing_model=PHYSICAL <dataset - name>`
  or
  `alter schema <dataset-name>   set options(storage_billing_model="PHYSICAL")`

## Others

- Use **REGEXP_CONTAINS** or **SEARCH** instead of **like %<>%**
- Use **APPROX_COUNT_DISTINCT** instead of **count(distint)**
- avoid OVER() use GROUP BY
- JOIN:

  - Large Table First while Joining -> **BIG_TBL** join **SMALL_TBL**
  - Cross join with 1 = 1 condition
- Join on with PARTITION BY and CLUSTER BY columns
