from airflow.providers.mysql.operators.mysql import MySqlOperator
from airflow import DAG
from datetime import datetime,timedelta
from airflow.operators import python_operator

class airflow_mysql():
    def __init__(self,conn_id,dag):
        
        self.mysql_conn_id = conn_id  
        self.dag = dag
    
    def create_database(self,database):
        cre_db = MySqlOperator(
            task_id = 'create_database',
            sql = f'create database {self.database};',
            mysql_conn_id = self.mysql_conn_id,
            dag = self.dag 
        )
        return cre_db
        
        
    def create_table(self,database,table_name,table_column:tuple):
        self.database = str(database)
        self.table_name = table_name,
        self.table_column = table_column,
        cre_tab = MySqlOperator(
            task_id = 'create_table',
            database = self.database,
            sql = f'create table if not exists {self.table_name}{self.table_column};',
            mysql_conn_id = self.mysql_conn_id,
            dag = self.dag ,
        )
        return cre_tab
        
    def insert_data(self,database,table_name,column,data):
        self.database = str(database)
        self.table_name = table_name
        self.column = tuple(column)
        self.data = tuple(data)
        ins_data = MySqlOperator(
            task_id = 'insert_data',
            database=self.database,
            sql = f"insert into {self.table_name}{self.column} values({self.data});",
            mysql_conn_id = self.mysql_conn_id,
            dag = self.dag,
        )
        return ins_data
        
    def delete_table(self):
        pass
    def update_record(self):
        pass
 
    