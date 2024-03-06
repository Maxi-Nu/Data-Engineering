import requests
import pandas as pd
import json
import datetime
from sqlalchemy import create_engine

def api_etl(redshift_conn,api_key):
    #CONEXION A REDSHIFT
    conn=create_engine(redshift_conn)

    #DATOS PARA LA API
    date = datetime.date.today()
    year = int(date.strftime("%Y"))-1 #SE DEBERIA HACER UN IF PARA QUE CONSIDERE SI ESTAMOS EN LA TEMPORADA ANTES DEL RECESO A MEDIO AÑO O DESPUES (DONDE CAMBIA DE AÑO AL AÑO ACTUAL) 
    print(f"Current Year -> {year}") #AÑO DE LA TEMPORADA A BUSCAR (TEMP ACTUAL 23-24 )

    url = "https://v3.football.api-sports.io/standings"
    url2='https://v3.football.api-sports.io/fixtures'

    params = {'league': '39', 'season': year}

    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': api_key
    }

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #CONEXION Y EXTRACCION DE DATOS DE PRIMERA URL(DATOS DE POSICIONES)--------------------------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    lista_pos=[]
    respuesta_pos = requests.get(url, params=params, headers=headers)
    # Verifica si la solicitud fue exitosa (código de estado 200)
    if respuesta_pos.status_code == 200:
        # Procesa la respuesta_pos de la API
        response_json = json.loads(respuesta_pos.text)
        data_liga= response_json['response'][0]['league']['standings'][0]
        print('Total de equipos de la liga:',len(data_liga))#20 es el total de equipos de la liga - se trae la lista y sus estadisticas actualizadas (partidos ganados-empatados-perdidos-puntos y posicion)
        for i in range(len(data_liga)):
            #--------------------------------------------------------
            #EQUIPOS de la tabla
            id_eq=data_liga[i]["team"]["id"]
            name_eq=data_liga[i]["team"]["name"]
            logo_eq=data_liga[i]["team"]["logo"]
            #POSICIONES DE LA LIGA
            puesto=data_liga[i]["rank"]
            puntos=data_liga[i]["points"]
            part_jugados=data_liga[i]["all"]["played"]
            part_ganados=data_liga[i]["all"]["win"]
            part_empatados=data_liga[i]["all"]["draw"]
            part_perdidos=data_liga[i]["all"]["lose"]
            goles_favor=data_liga[i]["all"]["goals"]["for"]
            goles_contra=data_liga[i]["all"]["goals"]["against"]
            #FECHA DE ACTUALIZACION DE LA API
            fecha_actualizacion=data_liga[i]["update"]
            #--------------------------------------------------------
            dicc_pos={"id_eq":id_eq,"name_eq":name_eq,"logo_eq":logo_eq,"puesto":puesto,"puntos":puntos,"part_jugados":part_jugados,"part_ganados":part_ganados,"part_empatados":part_empatados,
                      "part_perdidos":part_perdidos,"goles_favor":goles_favor,"goles_contra":goles_contra,"fecha_actualizacion":fecha_actualizacion,'Fecha_ingesta':str(date)}
            lista_pos.append(dicc_pos)
            #-------------------------------------------------------- #-------------------------------------------------------- #--------------------------------------------------------
            #FIN DEL FOR
            
        # Truncar la tabla antes de insertar nuevos datos
        truncate_sql = "TRUNCATE TABLE posiciones_premier_league;"
        try:
          with conn.connect() as con:
            con.execute(truncate_sql)
          print('Tabla truncada exitosamente.')
        except Exception as e:
          raise ValueError('Error al truncar la tabla(posiciones_premier_league):', e)

        # Preparar los datos para la inserción en la tabla

        df_posiciones = pd.DataFrame(lista_pos).drop_duplicates(subset=['id_eq']).dropna(subset=['id_eq'])
        print(df_posiciones.shape)

        #Dataframe a redshift
        # Insertar los datos en la tabla
        try:
          with conn.connect() as con:
            df_posiciones.to_sql('posiciones_premier_league', con, index=False, if_exists='append', method='multi',schema='mxxn13_coderhouse')
          print('Carga de posiciones completa.')
        except Exception as e:
          raise ValueError('Error en la carga de datos de posiciones a Redshift:', e)
          

    else:
        # Muestra un mensaje de error si la solicitud no fue exitosa
        raise ValueError("Error en la solicitud de posiciones. Código de estado:", respuesta_pos.status_code)

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #CONEXION Y EXTRACCION DE DATOS DE SEGUNDA URL(DATOS DE PARTIDOS)--------------------------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    lista_par=[]
    lista_estadios=[]
    respuesta_par = requests.get(url2, params=params, headers=headers)
    # Verifica si la solicitud fue exitosa (código de estado 200)
    if respuesta_par.status_code == 200:
        # Procesa la respuesta_par de la API
        response_json_2 = json.loads(respuesta_par.text)
        data_partidos= response_json_2['response']
        print(len(data_partidos))
        for j in range(len(data_partidos)):
            #--------------------------------------------------------
            #PARTIDOS
            id_partido=data_partidos[j]["fixture"]["id"]
            referi=data_partidos[j]["fixture"]["referee"]
            timezone=data_partidos[j]["fixture"]["timezone"]
            fecha=data_partidos[j]["fixture"]["date"]
            status_par=data_partidos[j]["fixture"]["status"]["long"]
            #-----
            id_eq_local=data_partidos[j]["teams"]["home"]["id"]
            eq_local_win=data_partidos[j]["teams"]["home"]["winner"]
            eq_local_goles=data_partidos[j]["goals"]["home"]
            #----
            id_eq_visitante=data_partidos[j]["teams"]["away"]["id"]
            eq_visitante_win=data_partidos[j]["teams"]["away"]["winner"]
            eq_visitante_goles=data_partidos[j]["goals"]["away"]
            #ESTADIOS
            id_estadio=data_partidos[j]["fixture"]["venue"]["id"]
            nombre_estadio=data_partidos[j]["fixture"]["venue"]["name"]
            ciudad=data_partidos[j]["fixture"]["venue"]["city"]
            #--ESTADISTICAS
            resultado_final_local=data_partidos[j]["score"]["fulltime"]["home"]
            resultado_final_visitante=data_partidos[j]["score"]["fulltime"]["away"]
            resultado_extratime_local=data_partidos[j]["score"]["extratime"]["home"]
            resultado_extratime_visitante=data_partidos[j]["score"]["extratime"]["away"]
            penales_local=data_partidos[j]["score"]["penalty"]["home"]
            penales_visitante=data_partidos[j]["score"]["penalty"]["away"]

            #--------------------------------------------------------
            # Datos de partidos
            datos_partidos = {
                'id_partido': id_partido,
                'referi': referi,
                'timezone': timezone,
                'fecha': fecha,
                'status_par': status_par,
                'id_eq_local': id_eq_local,
                'eq_local_win': eq_local_win,
                'eq_local_goles': eq_local_goles,
                'id_eq_visitante': id_eq_visitante,
                'eq_visitante_win': eq_visitante_win,
                'eq_visitante_goles': eq_visitante_goles,
                'resultado_final_local': resultado_final_local,
                'resultado_final_visitante': resultado_final_visitante,
                'resultado_extratime_local': resultado_extratime_local,
                'resultado_extratime_visitante': resultado_extratime_visitante,
                'penales_local': penales_local,
                'penales_visitante': penales_visitante
            }

            # Datos de estadios
            datos_estadios = {
                'id_estadio': id_estadio,
                'nombre_estadio': nombre_estadio,
                'ciudad': ciudad,
                'id_equipo':id_eq_local
            }
            lista_par.append(datos_partidos)
            lista_estadios.append(datos_estadios)
    #-------------------------------------------------------- #-------------------------------------------------------- #--------------------------------------------------------
            #FIN DEL FOR
        #CARGA DE PARTIDOS
        # Truncar la tabla antes de insertar nuevos datos

        truncate_sql = "TRUNCATE TABLE partidos_premier_league;"
        try:
          with conn.connect() as con:
            con.execute(truncate_sql)
          print('Tabla truncada exitosamente.')
        except Exception as e:
          raise ValueError('Error al truncar la tabla(partidos_premier_league):', e)

        # Preparar los datos para la inserción en la tabla  
        df_partidos = pd.DataFrame(lista_par).drop_duplicates(subset=['id_partido']).dropna(subset=['id_partido']) 
        print(df_partidos.shape)
        # Insertar los datos en la tabla
        try:
            with conn.connect() as con:
                df_partidos.to_sql('partidos_premier_league', con, index=False, if_exists='append', method='multi',schema='mxxn13_coderhouse')
            print('Carga de partidos completa.')
        except Exception as e:
            raise ValueError('Error en la carga de datos de partidos a Redshift:', e)

    #-------------------------------------------------------- #-------------------------------------------------------- #--------------------------------------------------------
        #CARGA DE ESTADIOS
        # Truncar la tabla antes de insertar nuevos datos

        truncate_sql = "TRUNCATE TABLE estadios_premier_league;"
        try:
          with conn.connect() as con:
            con.execute(truncate_sql)
          print('Tabla truncada exitosamente.')
        except Exception as e:
          raise ValueError('Error al truncar la tabla (estadios_premier_league):', e)

        # Preparar los datos para la inserción en la tabla  
        df_estadios= pd.DataFrame(lista_estadios).drop_duplicates(subset=['id_estadio', 'ciudad']).dropna(subset=['id_estadio'])
        print(df_estadios.shape) 
        # Insertar los datos en la tabla
        try:
            with conn.connect() as con:
                df_estadios.to_sql('estadios_premier_league', con, index=False, if_exists='append', method='multi',schema='mxxn13_coderhouse')
            print('Carga de estadios completa.')
        except Exception as e:
           raise ValueError('Error en la carga de datos de estadios a Redshift:', e)
    else:
        # Muestra un mensaje de error si la solicitud no fue exitosa
        raise ValueError("Error en la solicitud de partidos y estadios. Código de estado:", respuesta_par.status_code)     