import os
import sys
from PyQt5 import uic, QtWidgets, QtGui
from shodan import Shodan

from shodan_api import Shodanbrowser
from cracker import Cracker

# Inicializa las ventanas
from PyQt5.QtWidgets import QMessageBox, QWidget, QHBoxLayout, QLabel, QComboBox, QListWidgetItem

qtCreatorFile = "UI.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


def check_api_key(possible_api_key):
    try:
        api = Shodan(possible_api_key)
        info = api.info()
        return True
    except Exception:
        return False


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.devices = {}
        self.list_dev = {}
        self.pushButton.clicked.connect(self.ejecutar_busqueda)
        self.pushButton_2.clicked.connect(self.ejecutar_ataque)
        self.lineEdit_3.setValidator(QtGui.QIntValidator())
        self.lineEdit_5.setValidator(QtGui.QIntValidator())

    def ejecutar_busqueda(self):
        apikey = self.lineEdit.text()
        filter_search = self.lineEdit_2.text()
        self.listWidget.clear()

        if apikey == "" or filter_search == "":
            QMessageBox.critical(self, "Error", "Algún campo incompleto", QMessageBox.StandardButton.Ok)

        else:
            if check_api_key(apikey):
                shodan_browser = Shodanbrowser(apikey)
                self.devices, self.list_dev = shodan_browser.searchiotdevices(filter_search)
                num = 1
                for element in self.list_dev:
                    listWidgetItem = QListWidgetItem(
                        str(element) + ". IP = " + self.list_dev[element] + " Ports = " + str(
                            self.devices[self.list_dev[element]]))
                    self.listWidget.addItem(listWidgetItem)
                    num += 1
            else:
                QMessageBox.critical(self, "Error", "API-Key no válida", QMessageBox.StandardButton.Ok)

    def ejecutar_ataque(self):
        num_disp = self.lineEdit_3.text()
        dictionary = self.lineEdit_4.text()
        port = self.lineEdit_5.text()
        self.textEdit.clear()
        if num_disp == "" or dictionary == "" or port == "":
            QMessageBox.critical(self, "Error", "Algún campo incompleto", QMessageBox.StandardButton.Ok)
        else:
            if int(num_disp) > len(self.list_dev):
                QMessageBox.critical(self, "Error", "No existe el dispositivo", QMessageBox.StandardButton.Ok)
            else:
                if not os.path.exists(dictionary):
                    QMessageBox.critical(self, "Error", "Ruta de archivo incorrecta", QMessageBox.StandardButton.Ok)
                else:
                    IP = self.list_dev[int(num_disp)]
                    if int(port) in self.devices[IP]:
                        url_attack = 'http://' + IP + ':' + port
                        cracker = Cracker(url_attack, dictionary)
                        result = cracker.detect_auth()
                        if result['status'] >= 0:
                            cracker.attack()
                        else:
                            self.textEdit.append('No se admiten peticiones HTTP')
                    else:
                        QMessageBox.critical(self, "Error", "Puerto no abierto en el dispositivo", QMessageBox.StandardButton.Ok)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
