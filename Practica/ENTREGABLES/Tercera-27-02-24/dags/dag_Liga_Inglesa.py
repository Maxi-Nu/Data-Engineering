from datetime import datetime, timedelta
from email.policy import default
from airflow import DAG
from airflow.providers.amazon.aws.operators.redshift import RedshiftSQLOperator
from airflow.operators.python import PythonOperator
from scripts.ExtraccionApi import api_etl


default_args={
    'owner': 'Maximiliano_Nuñez',
    'retries':5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    default_args=default_args,
    dag_id='dag_extraccion_api_futbol',
    description= 'Obtiene datos de temporada de la premier League',
    start_date=datetime(2024,2,20),
    schedule_interval='@hourly',#'@daily',
    catchup=False,
    ) as dag:
    
    task1= RedshiftSQLOperator(
    task_id='crear_tabla_estadios',
    redshift_conn_id= 'redshift_localhost',
    sql='scripts/estadios_premier_league.sql', 
    )
    task2= RedshiftSQLOperator(
    task_id='crear_tabla_partidos',
    redshift_conn_id= 'redshift_localhost',
    autocommit=True,
    sql='scripts/partidos_premier_league.sql', 
    )
    task3= RedshiftSQLOperator(
    task_id='crear_tabla_posiciones',
    redshift_conn_id= 'redshift_localhost',
    autocommit=True,
    sql='scripts/posiciones_premier_league.sql', 
    )
    task4= PythonOperator(
    task_id='Ejecutar_API_ETL',
    python_callable=api_etl,
    op_kwargs={ 'redshift_conn':'{{var.value.redshift_conn}}',
               'api_key':'{{var.value.api_key}}'
            }
    )
[task1,task2,task3]>>task4