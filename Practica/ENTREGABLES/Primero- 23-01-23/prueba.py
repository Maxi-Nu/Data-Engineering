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
#CONEXION Y EXTRACCION DE DATOS DE LA SEGUNDA URL(DATOS DE JUGADORES)------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
try:
    lista_jug=[]
    #consulto la cantidad de paginas que tiene la api para luego recorrerlas
    paginas = requests.get(url2, params=params, headers=headers)
    response_json = json.loads(paginas.text)
    cantidad_paginas=response_json['paging']['total']+1
    print(cantidad_paginas)
    #-----------------------------------------------------------------------
    #for x in range(1,cantidad_paginas):
     #       respuesta_2 = requests.get(url2, params=params|{'page':x}, headers=headers)
    respuesta_2 = requests.get(url2, params=params|{'page':1}, headers=headers)
    #e wady 181822
            # Verifica si la solicitud fue exitosa (código de estado 200)
    if respuesta_2.status_code == 200:
                # Procesa la respuesta de la API
                lista=[]
                response_json = json.loads(respuesta_2.text)
                lista.append(response_json)
                respuesta_2 = requests.get(url2, params=params|{'page':2}, headers=headers)
                response_json2 =  json.loads(respuesta_2.text)
                lista.append(response_json2)
                #data_jugadores= response_json['response']
                print(lista[1])
                #for i in range(len(data_jugadores)):
                    #--------------------------------------------------------
                    #EQUIPOS de la tabla
                
                    #FECHA DE ACTUALIZACION DE LA API
                # fecha_actualizacion=data_jugadores[i]["update"]
                    #--------------------------------------------------------
                    #dicc_pos={"id_eq":id_eq,"name_eq":name_eq,"logo_eq":logo_eq,"puesto":puesto,"puntos":puntos,"part_jugados":part_jugados,"part_ganados":part_ganados,"part_empatados":part_empatados,
                    #          "part_perdidos":part_perdidos,"goles_favor":goles_favor,"goles_contra":goles_contra,"fecha_actualizacion":fecha_actualizacion}
                    #lista_jug.append(dicc_pos)
                    #fin del for

                #df_posiciones = pd.DataFrame(lista_pos)

                #Dataframe a redshift
                #try:
                #    df_posiciones.to_sql('mxxn13_coderhouse.tabla_posiciones_premier_league',conn,index=False,if_exists='replace')
                #except:
                #    print('Error en la carga de datos a redshift')
    else:
        # Muestra un mensaje de error si la solicitud no fue exitosa
        print("Error en la solicitud. Código de estado:", respuesta_2.status_code)
except requests.exceptions.RequestException as e:
    # Muestra un mensaje si hay un error en la solicitud
    print("Error en la solicitud:", e)