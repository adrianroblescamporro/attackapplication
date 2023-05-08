
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QListWidgetItem
from shodan import Shodan


class Shodanbrowser(QThread):
    Info = pyqtSignal(str)
    State = pyqtSignal(str)

    # Metodo que inicializa la api de Shodan con la API-Key gratuita
    def __init__(self, api_key, query):
        super().__init__()
        self.api = Shodan(api_key)
        self.query = query
        self.devices = 0
        self.num_devices = 1

    # Metodo que realiza la busqueda filtrando por dispositivos iot con http
    def run(self):
        try:
            self.State.emit('Buscando...')
            results = self.api.search(self.query)
            self.num_devices = len(results)
            for result in results['matches']:
                text = result['ip_str'] + ":" + str(result['port'])
                self.print(text)
            self.State.emit('Busqueda finalizada')

        except Exception as e:
            self.Info.emit('Error: {}'.format(e))

    def print(self, text):
        self.Info.emit(text)
