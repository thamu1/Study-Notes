from airflow.providers.mysql.operators import mysql 
from airflow import DAG
from airflow.operators import python_operator 
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago



args = {
    'owner': 'thamu',    
    #'start_date': airflow.utils.dates.days_ago(2),
    # 'end_date': datetime(),
    # 'depends_on_past': False,
    # 'email': ['test@example.com'],
    #'email_on_failure': False,
    #'email_on_retry': False,
    # If a task fails, retry it once after waiting
    # at least 5 minutes
    #'retries': 1,
    'retry_delay': timedelta(seconds=5),
    }


dag = DAG(
    dag_id='airflow_mysql_1',
    default_args=args,
    # schedule_interval='0 0 * * *',
    schedule_interval='@once',
    start_date=days_ago(1),
    dagrun_timeout=timedelta(minutes=60),
    description='use case of mysql operator in airflow',
)

create_database = mysql.MySqlOperator(
    task_id = 'create_database',
    # database='world',
    sql = f'create database thamu;',
    mysql_conn_id = 'airflow_mysql',
    # autocommit = True,
    dag = dag ,
)

create_table = mysql.MySqlOperator(
    task_id = 'create_table',
    database='thamu',
    sql = f'create table if not exists mysql_try(id int, name varchar(50));',
    mysql_conn_id = 'airflow_mysql',
    # autocommit = True,
    dag = dag ,
    
)

insert_data = mysql.MySqlOperator(
    task_id = 'insert_data',
    database='world',
    sql = f"insert into mysql_try(id,name) values(1,'thamu');",
    mysql_conn_id = 'airflow_mysql',
    # autocommit = True,
    dag = dag,
)


# create_sql_query = """ CREATE TABLE world.employee(empid int, empname VARCHAR(25), salary int); """

# create_table = mysql.MySqlOperator(sql=create_sql_query, task_id="CreateTable", mysql_conn_id="airflow_mysql", dag=dag)

# insert_sql_query = """ INSERT INTO world.employee(empid, empname, salary) VALUES(1,'VAMSHI',30000),(2,'chandu',50000); """

# insert_data = mysql.MySqlOperator(
#     sql=insert_sql_query, 
#     task_id="InsertData", 
#     mysql_conn_id="airflow_mysql", 
#     dag=dag)


create_database >> create_table >> insert_data
