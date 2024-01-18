import requests
import json
import datetime

date = datetime.date.today()
year = int(date.strftime("%Y"))-1
print(f"Current Year -> {year}")

url = "https://v3.football.api-sports.io/standings"
params = {'league': '39', 'season': year}

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': "9c8d551d3c2173d4d742c93a0d86a553"
}

try:
    # Realiza una solicitud GET a la API utilizando requests
    respuesta = requests.get(url, params=params, headers=headers)

    # Verifica si la solicitud fue exitosa (código de estado 200)
    if respuesta.status_code == 200:
        # Procesa la respuesta de la API
        response_json = respuesta.json()
        print("Datos de la API:", response_json)
    else:
        # Muestra un mensaje de error si la solicitud no fue exitosa
        print("Error en la solicitud. Código de estado:", respuesta.status_code)

except requests.exceptions.RequestException as e:
    # Muestra un mensaje si hay un error en la solicitud
    print("Error en la solicitud:", e)