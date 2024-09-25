import requests, json

# Función para obtener IPs y región desde un dominio
def obtenerIPdesdeDominio(dominio):
    print("------ Dominio: " + str(dominio) + " ------")
    resultadoBusqueda = requests.get("https://networkcalc.com/api/dns/lookup/"+str(dominio))
    if resultadoBusqueda.json()['records'] != None:
        for i in range(len(resultadoBusqueda.json()['records']['A'])):
            ip = resultadoBusqueda.json()['records']['A'][i]['address']
            resultadoRegion = requests.get("https://ipinfo.io/"+str(ip)+"/json")
            print("La IP es: " + str(ip) + " y su región es: " + str(resultadoRegion.json()))
    else:
        print(f"No se encontraron registros para {dominio}")


def obtenerEmailsdesdeDominio(dominio):
    print("------ Correos para el dominio: " + str(dominio) + " ------")
    resultadoEmails = requests.get("https://api.hunter.io/v2/domain-search?domain="+str(dominio)+"&api_key=3be4bd56d0e0b0de1b899203b1a98102bede7166")
    if resultadoEmails.status_code == 200:
        print(json.dumps(resultadoEmails.json(), indent=4))
    else:
        print("Error al obtener correos del dominio:", dominio)

# Lista completa de dominios de empresas
dominios_empresa = [
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


for dominio in dominios_empresa:
    obtenerIPdesdeDominio(dominio)
    obtenerEmailsdesdeDominio(dominio)
