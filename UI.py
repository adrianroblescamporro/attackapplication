import os
import sys

from PyQt6 import uic, QtWidgets, QtGui
from shodan import Shodan

from shodan_api import Shodanbrowser
from cracker import Cracker

# Inicializa las ventanas
from PyQt6.QtWidgets import QMessageBox, QWidget, QHBoxLayout, QLabel, QComboBox, QListWidgetItem, QFileDialog

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

        self.pushButton.clicked.connect(self.ejecutar_busqueda)
        self.pushButton_2.clicked.connect(self.ejecutar_ataque)
        self.pushButton_3.clicked.connect(self.ejecutar_ataque_ejemplo)
        self.pushButton_4.clicked.connect(self.abrir)
        self.shodan_browser = None
        self.cracker = None
        self.dictionary = " "

    def ejecutar_busqueda(self):
        apikey = self.lineEdit.text()
        filter_search = self.lineEdit_2.text()
        self.listWidget.clear()

        if apikey == "" or filter_search == "":
            QMessageBox.critical(self, "Error", "Algún campo incompleto", QMessageBox.StandardButton.Ok)

        else:
            if check_api_key(apikey):
                self.shodan_browser = Shodanbrowser(apikey, filter_search)
                self.shodan_browser.State.connect(self.label_search.setText)
                self.shodan_browser.Info.connect(self.listWidget.addItem)
                self.shodan_browser.start()


            else:
                QMessageBox.critical(self, "Error", "API-Key no válida", QMessageBox.StandardButton.Ok)

    def ejecutar_ataque(self):
        self.textEdit.clear()
        if self.shodan_browser is None or self.dictionary == "":
            QMessageBox.critical(self, "Error", "Algún campo de información incompleto", QMessageBox.StandardButton.Ok)
        else:
            disp = self.listWidget.currentItem().text()
            if not os.path.exists(self.dictionary):
                QMessageBox.critical(self, "Error", "Ruta de archivo incorrecta", QMessageBox.StandardButton.Ok)
            else:
                url_attack = 'http://' + disp
                self.cracker = Cracker(url_attack, self.dictionary)
                self.cracker.Info.connect(self.textEdit.append)
                self.cracker.start()

    def ejecutar_ataque_ejemplo(self):
        self.textEdit.clear()
        if self.dictionary == "":
            QMessageBox.critical(self, "Error", "Algún campo de información incompleto", QMessageBox.StandardButton.Ok)
        else:
            url_attack = 'http://42.159.198.157:8081'
            self.cracker = Cracker(url_attack, self.dictionary)
            self.cracker.Info.connect(self.textEdit.append)
            self.cracker.start()

    def abrir(self):
        archivo = QFileDialog.getOpenFileName(self, 'Abrir archivo', 'C:\\', "Wanted Files (*.txt)")
        self.dictionary = archivo[0]
        self.label_dictionary.setText('Diccionario cargado')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())
