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
            results = self.api.search(query)
            for resultdev in results['matches']:
                # host = self.api.host(resultdev['ip_str'])
                devices[resultdev['ip_str']] = resultdev['port']
                list_dev[count] = resultdev['ip_str']
                count += 1
                # if 'iot' in host['tags']:
                # devices[resultdev['ip_str']] = resultdev['port']
                # for port in host['ports']:
                # urlhost = 'http://' + str(resultdev['ip_str']) + ':' + str(port)
                # request = {'method': 'get', 'url': urlhost}
                # response, result = self.request(request)
                # print(response)
                # print(result)
                # if result['status'] >= 0:
                # devices[resultdev['ip_str']] = port
            return devices, list_dev
        except Exception as e:
            print('Error: {}'.format(e))
