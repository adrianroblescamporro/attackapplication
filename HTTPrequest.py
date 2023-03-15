
import requests
import socket
from requests.packages.urllib3.exceptions import InsecureRequestWarning


class HTTPrequest:
    request_tries = 3

    def __init__(self):
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    def request(self, request):
        result = {'status': 0}
        response = None
        tries = self.request_tries
        while tries > 0:
            try:
                response = requests.request(**request)
                break

            except requests.exceptions.ConnectionError:
                result = {'status': -1}

            except socket.timeout:
                result = {'status': -2}

            tries -= 1

        return response, result
