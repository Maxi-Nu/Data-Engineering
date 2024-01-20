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
url2='https://v3.football.api-sports.io/players'

params = {'league': '39', 'season': year} 

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': keys.api_key
}

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#CONEXION Y EXTRACCION DE DATOS DE PRIMERA URL(DATOS DE POSICIONES)--------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
try:
    lista_pos=[]
    respuesta = requests.get(url, params=params, headers=headers)
    # Verifica si la solicitud fue exitosa (código de estado 200)
    if respuesta.status_code == 200:
        # Procesa la respuesta de la API
        response_json = json.loads(respuesta.text)
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
                      "part_perdidos":part_perdidos,"goles_favor":goles_favor,"goles_contra":goles_contra,"fecha_actualizacion":fecha_actualizacion}
            lista_pos.append(dicc_pos)
            #fin del for

        df_posiciones = pd.DataFrame(lista_pos)

        #Dataframe a redshift
        try:
            df_posiciones.to_sql('mxxn13_coderhouse.tabla_posiciones_premier_league',conn,index=False,if_exists='replace')
        except:
            print('Error en la carga de datos a Redshift.')
    else:
        # Muestra un mensaje de error si la solicitud no fue exitosa
        print("Error en la solicitud. Código de estado:", respuesta.status_code)
        
except requests.exceptions.RequestException as e:
    # Muestra un mensaje si hay un error en la solicitud
    print("Error en la solicitud:", e)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#CONEXION Y EXTRACCION DE DATOS DE LA SEGUNDA URL(DATOS DE JUGADORES)------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------


#pendiente ...