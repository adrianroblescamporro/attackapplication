import requests
from shodan import Shodan

class Shodanbrowser:

    #Metodo que inicializa la api de Shodan con la API-Key gratuita
    def __init__(self, api_key):
        try:
            self.api = Shodan(api_key)
        except Exception as e:
            print('Error: {}'.format(e))
        
    # Metodo que realiza la busqueda filtrando por dispositivos iot con http
    def searchiotdevices(self, query):
        devices=0
        try:
            results = self.api.search(query)
            for result in results['matches']:
                host=self.api.host(result['ip_str'])

                #if ('iot' in host['tags']):
                    #for port in host['ports']:
                        #urlhost='http://'+str(result['ip_str'])+':'+str(port)
                        #result = {'status': 0}
                        #try:
                            #response=requests.get(urlhost)
                        #except requests.exceptions.ConnectionError:
                            #result={'status':-1}
                        #if result['status']>=0:
                devices+=1
                print(result['ip_str'])
                print(result['data'])
                print(host['ports'])

            return devices
        except Exception as e:
            print('Error: {}'.format(e))




