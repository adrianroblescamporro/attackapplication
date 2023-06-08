
from PyQt6.QtCore import QThread, pyqtSignal
from shodan import Shodan


class Shodanbrowser(QThread):
    Info = pyqtSignal(str)
    State = pyqtSignal(str)

    # Método que inicializa la api de Shodan con la API-Key
    def __init__(self, api_key, query):
        super().__init__()
        self.api = Shodan(api_key)
        self.query = query
        self.devices = 0
        self.num_devices = 1

    # Método que realiza la busqueda filtrando los dispositivos
    def run(self):
        try:
            self.State.emit('Buscando...')
            results = self.api.search(self.query) #búsqueda de dispositivos
            self.num_devices = len(results)
            for result in results['matches']:
                text = result['ip_str'] + ":" + str(result['port'])
                self.print(text)
            self.State.emit('Busqueda finalizada')

        except Exception as e:
            self.Info.emit('Error: {}'.format(e))

    #Método para mostrar el resultado al usuario
    def print(self, text):
        self.Info.emit(text)
