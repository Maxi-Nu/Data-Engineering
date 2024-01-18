import requests
import json
from pprint import pprint

ts=1
private_key ='675938500adefc8aff65e39d088a699c7020ab1c' 
public_key='e5ff055ba880b19ec5ae79656137e397'

#documentacion de marvel dice que se deben unir 
#ts, su clave privada y su clave pública (por ejemplo, md5(ts.privateKey.publicKey)
#ts + pvk+ pk: 1675938500adefc8aff65e39d088a699c7020ab1ce5ff055ba880b19ec5ae79656137e397
#se hashea en md5 en la pag: https://www.md5hashgenerator.com/
hashed='06c2388163e38dfc888ae7ad5e0043ca'

url=f'https://gateway.marvel.com:443/v1/public/characters?ts={ts}&apikey={public_key}&hash={hashed}'
url2=f'https://gateway.marvel.com:443/v1/public/comics?orderBy=-onsaleDate&ts={ts}&apikey={public_key}&hash={hashed}'

response= requests.get(url2) 

print(response)#si es una tipo get debe devolver 200 que es correcta 
print(url2)#
lista =[]

if response.status_code==200:
   response_json=json.loads(response.text)
   comics=response_json['data']['results']
#    personajes=(response_json['data']['results'])
#   for i in personajes:
#        id=i["id"]
#        nombre=i["name"]
#        descripcion=i["description"]
#        cant_comics=i["comics"]["available"]
#        cant_series=i["series"]["available"]
#        dic={"id":id,"nombre:":nombre,"descripcion":descripcion,"cant_comics":cant_comics,"cant_series":cant_series}
#        lista.append(dic)
#print(lista)
#print(len(lista))
    for i in comics:
        id=i["id"]
        title=i["name"]
        descripcion=i["description"]
        cant_comics=i["comics"]["available"]
        cant_series=i["series"]["available"]
        dic={"id":id,"title:":title,"descripcion":descripcion,"cant_comics":cant_comics,"cant_series":cant_series}
        lista.append(dic)
print(lista)