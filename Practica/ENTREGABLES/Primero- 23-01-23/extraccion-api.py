import requests
import pandas as pd
import json
import datetime
import key
from sqlalchemy import create_engine


#DATOS PARA LA API
date = datetime.date.today()
year = int(date.strftime("%Y"))-1
print(f"Current Year -> {year}")

url = "https://v3.football.api-sports.io/standings"
params = {'league': '39', 'season': year}

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': key.api_key
}

#CONEXION Y EXTRACCION DE DATOS 
try:
    lista_liga=[]
    lista_equipos=[]
    respuesta = requests.get(url, params=params, headers=headers)
    # Verifica si la solicitud fue exitosa (código de estado 200)
    if respuesta.status_code == 200:
        # Procesa la respuesta de la API
        response_json = json.loads(respuesta.text)
        data_liga= response_json['response'][0]['league']['standings'][0]
        print(len(data_liga))#20 es el total de equipos de la liga - se trae la lista y sus estadisticas actualizadas (partidos ganados-empatados-perdidos-puntos y posicion)
        for i in range(len(data_liga)):
            #equipos
            id_eq=data_liga[i]["team"]["id"]
            name_eq=data_liga[i]["team"]["name"]
            logo_eq=data_liga[i]["team"]["logo"]
            lista_equipos=lista_equipos.append()
            #partidos

            #df = pd.DataFrame(data)

    # Imprime el DataFrame
        #print(df)

    else:
        # Muestra un mensaje de error si la solicitud no fue exitosa
        print("Error en la solicitud. Código de estado:", respuesta.status_code)

except requests.exceptions.RequestException as e:
    # Muestra un mensaje si hay un error en la solicitud
    print("Error en la solicitud:", e)