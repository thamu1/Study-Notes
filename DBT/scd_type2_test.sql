
/*

STEP 1:

profiles.yml
------------

v_dbt_team: -- project-name
  target: ci_personal
  outputs:
    ci_personal: # do not change
      type: snowflake
      account: <vm.west-europe.azure>
      role:  "<CSG>"  # Update with snowflake role name 
      # SSO auth
      user: "<abcd@company.com>"
      authenticator: externalbrowser
      database: "<DB_Name>" # Provide the database name
      warehouse: "<warehouse-name>" # Provide the warehouse name
      schema: <default-schema-name>
      threads: 1

STEP: 2

dbt_project.yml
---------------
.
.
.
models:
  asset_tag:
      psa:
        +schema: PSA
        +materialized: table

      trf:
        +schema: TRF 
        +materialized: view
.
.
.


STEP: 3 

environment_variables:
-----------------------

# Instructions:

# Encoded Private Key Must be generated from PEM file using the following command:

# STEPS:
# 1. openssl pkcs8 -topk8 -nocrypt -in "C:/Thamo/xyz-company/smartfacts-windows-amd64/cdbi_snowflake_private_key.pem" -out cdbi.p8
# 2. Replace all / -> _ and + -> - in the generated cdbi.p8 file content.
# 3. Use it in the Encoded Private Key field below.
# 4. snowflake_base64_url_encoded_private_key="<Generated Key Here>"


# DBT Configuration: ci_personal Keys
CDSID='<>'
DBT_ENV_SNOWFLAKE_USR='<User-name>'
DBT_ENV_SNOWFLAKE_PK='<Private-Key>'
DBT_ENV_SNOWFLAKE_PP='<Passpharase>'
DBT_ENV_SNOWFLAKE_ROLE='<Snowflake-Role>'
DBT_ENV_SNOWFLAKE_DB='<Db-Name>'
DBT_ENV_SNOWFLAKE_SCHEMA='<Schema-name>'
DBT_ENV_SNOWFLAKE_WH='<Warehouse-Name>'
cdbi_base64_url_encoded_private_key="C:/Thamo/<>/smartfacts/private_key.pem"


STEP: 4

export $(grep -v '^#' cdbi.env | xargs);

root="C:/Thamo/xyz-company/Data Core/Tasks/data-workspace-core-data-bi-7027-genai"

# # dbt debug --project-dir "$root/airdbt/dbt/dbt-dev" --profiles-dir "$root/airdbt/dbt/ci" --target ci_personal

# # dbt deps --project-dir "$root/airdbt/dbt/dbt-prod"


# # dbt run-operation --profiles-dir "$root/airdbt/dbt/ci" --target ci_personal --project-dir "$root/airdbt/dbt/dbt-dev" apply_table_description_and_tags --args '{db_name: DEV_CDBI_DB, schema_name: ci_run_tc, table_name: dm__FACT_GPF_USECASE_STATUS}' 

# # dbt run-operation --profiles-dir "$root/airdbt/dbt/ci" --target ci_personal --project-dir "$root/airdbt/dbt/dbt-dev" test # --log-level debug


# # dbt docs generate --profiles-dir "$root/airdbt/dbt/ci" --target ci_personal --project-dir "$root/airdbt/dbt/dbt-dev"

# # dbt docs serve --profiles-dir "$root/airdbt/dbt/ci" --target ci_personal --project-dir "$root/airdbt/dbt/dbt-dev"


# # dbt run --profiles-dir "$root/airdbt/dbt/ci" --target ci_personal --project-dir "$root/airdbt/dbt/dbt-dev" --select path:models/genai_usecase_portfolio/load

dbt run --profiles-dir "$root/airdbt/dbt/ci" --target ci_personal --project-dir "$root/airdbt/dbt/dbt-dev" --select scd_type2_test # path:models/collate/trf


*/

-- STEP: 5

-- scd_type2_test.sql

{{
    config(
        alias='scd_type2_test',
        materialized='incremental', -- This must be Incremental 
        unique_key=['hash_key', 'hash_diff'], -- Unique to identify insert & updated records
        incremental_strategy='merge'
    )
}}

with data as 
(
    select '2026-10-19' as batch_date, 'thamu' as table_name, 17 as cnt
    union all 
    select '2026-10-19' as batch_date, 'dhiva' as table_name, 18 as cnt
)

, hash_prep as (
    select
        hash(table_name) as hash_key, -- Unique Column
        hash(batch_date || table_name || cnt) as hash_diff, -- columns list to track changes
        batch_date, table_name, cnt 
    from data
)

{% if is_incremental() %}

    , current_data as 
    (
       select * from {{ this }}
       where is_current = TRUE
    )

    , insert_record as 
    (
        select 
            o.hash_key, o.hash_diff, o.batch_date, 
            o.table_name, o.cnt,
            TRUE as is_current,
            current_date() as valid_from,
            NULL as valid_to
        from hash_prep as o
        left join current_data as c
            on o.hash_key = c.hash_key
        where c.hash_key is null -- Finding New
            or o.hash_diff != c.hash_diff -- Finding the updated records
    )

    , updated_record as 
    (
        select
            c.hash_key,
            c.hash_diff,
            c.batch_date,
            c.table_name,
            c.cnt,
            FALSE as is_current,
            c.valid_from as valid_from,
            current_date() as valid_to
        from hash_prep as o
        join current_data as c
            on o.hash_key = c.hash_key
        where o.hash_diff != c.hash_diff -- Finding Updated records to mark it as old
    )

    select * from insert_record
    union all
    select * from updated_record

{% else %} -- Used for the initial ingestion/insert

    select 
        hash_key,
        hash_diff,
        batch_date,
        table_name,
        cnt,
        TRUE as is_current,
        current_date() as valid_from,
        NULL as valid_to
    from hash_prep

{% endif %}





