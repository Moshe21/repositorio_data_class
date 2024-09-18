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
    "apple.com", "google.com", "microsoft.com", "amazon.com", "facebook.com",
    "netflix.com", "samsung.com", "tesla.com", "ibm.com", "intel.com",
    "oracle.com", "adobe.com", "salesforce.com", "uber.com", "airbnb.com",
    "spotify.com", "twitter.com", "linkedin.com", "yahoo.com", "ebay.com",
    "alibaba.com", "tencent.com", "baidu.com", "zoom.us", "shopify.com",
    "paypal.com", "square.com", "reddit.com", "dropbox.com", "slack.com",
    "stripe.com", "pinterest.com", "vmware.com", "nvidia.com", "sap.com",
    "qualcomm.com", "palantir.com", "hp.com", "dell.com", "lenovo.com",
    "asus.com", "acer.com", "xiaomi.com", "huawei.com", "sony.com",
    "panasonic.com", "toshiba.com", "bosch.com", "siemens.com", "ge.com",
    "honeywell.com", "3m.com", "jnj.com", "pfizer.com", "novartis.com",
    "roche.com", "merck.com", "astrazeneca.com", "gsk.com", "sanofi.com",
    "abbvie.com", "amgen.com", "biogen.com", "lilly.com", "gilead.com",
    "regeneron.com", "vrtx.com", "texasinst.com", "broadcom.com",
    "analog.com", "micron.com", "qualcomm.com"
]


for dominio in dominios_empresa:
    obtenerIPdesdeDominio(dominio)
    obtenerEmailsdesdeDominio(dominio)

