import os
import sys

from PyQt6 import uic, QtWidgets
from shodan import Shodan

from shodan_api import Shodanbrowser
from cracker import Cracker

# Inicializa las ventanas
from PyQt6.QtWidgets import QMessageBox, QFileDialog

qtCreatorFile = "UI.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


def check_api_key(possible_api_key):
    try:
        Shodan(possible_api_key).info()
        return True
    except Exception:
        return False


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.pushButton.clicked.connect(self.ejecutar_busqueda) #botón de Buscar
        self.pushButton_2.clicked.connect(self.ejecutar_ataque) #botón de Atacar
        self.pushButton_3.clicked.connect(self.ejecutar_ataque_ejemplo) #botón de Ejemplo ataque form
        self.pushButton_4.clicked.connect(self.abrir) #botón abrir
        self.shodan_browser = None
        self.cracker = None
        self.dictionary = " "

    #Método para ejecutar la búsqueda de dispositivos
    def ejecutar_busqueda(self):
        apikey = self.lineEdit.text()
        filter_search = self.lineEdit_2.text()
        self.listWidget.clear()

        if apikey == "" or filter_search == "": #si no se indica API key o filtro
            QMessageBox.critical(self, "Error", "Algún campo incompleto", QMessageBox.StandardButton.Ok)

        else:
            if check_api_key(apikey): #si la API key es válida
                self.shodan_browser = Shodanbrowser(apikey, filter_search)
                self.shodan_browser.State.connect(self.label_search.setText)
                self.shodan_browser.Info.connect(self.listWidget.addItem)
                self.shodan_browser.start()


            else:
                QMessageBox.critical(self, "Error", "API-Key no válida", QMessageBox.StandardButton.Ok)

    # Método para ejecutar el ataque a un dispositivo seleccionado
    def ejecutar_ataque(self):
        self.textEdit.clear()
        if self.shodan_browser is None or self.dictionary == "": #si no hay shodan_browser o no hay diccionario cargado
            QMessageBox.critical(self, "Error", "Algún campo de información incompleto", QMessageBox.StandardButton.Ok)
        else:
            disp = self.listWidget.currentItem().text()
            if not os.path.exists(self.dictionary): #si el diccionario deja de existir
                QMessageBox.critical(self, "Error", "Ruta de archivo incorrecta", QMessageBox.StandardButton.Ok)
            else:
                url_attack = 'http://' + disp
                self.cracker = Cracker(url_attack, self.dictionary)#crear cracker
                self.cracker.Info.connect(self.textEdit.append)
                self.cracker.start()

    # Método para ejecutar el ataque de ejemplo
    def ejecutar_ataque_ejemplo(self):
        self.textEdit.clear()
        if self.dictionary == "": #si no hay diccionario seleccionado
            QMessageBox.critical(self, "Error", "Algún campo de información incompleto", QMessageBox.StandardButton.Ok)
        else:
            url_attack = 'http://42.159.198.157:8081' #dispositivo con autenticación form
            self.cracker = Cracker(url_attack, self.dictionary) #crear objeto cracker
            self.cracker.Info.connect(self.textEdit.append)
            self.cracker.start()

    # Método para abrir el diccionario
    def abrir(self):
        archivo = QFileDialog.getOpenFileName(self, 'Abrir archivo', 'C:\\', "Wanted Files (*.txt)") # sólo se
        # permiten archivos con extensión .txt
        self.dictionary = archivo[0]
        self.label_dictionary.setText('Diccionario cargado')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())
