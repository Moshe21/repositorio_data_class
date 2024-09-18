import requests,json

def obteneripdesdedominio(dominios):
    print("------dominio->"+str(dominios+"-----"))
    resultadobusqueda = requests.get("https://networkcalc.com/api/dns/lookup/"+str(dominios))
    if resultadobusqueda.json()['records'] != None:
        for i in range(len(resultadobusqueda.json()['records']['A'])):
            ip = resultadobusqueda.json()['records']['A'][i]['address']
            resultadoregion= requests.get("https://ipinfo.io/"+str(ip)+"/json")
            print("la region de la ip ->"+str(ip)+" es "+str(resultadoregion.json()))
dominios=[
    "notonthehighstreet.com",
    "opumo.com",
    "trouva.com",
    "chairish.com",
    "madeinindonesia.com",
    "folksy.com",
    "uncommongoods.com",
    "storenvy.com",
    "tictail.com",
    "cratejoy.com",
    "bonanza.com",
    "reverb.com",
    "shedul.com",
    "storables.com",
    "fyvor.com",
    "thestore.com",
    "sivvi.com",
    "namshi.com",
    "kooomo.com",
    "coupang.com",
    "lightinthebox.com",
    "jdworldwide.com",
    "github.com",
    "spacex.com",
    "platzi.com"
]




def obteneremailsdesdedominio(dominios):
    resultadoemails = requests.get("https://api.hunter.io/v2/domain-search?domain="+str(dominios)+ "&api_key=3be4bd56d0e0b0de1b899203b1a98102bede7166")

for i in dominios:
    obteneripdesdedominio(i)