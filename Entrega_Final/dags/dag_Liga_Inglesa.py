from datetime import datetime, timedelta
from email.policy import default
from airflow import DAG
from airflow.providers.amazon.aws.operators.redshift import RedshiftSQLOperator
from airflow.operators.python import PythonOperator
from scripts.ExtraccionApi import api_etl


default_args={
    'owner': 'Maximiliano_Nuñez',
    'retries':15,
    'retry_delay': timedelta(minutes=1)
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
    sql="""CREATE TABLE IF NOT EXISTS mxxn13_coderhouse.estadios_premier_league (
                            id_estadio INT,
                            nombre_estadio VARCHAR,
                            ciudad VARCHAR,
                            id_equipo INT,
                            PRIMARY KEY (id_estadio)
            )
            """, 
    )
    task2= RedshiftSQLOperator(
    task_id='crear_tabla_partidos',
    redshift_conn_id= 'redshift_localhost',
    autocommit=True,
    sql="""CREATE TABLE IF NOT EXISTS mxxn13_coderhouse.partidos_premier_league
                (
                    id_partido INTEGER NOT NULL  ENCODE az64
                    ,referi VARCHAR(256)   ENCODE lzo
                    ,timezone VARCHAR(256)   ENCODE lzo
                    ,fecha VARCHAR(256)   ENCODE lzo
                    ,status_par VARCHAR(256)   ENCODE lzo
                    ,id_eq_local INTEGER   ENCODE az64
                    ,eq_local_win BOOLEAN   ENCODE RAW
                    ,eq_local_goles INTEGER   ENCODE az64
                    ,id_eq_visitante INTEGER   ENCODE az64
                    ,eq_visitante_win BOOLEAN   ENCODE RAW
                    ,eq_visitante_goles INTEGER   ENCODE az64
                    ,resultado_final_local INTEGER   ENCODE az64
                    ,resultado_final_visitante INTEGER   ENCODE az64
                    ,resultado_extratime_local INTEGER   ENCODE az64
                    ,resultado_extratime_visitante INTEGER   ENCODE az64
                    ,penales_local INTEGER   ENCODE az64
                    ,penales_visitante INTEGER   ENCODE az64
                    ,PRIMARY KEY (id_partido)
                )
                """, 
    )
    task3= RedshiftSQLOperator(
    task_id='crear_tabla_posiciones',
    redshift_conn_id= 'redshift_localhost',
    autocommit=True,
    sql="""CREATE TABLE IF NOT EXISTS mxxn13_coderhouse.posiciones_premier_league
                (
                    id_eq INTEGER NOT NULL  ENCODE az64
                    ,name_eq VARCHAR(256) NOT NULL  ENCODE lzo
                    ,logo_eq VARCHAR(256)   ENCODE lzo
                    ,puesto INTEGER   ENCODE az64
                    ,puntos INTEGER   ENCODE az64
                    ,part_jugados INTEGER   ENCODE az64
                    ,part_ganados INTEGER   ENCODE az64
                    ,part_empatados INTEGER   ENCODE az64
                    ,part_perdidos INTEGER   ENCODE az64
                    ,goles_favor INTEGER   ENCODE az64
                    ,goles_contra INTEGER   ENCODE az64
                    ,fecha_actualizacion VARCHAR(256)   ENCODE lzo
                    ,fecha_ingesta VARCHAR(256)   ENCODE lzo
                    ,PRIMARY KEY (id_eq, name_eq)
                )
                """, 
    )
    task4= PythonOperator(
    task_id='Ejecutar_API_ETL',
    python_callable=api_etl,
    op_kwargs={ 'redshift_conn':'{{var.value.redshift_conn}}',
               'api_key':'{{var.value.api_key}}'
            }
    )
task1>>task2>>task3>>task4