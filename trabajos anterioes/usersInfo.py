import requests
import json


class usersInfo:


    def __init__(self):
        self.listUsers=[]

    def getUsers(self):
        responseUsers= requests.get("https://datos.gov.co/resource/jtnk-dmga.json")
        dataJson=responseUsers.json()
        for ind in range (len(dataJson)):
            print(dataJson[ind]['email_address'])

    def valideteUsers(self):
        for email in self.listUsers:

prueba2 = usersInfo()

prueba2.getUsers()