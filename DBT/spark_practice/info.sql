
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






