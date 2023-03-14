from HTTPrequest import HTTPrequest
from shodan import Shodan


class Shodanbrowser(HTTPrequest):

    # Metodo que inicializa la api de Shodan con la API-Key gratuita
    def __init__(self, api_key):
        super(HTTPrequest, self).__init__()
        self.api = Shodan(api_key)

    # Metodo que realiza la busqueda filtrando por dispositivos iot con http
    def searchiotdevices(self, query):
        try:
            list_dev = {}
            count = 1
            devices = {}
            http_ports = []
            results = self.api.search(query)
            for resultdev in results['matches']:
                host = self.api.host(resultdev['ip_str'])
                list_dev[count] = resultdev['ip_str']
                count += 1
                devices[resultdev['ip_str']] = host['ports']

            return devices, list_dev

        except Exception as e:
            print('Error: {}'.format(e))
