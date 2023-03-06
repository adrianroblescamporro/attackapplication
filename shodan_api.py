from HTTPrequest import HTTPrequest
from shodan import Shodan


class Shodanbrowser(HTTPrequest):

    # Metodo que inicializa la api de Shodan con la API-Key gratuita
    def __init__(self, api_key):
        super(HTTPrequest, self).__init__()
        self.notvalid = False
        try:
            self.api = Shodan(api_key)
        except Exception as e:
            self.notvalid = True

    # Metodo que realiza la busqueda filtrando por dispositivos iot con http
    def searchiotdevices(self, query):
        try:
            devices = {}
            results = self.api.search(query)
            for resultdev in results['matches']:
                host = self.api.host(resultdev['ip_str'])

                #if 'iot' in host['tags']:
                for port in host['ports']:
                        urlhost = 'http://' + str(resultdev['ip_str']) + ':' + str(port)
                        request = {'method': 'get', 'url': urlhost}
                        response, result = self.request(request)
                        if result['status'] >= 0:
                            devices[resultdev['ip_str']] = port
            return devices
        except Exception as e:
            print('Error: {}'.format(e))
