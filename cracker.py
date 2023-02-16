import requests
import socket
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from html import HTML


class Cracker():
    def __init__(self, url):
        self.numrequests = 0
        self.urlattack = url
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    def basicauthcrack(self, username, password):
        response = requests.get(self.urlattack, auth=HTTPBasicAuth(username, password))
        if response.status_code == 200:
            print('Usuario y contraseña válidos')

    def digestauthcrack(self, username, password):
        response = requests.get(self.urlattack, auth=HTTPDigestAuth(username, password))
        if response.status_code == 200:
            print('Usuario y contraseña válidos')

    def formcrack(self, username, password):
        result = {'status': 0}
        try:
            response = requests.get(self.urlattack)
        except requests.exceptions.ConnectionError:
            result = {'status': -1}
        except socket.timeout:
            result = {'status': -2}

        if result['status'] < 0:
            print('Error in connection')

        if response.status_code != 200 or response.status_code != 403:
            print('Bad Status code')

        htmlcode = HTML(response.text)
        login_form = htmlcode.get_login_forms()
        print(login_form)
