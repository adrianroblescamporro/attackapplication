import os
import sys
from PyQt5 import uic, QtWidgets, QtGui
from shodan import Shodan

from shodan_api import Shodanbrowser

# Inicializa las ventanas
from PyQt5.QtWidgets import QMessageBox, QWidget, QHBoxLayout, QLabel, QComboBox, QListWidgetItem

qtCreatorFile = "UI.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.devices = {}
        self.pushButton.clicked.connect(self.ejecutar_busqueda)
        self.pushButton_2.clicked.connect(self.ejecutar_ataque)
        self.lineEdit_3.setValidator(QtGui.QIntValidator())

    def check_api_key(self, possible_api_key):
        try:
            api = Shodan(possible_api_key)
            info = api.info()
            return True
        except Exception:
            return False

    def ejecutar_busqueda(self):
        apikey = self.lineEdit.text()
        filter = self.lineEdit_2.text()
        self.listWidget.clear()

        if apikey == "" or filter == "":
            QMessageBox.critical(self, "Error", "Algún campo incompleto", QMessageBox.StandardButton.Ok)

        else:
            if self.check_api_key(apikey):
                shodan_browser = Shodanbrowser(apikey)
                self.devices = shodan_browser.searchiotdevices(filter)
                num = 1
                for device in self.devices:
                    listWidgetItem = QListWidgetItem(
                        str(num) + ". IP = " + device + " Port = " + str(self.devices[device]))
                    self.listWidget.addItem(listWidgetItem)
                    num += 1
            else:
                QMessageBox.critical(self, "Error", "API-Key no válida", QMessageBox.StandardButton.Ok)

    def ejecutar_ataque(self):
        num_disp = self.lineEdit_3.text()
        dict = self.lineEdit_4.text()
        if num_disp == "" or dict == "":
            QMessageBox.critical(self, "Error", "Algún campo incompleto", QMessageBox.StandardButton.Ok)
        else:
            if num_disp > len(self.devices):
                QMessageBox.critical(self, "Error", "No existe el dispositivo", QMessageBox.StandardButton.Ok)
            else:
                if not os.path.exists(dict):
                    QMessageBox.critical(self, "Error", "Ruta de archivo incorrecta", QMessageBox.StandardButton.Ok)
                else:
                    url_attack=
                    cracker=Cracker(dict)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
