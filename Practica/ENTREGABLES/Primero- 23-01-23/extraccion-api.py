import requests
import pandas as pd
import json
import datetime
import keys
from sqlalchemy import create_engine

#CONEXION A REDSHIFT
conn=create_engine(keys.redshift_conn)

#DATOS PARA LA API
date = datetime.date.today()
year = int(date.strftime("%Y"))-1
print(f"Current Year -> {year}")

#conexion a tabla de posiciones
url = "https://v3.football.api-sports.io/standings"
#conexion a tabla de jugadores de cada equipos
url2='https://v3.football.api-sports.io/fixtures'

params = {'league': '39', 'season': year} 

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': keys.api_key
}

try:

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
        print(len(data_liga))#20 es el total de equipos de la liga - se trae la lista y sus estadisticas actualizadas (partidos ganados-empatados-perdidos-puntos y posicion)
        #print(data_liga[0])
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
            #fin del for

        df_posiciones = pd.DataFrame(lista_pos)

        #Dataframe a redshift
        try:
            df_posiciones.to_sql('mxxn13_coderhouse.posiciones_premier_league',conn,index=False,if_exists='replace')
            print('Carga de posiciones completa.')
        except:
            print('Error en la carga de datos de posiciones a Redshift.')
    else:
        # Muestra un mensaje de error si la solicitud no fue exitosa
        print("Error en la solicitud de posiciones. Código de estado:", respuesta_pos.status_code)
        
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #CONEXION Y EXTRACCION DE DATOS DE SEGUNDA URL(DATOS DE PARTIDOS)--------------------------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

  # lista_par=[]
  #  respuesta_par = requests.get(url2, params=params, headers=headers)
  #  # Verifica si la solicitud fue exitosa (código de estado 200)
  #  if respuesta_par.status_code == 200:
  #      # Procesa la respuesta_par de la API
  #      response_json_2 = json.loads(respuesta_par.text)
  #      data_partidos= response_json_2['response']
  #      print(len(data_partidos))#20 es el total de equipos de la liga - se trae la lista y sus estadisticas actualizadas (partidos ganados-empatados-perdidos-puntos y posicion)
  #      for j in (data_partidos):
  #          #--------------------------------------------------------        
  #          #PARTIDOS
  #          id_partido=data_partidos[j]["fixture"]["id"]
  #          referi=data_partidos[j]["fixture"]["referee"]
  #          timezone=data_partidos[j]["fixture"]["timezone"]        
  #          fecha=data_partidos[j]["fixture"]["date"] 
  #          status_par=data_partidos[j]["fixture"]["status"]["long"] 
  #          #-----
  #          id_eq_local=data_partidos[j]["teams"]["home"]["id"]
  #          eq_local_win=data_partidos[j]["teams"]["home"]["winner"]
  #          eq_local_goles=data_partidos[j]["goals"]["home"]
  #          #----
  #          id_eq_visitante=data_partidos[j]["teams"]["away"]["id"]
  #          eq_visitante_win=data_partidos[j]["teams"]["away"]["winner"]
  #          eq_visitante_goles=data_partidos[j]["goals"]["away"]
  #          #ESTADIOS
  #          id_estadio=data_partidos[j]["fixture"]["venue"]["id"] 
  #          nombre_estadio=data_partidos[j]["fixture"]["venue"]["name"]
  #          ciudad=data_partidos[j]["fixture"]["venue"]["city"]
  #          #--ESTADISTICAS
  #          resultado_final_local=data_partidos[j]["score"]["fulltime"]["home"]
  #          resultado_final_visitante=data_partidos[j]["score"]["fulltime"]["away"]
  #          resultado_extratime_local=data_partidos[j]["score"]["extratime"]["home"]
  #          resultado_extratime_visitante=data_partidos[j]["score"]["extratime"]["away"]
  #          penales_local=data_partidos[j]["score"]["penalty"]["home"]
  #          penales_visitante=data_partidos[j]["score"]["penalty"]["away"]
  #          
  #          #--------------------------------------------------------
  #          dicc_par={"id_eq":id_eq,"name_eq":name_eq,"logo_eq":logo_eq,"puesto":puesto,"puntos":puntos,"part_jugados":part_jugados,"part_ganados":part_ganados,"part_empatados":part_empatados,
  #                    "part_perdidos":part_perdidos,"goles_favor":goles_favor,"goles_contra":goles_contra,"fecha_actualizacion":fecha_actualizacion,'Fecha_ingesta':str(date)}
  #          lista_par.append(dicc_par)
  #          #fin del for
#
  #      df_partidos = pd.DataFrame(lista_par)
#
  #      #Dataframe a redshift
  #      try:
  #          df_partidos.to_sql('mxxn13_coderhouse.partidos_premier_league',conn,index=False,if_exists='replace')
  #          print('Carga de datos de partidos completa correctamente.')
  #      except:
  #          print('Error en la carga de datos de partidos a Redshift.')
  #  else:
  #      # Muestra un mensaje de error si la solicitud no fue exitosa
  #      print("Error en la solicitud de partidos. Código de estado:", respuesta_pos.status_code)

except requests.exceptions.RequestException as e:
    # Muestra un mensaje si hay un error en la solicitud
    print("Error en la solicitud:", e)