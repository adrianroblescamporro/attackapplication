import requests
import socket
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from htmlstructure import HTML


class Cracker:
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

        if response.status_code != 200 and response.status_code != 403:
            print('Bad Status code')

        htmlcode = HTML(response.text, "html.parser")
        login_form = htmlcode.get_login_forms()[0]
        datasend = {'data': {}}

        if not (('usr_field' in login_form) and ('pwd_field' in login_form)):
            print('Error: form incorrect')
        if 'fields' in login_form:
            datasend.update(login_form['fields'])

        datasend['data'][login_form['usr_field']] = username
        datasend['data'][login_form['pwd_field']] = password

        responsepost = requests.post(self.urlattack, data=datasend['data'])
        htmlpost = HTML(responsepost.text, "html.parser")

        if (responsepost.status_code == 200) and (login_form not in htmlpost):
            print('Usuario y contraseña válidos')
        else:
            print('Usuario y contraseña incorrectos')
