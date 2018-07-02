import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtWidgets, uic, QtCore
import py_form
from db.db import session
from db.db_lib import Storage
from client_read import ClientRead


# client.connect_to_server()

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#
#     w = QWidget()
#     w.resize(250, 150)
#     w.move(300,300)
#     w.setWindowTitle('Simple')
#     w.show()
#
#     sys.exit(app.exec_())


# app = QtWidgets.QApplication(sys.argv)
# window = uic.loadUi('untitled.ui')
# window.show()
#
# sys.exit(app.exec_())


# class MyWindow(QtWidgets.QMainWindow):
#
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         uic.loadUi('untitled.ui', self)
#
#
# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     window = MyWindow()
#     window.show()
#     print(window.tabWidget)
#     sys.exit(app.exec_())


app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()
ui = py_form.Ui_MainWindow()
ui.setupUi(window)
repo = Storage(session)
client_r = ClientRead(name='Kolya')


def load_contacts():
    contacts = repo.get_contacts(client_r.name)
    ui.listWidgetContacts.clear()
    for contact in contacts:
        contact_str = str(contact)
        contact_str = contact_str[10:-3]
        ui.listWidgetContacts.addItem(contact_str)


def load_online():
    clients = repo.get_clients()
    ui.listWidgetOnline.clear()
    for client in clients:
        client_str = str(client)
        client_str = client_str[10:-3]
        ui.listWidgetOnline.addItem(client_str)


load_online()
load_contacts()
window.show()


def send():
    text = ui.textEditEnter.toPlainText()
    ui.textEditChat.append(text)
    ui.textEditEnter.clear()


def add_contact():
    contact = ui.textEditClientAppend.toPlainText()
    repo.add_client(contact)
    repo.add_contact(client_r.name, contact)
    ui.listWidgetContacts.addItem(contact)
    ui.textEditClientAppend.clear()


def remove_contact():
    item = ui.listWidgetContacts.currentItem()
    contact_name = item.text()
    print(contact_name)

    repo.del_contact(client_r.name, contact_name)
    item = ui.listWidgetContacts.takeItem(ui.listWidgetContacts.row(item))
    del item


def remove_online():
    item = ui.listWidgetOnline.currentItem()
    client_name = item.text()
    print(client_name)
    repo.remove_client(client_name)
    item = ui.listWidgetOnline.takeItem(ui.listWidgetOnline.row(item))
    del item


def new_tab():
    item = ui.listWidgetContacts.currentItem()
    contact_name = item.text()
    widget = QtWidgets.QListWidget()
    widget.setGeometry(QtCore.QRect(10, 10, 541, 411))
    ui.tabWidgetChat.addTab(widget, contact_name)


ui.pushButton.clicked.connect(send)
ui.pushButtonAddClient.clicked.connect(add_contact)
ui.pushButtonRemove.clicked.connect(remove_contact)
ui.pushButtonOnlineRefresh.clicked.connect(load_online)
ui.pushButtonOnlineRemove.clicked.connect(remove_online)
ui.pushButtonChat.clicked.connect(new_tab)


sys.exit(app.exec_())