PRIMERA ENTREGA

Buenas, la API que consumo es de informacion de futbol : Api-Football, los endpoint que se consumen son 2 :

    Standings : Devuelve una tabla de una o más clasificaciones según la liga / copa.

    Frecuencia de actualización: Este endpoint se actualiza cada hora.

    Fixtures : Lista de partidos, incluye info de equipos que juegan, estadios ,score y liga.

    Frecuencia de actualización: Esta endpoint se actualiza cada 15 segundos.

Para esta primera entrega se realizo la consulta a ambos endpoint guardando en 3 tablas en redshift . La info que se extrajo fue de la premier league (liga inglesa) para la temporada actual(2023-2024):

    ESQUEMA "mxxn13_coderhouse".
    TABLA "posiciones_premier_league" : Lista de todos los equipos (20) con sus puntos , partidos jugados , partidos ganados ,empatados,etc
    TABLA "partidos_premier_league" : Lista de todos los partidos jugados y por jugar de la temporada con sus respectivos datos (goles,referi,equipos enfrentados,etc)
    TABLA "estadios_premier_league" : Tabla auxiliar sacada del mismo enpoint "fixtures" ,con datos de los estadios donde se jugo/jugaran los partidos de los 20 equipos de la temporada.

SEGUNDA ENTREGA

    Se sumaron manipulaciones de datos para evitar duplicados y nulos (dropna y drop_duplicates)
    Se agrego la creacion de las tablas en redshift con claves primarias
    Se agrego truncates antes de las inserciones y se cambio la insercion a tipo append para evitar que borre la tabla reemplazandola por una sin primary keys

TERCERA ENTREGA

    Se paso al sistema de entrega por GitHub : 
    se cambio los create tables
    se cambio el keys.py
    se agrego keys a airflow ,explicar como crear
    se crea tabla de scrips dentro de dags
    