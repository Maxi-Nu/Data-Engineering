from datetime import datetime, timedelta
from email.policy import default
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python_operator import PythonOperator

default_args={
    'owner': 'Maximiliano_Nuñez',
    'retries':15,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    default_args=default_args,
    dag_id='dag_extraccion_api_futbol',
    description= 'Obtiene datos de temporada de la premier League',
    start_date=datetime(2024,2,20),
    schedule_interval='@once',  #'@hourly',
    catchup=False,
    ) as dag:

    task1= PostgresOperator(
        task_id='crear_tablas_redshift',
        postgres_conn_id= 'postgres_localhost',
        sql="/querys/creacion_tablas_redshift.sql"
    )
    '''
    task2 =PythonOperator(
    task_id='Extraccion y carga API',
    python_callable=lambda: subprocess.Popen(["/scripts/extraccion-api.py"]),
    )'''

task1 #>> task2
