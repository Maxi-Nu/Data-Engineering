# PRIMERA ENTREGA

Buenas, la API que consumo es de informacion de futbol : Api-Football, los endpoint que se consumen son 2 :

  * Standings : Devuelve una tabla de una o más clasificaciones según la liga / copa.

    Frecuencia de actualización: Este endpoint se actualiza cada hora.

  * Fixtures : Lista de partidos, incluye info de equipos que juegan, estadios ,score y liga.

    Frecuencia de actualización: Esta endpoint se actualiza cada 15 segundos.

Para esta primera entrega se realizo la consulta a ambos endpoint guardando en 3 tablas en redshift . La info que se extrajo fue de la premier league (liga inglesa) para la temporada actual(2023-2024):

    ESQUEMA "mxxn13_coderhouse".
    TABLA "posiciones_premier_league" : Lista de todos los equipos (20) con sus puntos , partidos jugados , partidos ganados ,empatados,etc
    TABLA "partidos_premier_league" : Lista de todos los partidos jugados y por jugar de la temporada con sus respectivos datos (goles,referi,equipos enfrentados,etc)
    TABLA "estadios_premier_league" : Tabla auxiliar sacada del mismo enpoint "fixtures" ,con datos de los estadios donde se jugo/jugaran los partidos de los 20 equipos de la temporada.

# SEGUNDA ENTREGA

## Cambios:
  * Se sumaron manipulaciones de datos para evitar duplicados y nulos (dropna y drop_duplicates).
  * Se agrego la creacion de las tablas en redshift con claves primarias.
  * Se agrego truncates antes de las inserciones y se cambio la insercion a tipo append para evitar que borre la tabla reemplazandola por una sin primary keys.

# TERCERA ENTREGA

## Cambios:
  * Se subio todo el proyecto a Github para facilitar la entrega.
  * Cambio en la creacion de las tablas: las tablas se creaban con una comprobacion previa al insertado de datos en la api , ahora se realiza la creacion y comprobacion de existencia de tablas antes en Task de airflow separadas para permitir el relanzamiento en caso de fallo . 
  * Eliminacion del archivo api.key donde se guardaban la key de la api y la conexion con sus credenciales a redshift , se opto por utilizar las variables del propio airflow para proporcionarlas.
  * Se creo una carpeta de scripts dentro de 'Entrega_Final\dags' para poder ejecutar el ETL de la API y los .sql .
  * Se cambio la captura de errores del archivo ExtraccionApi.py para que ahora fuerce el error en las tareas de airflow(se cambio los prints por raise)

## Instrucciones: 
  * Ejecutar el docker-compose up 
  * Una vez levantado el contenedor y teniendo airflow corriendo en localhost:8080 (Loguearse con user : airflow ,pass: airflow ) se debe ir a las opciones:
    - Admin->Connections : creamos una conexion a redshift con las credenciales que se le va a pasar por privado.
    - Admin->Variables : creamos las 2 variables que necesita la api para correr, que se enviaran por privado.