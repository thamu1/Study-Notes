
Reference:

    . cheat sheet : https://medium.com/indiciumtech/17-dbt-commands-you-should-start-using-today-581998dbf8f0

1. need to start the spark thrift server

spark-submit \
--master 'local[*]' \
--conf spark.executor.extraJavaOptions=-Duser.timezone=Etc/UTC \
--conf spark.eventLog.enabled=false \
--conf spark.sql.warehouse.dir=~/spark/sparkwarehouse \
--class org.apache.spark.sql.hive.thriftserver.HiveThriftServer2 \
--name "Thrift JDBC/ODBC Server" \
--executor-memory 512m

2. Beeline:

 > beeline -u jdbc:hive2://localhost:10000/

 or 

 > beeline
 > !connect jdbc:hive2://localhost:10000/
 > username > tchand19
 > password > tchand19


3. source dbt_pyenv/bin/activate && cd test/spark_practice

4. create macro for DDL(create, insert, update, delete, alter etc..) operation:

    macro/factory.sql 

    {% macro create_db(db_name) %} -- 
        {% set query %}
            create database if not exists {{db_name}} -- Place your query here.
        {% endset %}

        {% if execute %}
            {% do run_query(query) %}
        {% endif %}

    {% endmacro%}

    dbt run-operation create_db --args '{db_name: shop}'
    
5. dbt external test: 

    macro/tests/unique_check.sql

    {% test unique_check(model, column_name) %}

        select product_name
            , category
            , count(1) as cnt 
        from  {{model}} -- default.dim_product_details
        group by 1, 2 having count(1) > 1

    {% endtest %} 

    -> Include in you model 

        - name: model_name (basically sql file name)
          tests:
            - <your-test-name> (unique_check)
              arguments
          columns:
            - name: <col-name>
              data_test/tests:
                - unique 
                - not_null
                - <your-test-name> (unique_check)
                  arguments


---------------------------------------------------------------------------------------------------------------------


SCD TYPE - 2:
-------------

# models/scd/dummy.sql

{{
    config(
        materialized = 'view',
        alias = 'dummy', # Dummy table execution
        pre[post]_hook = "{{ macro_call('database', 'schema', 'table') }}" -- Macro Call to execute DML 
    )
}}


select 1 as placeholder


# macros/scd_type_2/scd2.sql

{% macro macro_call(databse, schema, table) %}

    {% set query %}
        merge into dev_cdbi_db.ci_run_TC.DM__FACT_GPF_USECASE_STATUS as t
        using (
            -- Records which Needs to be Inserted
            select sf.usecaseid, sf.statusid, 'insert' as flag -- 
            from DEV_CDBI_DB.CI_RUN_TC.TRF__V_TRF_GPF_USECASES as sf
            left join dev_cdbi_db.ci_run_TC.DM__FACT_GPF_USECASE_STATUS as tf
                on sf.usecaseid = tf.usecase_id 
            where (sf.statusid != tf.status_id) or tf.usecase_id is null
        
            union all 

            -- Records which Needs to be Updated
            select sf.usecaseid, sf.statusid, 'update' as flag
            from DEV_CDBI_DB.CI_RUN_TC.TRF__V_TRF_GPF_USECASES as sf
            left join dev_cdbi_db.ci_run_TC.DM__FACT_GPF_USECASE_STATUS as tf
                on sf.usecaseid = tf.usecase_id
            where (sf.statusid != tf.status_id)
            
        ) as s 
            on t.usecase_id = s.usecaseid and s.flag = 'update'
        when matched then update 
            set t.status_id = s.statusid, t._valid_to = current_timestamp()::timestamp_ntz, t._is_active_ind = FALSE
        when not matched then insert 
            values(s.usecaseid
                , s.statusid
                , NULL
                , NULL
                , current_timestamp()::timestamp_ntz
                , current_timestamp()::timestamp_ntz
                , current_timestamp()::timestamp_ntz
                , NULL 
                , TRUE 
            )

    {% endset %}

    {% if execute %}
        {% do run_query(query) %}
    {% endif %}

{% endmacro %}



# Commands to Execute
  1. dbt run-operation create_db --args '{database: db, schema: schm, table: tbl}'
    
    exe.sh:
    -------
        export $(grep -v '^#' .env | xargs);
        
        root="C:/Thamo/Volvo/Data Core/Tasks/Collate_dbt/data-workspace-core-data-bi-7027-genai"
        
        # # Connection Check
        # dbt debug --project-dir "$root/airdbt/dbt/dbt-dev" --profiles-dir "$root/airdbt/dbt/ci" --target ci_personal
        
        # # Install dependencies Need to Set Env variable for Git token
        # dbt deps --project-dir "$root/airdbt/dbt/dbt-dev"
        
        # # See the dependency graph of the models in Web UI
        
        # dbt docs generate --profiles-dir "$root/airdbt/dbt/ci" --target ci_personal --project-dir "$root/airdbt/dbt/dbt-dev"
        
        # dbt docs serve --profiles-dir "$root/airdbt/dbt/ci" --target ci_personal --project-dir "$root/airdbt/dbt/dbt-dev"
        
        
        # # Compile the queries to check for any syntax errors or issues with the models
        # dbt compile --profiles-dir "$root/airdbt/dbt/ci" --target ci_personal --project-dir "$root/airdbt/dbt/dbt-dev" --select collate_column
        
        
        # # # Run the models to create the tables in the target database
        # dbt run --profiles-dir "$root/airdbt/dbt/ci" --target ci_personal --project-dir "$root/airdbt/dbt/dbt-dev" --select collate_table_domains
        
        
        # # Run All the models to create the tables in the target database
        # dbt run --profiles-dir "$root/airdbt/dbt/ci" --target ci_personal --project-dir "$root/airdbt/dbt/dbt-dev" --select path:models
        
        # # Run All the models under the perticular folder to create the tables in the target database 
        # dbt run --profiles-dir "$root/airdbt/dbt/ci" --target ci_personal --project-dir "$root/airdbt/dbt/dbt-dev" --select path:models/collate/load
        
        
        # dbt run --profiles-dir "$root/airdbt/dbt/ci" --target ci_personal --project-dir "$root/airdbt/dbt/dbt-dev" --select path:models/collate/psa
        
        # dbt run --profiles-dir "$root/airdbt/dbt/ci" --target ci_personal --project-dir "$root/airdbt/dbt/dbt-dev" --select STG_COLLATE_COLUMN_TAGS
        
        # dbt run --profiles-dir "$root/airdbt/dbt/ci" --target ci_personal --project-dir "$root/airdbt/dbt/dbt-dev" --select FACT_COLLATE_DATAPRODUCT_STANDARDS
        
        # dbt run --profiles-dir "$root/airdbt/dbt/ci" --target ci_personal --project-dir "$root/airdbt/dbt/dbt-dev" --select  path:models/sp_dataproduct/
        
        dbt run --profiles-dir "$root/airdbt/dbt/ci" --target ci_personal --project-dir "$root/airdbt/dbt/dbt-dev" --select FACT_GPF_USECASE_STATUS
        

