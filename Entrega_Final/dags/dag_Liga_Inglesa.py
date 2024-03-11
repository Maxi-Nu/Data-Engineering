from datetime import datetime, timedelta
from email.policy import default
from airflow import DAG
from airflow.providers.amazon.aws.operators.redshift import RedshiftSQLOperator
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from scripts.ExtraccionApi import api_etl
from airflow.models import Variable

try:
   mail=Variable.get('mail_alert')
except:
    mail=' '
    
default_args={
    'owner': 'Maximiliano_Nuñez',
    'retries':3,
    'retry_delay': timedelta(minutes=2),
    'email_on_failure': True,
    'email': mail
}

with DAG(
    default_args=default_args,
    dag_id='dag_extraccion_api_futbol',
    description= 'Obtiene datos de temporada de la premier League',
    start_date=datetime(2024,2,20),
    schedule_interval='@hourly',#'@daily',
    catchup=False,
    max_active_runs=1
    ) as dag:
    
    task1= RedshiftSQLOperator(
    task_id='crear_tabla_estadios',
    redshift_conn_id= 'redshift_localhost',
    sql='scripts/estadios_premier_league.sql', 
    )
    task2= RedshiftSQLOperator(
    task_id='crear_tabla_partidos',
    redshift_conn_id= 'redshift_localhost',
    sql='scripts/partidos_premier_league.sql', 
    )
    task3= RedshiftSQLOperator(
    task_id='crear_tabla_posiciones',
    redshift_conn_id= 'redshift_localhost',
    sql='scripts/posiciones_premier_league.sql', 
    )
    task4= PythonOperator(
    task_id='Ejecutar_API_ETL',
    python_callable=api_etl,
    op_kwargs={ 'redshift_conn':'{{var.value.redshift_conn}}',
               'api_key':'{{var.value.api_key}}'
            }
    )
    task5=EmailOperator(
        task_id='Envio_mail',
        to='{{var.value.mail_alert}}',
        subject='Airflow extraccion API',
        html_content= "{{ ti.xcom_pull(task_ids='Ejecutar_API_ETL')}}"
    )
[task1,task2,task3]>>task4>>task5