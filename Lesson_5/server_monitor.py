from PyQt5 import QtWidgets
import sys
import py_server_monitor
from db.db_lib import Storage
from db.db import session


app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()
ui = py_server_monitor.Ui_MainWindow()
ui.setupUi(window)
repo = Storage(session)


repo.add_client('Kolya')
repo.add_client('Vasya')
repo.add_client('Shakira')
repo.add_contact('Kolya', 'Shakira')


def load_clients():
    clients = repo.get_clients()
    ui.listWidget.clear()

    for clint in clients:
        ui.listWidget.addItem(str(clint))


load_clients()
ui.pushButton.clicked.connect(load_clients)

window.show()
sys.exit(app.exec_())