---------------------------------------------------------------------------------------------------------------------


# Pipeline Log Macro:
---------------------

.macros/log_pipeline_run.sql:
-----------------------------

{% macro test() %}

  {% set args = invocation_args_dict if invocation_args_dict is defined else {} %}
  {% set pipeline_name = args.get('project_dir', '') %}

  {% set parsed_pipeline_name = pipeline_name.split('/')[4]  %}

  {% set model_name = args.get('select', args.get('models', 'n/a'))[0] %}

  {{ log("parsed Pipeline Name:::::::::::: " ~ parsed_pipeline_name, info= True) }}

  {{ log("Model Name :::::::::::: " ~ model_name, info= True) }}

  {% for result in results %}
      {{ log(
          "Model Statua =>>>> " ~ result.node.name ~
          " -> " ~ result.status,
          info=True
      ) }}
  {% endfor %}

{% endmacro %}

#}

{% macro log_pipeline_start() %}

  {% set args = invocation_args_dict if invocation_args_dict is defined else {} %}
  {% set model_name = args.get('select', ('na',))[0] %}
  {% set pipeline_name_raw = args.get('project_dir', '') %}

  {{ log("Pipeline Name Raw:::: " ~ pipeline_name_raw, info=True) }}

  {% set pipeline_name = pipeline_name_raw.split('/')[4] %}

  {% set create_schema_sql %}
    CREATE SCHEMA IF NOT EXISTS {{ target.database }}.LOAD
  {% endset %}

  {% set create_table_sql %}
  
    CREATE TABLE IF NOT EXISTS {{ target.database }}.LOAD.SMARTFACTS_PROCESS_LOG (
        BATCH_DATE DATE,
        PIPELINE_ID VARCHAR(100),
        PIPELINE_NAME VARCHAR(100),
        PIPELINE_STARTED_AT TIMESTAMP_NTZ(9),
        PIPELINE_ENDED_AT TIMESTAMP_NTZ(9),
        STATUS VARCHAR(50)
    );

  {% endset %}


  {% set insert_sql %}
    INSERT INTO {{ target.database }}.LOAD.SMARTFACTS_PROCESS_LOG (BATCH_DATE, PIPELINE_ID, PIPELINE_NAME, PIPELINE_STARTED_AT, PIPELINE_ENDED_AT, STATUS)
    SELECT CURRENT_DATE, '{{ invocation_id }}', '{{ pipeline_name }}' || '@' || '{{ model_name }}', CURRENT_TIMESTAMP(), NULL, 'in_progress'
  {% endset %}


  {% if execute %}
    {% do run_query(create_schema_sql) %}
    {% do run_query(create_table_sql) %}
    {% do run_query(insert_sql) %}
  {% endif %}

{% endmacro %}




{% macro log_pipeline_end() %}

  {% set update_sql %}
    UPDATE {{ target.database }}.LOAD.SMARTFACTS_PROCESS_LOG
    SET PIPELINE_ENDED_AT = CURRENT_TIMESTAMP(), STATUS = 'completed'
    WHERE PIPELINE_ID = '{{ invocation_id }}'
  {% endset %}

  {% if execute %}
    {% do run_query(update_sql) %}
  {% endif %}

{% endmacro %}


dbt_project.yml
---------------

...
# models in models folder will be rendered to the schema
models:
  volvo_dbt:
    +database: DB_Name
    +persist_docs:
      relation: true
      columns: true

    risk_registry:
      +tags: ["risk_registry"]
      load:
        +schema: load
        +materialized: table
      stage:
        +schema: stg
        +materialized: table
      psa:
        +schema: psa
        +materialized: table
      trf:
        +schema: trf
        +materialized: view
      dm:
        +schema: dm
        +materialized: table


# If run results are enabled then keep it. If kept then make sure `enable_logging: true` in the dbt_config of the airflow DAG definition
on-run-start:
  - "{{ log_pipeline_start() }}" # ./macros/log_pipeline_run.sql

on-run-end:
  - "{{ log_pipeline_end() }}" # ./macros/log_pipeline_run.sql
  - "{{ vcc_dbt.log_dbt_results(results) }}"


---------------------------------------------------------------------------------------------------------------------





