from datetime import datetime, timedelta
from email.policy import default
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python_operator import PythonOperator

default_args={
    'owner': 'Maximiliano_Nuñez',
    'retries':5,
    'retry_delay': timedelta(minutes=1)
}

with DAG(
    default_args=default_args,
    dag_id='dag_extraccion_api_futbol',
    description= 'Nuestro primer dag usando python Operator',
    start_date=datetime(2024,2,20),
    schedule_interval='@daily',
    catchup=False,
    ) as dag:

    task1= PostgresOperator(
        task_id='crear_tablas_redshift',
        postgres_conn_id= 'postgres_localhost',
        sql="/querys/creacion_tablas_redshift.sql"
    )
    task2 =PythonOperator(
    task_id='Extraccion y carga API',
    python_callable='/scripts/extraccion-api.py',
    op_args=["{{ ds }} {{ execution_date.hour }}"],  
    )

task1 >> task2
