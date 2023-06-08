
import requests
import socket
from requests.packages.urllib3.exceptions import InsecureRequestWarning


class HTTPrequest:
    request_tries = 3 #se va a intentar hacer la petición 3 veces como mucho

    def __init__(self):
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    def request(self, request):
        result = {'status': 0}
        response = None
        tries = self.request_tries
        while tries > 0:
            try:
                response = requests.request(**request) #hacer la petición
                break

            #Posibles excepciones
            except requests.exceptions.ConnectionError:
                result = {'status': -1}

            except requests.exceptions.HTTPError:
                result = {'status': -2}

            except requests.exceptions.Timeout:
                result = {'status': -3}

            except socket.timeout:
                result = {'status': -4}

            tries -= 1

        return response, result
