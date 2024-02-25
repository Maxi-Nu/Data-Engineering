from datetime import datetime, timedelta
from email.policy import default
from airflow import DAG
from airflow.providers.amazon.aws.operators.redshift import RedshiftSQLOperator
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

    task1= RedshiftSQLOperator(
        task_id='crear_tablas_redshift',
        redshift_conn_id= 'redshift_localhost',
        autocommit=True,
        sql='/scripts/creacion_tablas_redshift.sql' 
    )
    '''
    task2 =PythonOperator(
    task_id='Extraccion y carga API',
    python_callable=lambda: subprocess.Popen(["/scripts/extraccion-api.py"]),
    )'''
task1 #>> task2
