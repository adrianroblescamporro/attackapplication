import socket
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from htmlstructure import HTML
from HTTPrequest import HTTPrequest
from selenium import webdriver


class Cracker(HTTPrequest):
    def __init__(self, url,dictionary_user, dictionary_pass):
        super().__init__()
        self.numrequests = 0
        self.urlattack = url
        self.dictusername=dictionary_user
        self.dictpassword=dictionary_pass

    def basicauthcrack(self):
        dictus=open(self.dictusername)
        dictpass=open(self.dictusername)
        exit=False
        for lineaus in dictus:
            if exit:
                break
            username=lineaus
            for lineapass in dictpass:
                password=lineapass
                request={'method':'get', 'url':self.urlattack,'auth':HTTPBasicAuth(username, password)}
                response,result = self.request(request)
                if result['status']<0:
                    print('Error en la conexión')
                    break
                if response.status_code == 200:
                    exit=True
                    print('Usuario '+username+' y contraseña '+password+' válidos')
                    break
        if not exit:
            print('Ningún usuario y contraseña válidos')
        dictus.close()
        dictpass.close()

    def digestauthcrack(self):
        dictus = open(self.dictusername)
        dictpass = open(self.dictusername)
        exit = False
        for lineaus in dictus:
            if exit:
                break
            username = lineaus
            for lineapass in dictpass:
                password = lineapass
                request = {'method': 'get', 'url': self.urlattack, 'auth': HTTPDigestAuth(username, password)}
                response, result = self.request(request)
                if result['status'] < 0:
                    print('Error en la conexión')
                    break
                if response.status_code == 200:
                    exit = True
                    print('Usuario ' + username + ' y contraseña ' + password + ' válidos')
                    break
        if not exit:
            print('Ningún usuario y contraseña válidos')
        dictus.close()
        dictpass.close()

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