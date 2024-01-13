import requests 
import random as r
from PIL import Image
from io import BytesIO

imagenrandom=r.randrange(0,101,1) 
print(imagenrandom)
# 1. URL de destino
url = "https://api.imgflip.com/get_memes"
headers = {"Accept-Encoding": "gzip, deflate"} #datos que se requieren para acceder a la api
# 2. Obtener response
response = requests.get(url, headers=headers)   
data = response.json()  #se le da formato al response
# 3. Verificar keys de data (info que tiene la api )
print(data.keys())  
# 4. Mirar estructura y consistencia de datos
print(len(data['data']['memes'])) #cantidad de keys que tiene dentro de data / memes
print(data['data']['memes'][imagenrandom])    #se muestra el meme numero 3 
#5. Obtener figura aleatoria
#destino= data['data']['memes'][3]
destino= data['data']['memes'][imagenrandom]
response = requests.get(destino['url'])
img = Image.open(BytesIO(response.content))
img.save("Practica/Semana 1/Manual de practicas/imagen_meme.jpeg", "JPEG")
print('Proceso finalizado con exito')