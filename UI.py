import sys
from PyQt5 import uic, QtWidgets
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

    def check_api_key(self, possible_api_key):
        try:
            api = Shodan(possible_api_key)
            info = api.info()
            return True
        except Exception:
            return False

    def ejecutar_busqueda(self):
        apikey = self.lineEdit.text()
        filtro = self.lineEdit_2.text()
        self.listWidget.clear()

        if apikey == "" or filtro == "":
            QMessageBox.critical(self, "Error", "Algún campo incompleto", QMessageBox.StandardButton.Ok)

        else:
            if self.check_api_key(apikey):
                shodanbrowser = Shodanbrowser(apikey)
                self.devices = shodanbrowser.searchiotdevices(filtro)
                num=1
                for device in self.devices:
                    listWidgetItem = QListWidgetItem(str(num)+". IP = "+device+" Port = "+str(self.devices[device]))
                    self.listWidget.addItem(listWidgetItem)
                    num+=1
            else:
                QMessageBox.critical(self, "Error", "API-Key no válida", QMessageBox.StandardButton.Ok)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
