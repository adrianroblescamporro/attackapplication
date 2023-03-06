import sys
from PyQt5 import uic, QtWidgets
from shodan_api import Shodanbrowser

# Inicializa las ventanas
from PyQt5.QtWidgets import QMessageBox, QWidget, QHBoxLayout, QLabel, QComboBox

qtCreatorFile = "UI.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.devices = {}
        self.pushButton.clicked.connect(self.ejecutar_busqueda)

    def ejecutar_busqueda(self):
        apikey = self.lineEdit.text()
        filtro = self.lineEdit_2.text()

        if apikey == "" or filtro == "":
            QMessageBox.critical(self, "Error", "Algún campo incompleto", QMessageBox.StandardButton.Ok)

        else:
            shodanbrowser = Shodanbrowser(apikey)
            if shodanbrowser.notvalid:
                QMessageBox.critical(self, "Error", "API-KEY no válida", QMessageBox.StandardButton.Ok)
            self.devices = shodanbrowser.searchiotdevices(filtro)
            for device in self.devices:
                item=QWidget()
                item_layout=QHBoxLayout()
                item_layout.setContentsMargins(0,0,0,0)
                item.setLayout(item_layout)
                item.layout().addWidget(QLabel(device))

                values=QComboBox()
                values.addItems(self.devices[device])
                item.layout().addWidget(values)
                item.layout().setStretch(0,1)
                item.layout().setStretch(1,8)
                self.listWidget.layout().addWidget(item)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
