import sys
from reseiver import GuiReciever
import time
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtWidgets, uic, QtCore
import py_form
from db.db import session
from db.db_lib import Storage
from client import Client
from PyQt5.QtCore import Qt, QThread, pyqtSlot
from threading import Thread
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal, pyqtSlot
# from chat_form import Ui_ChatForm
# import socket


app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()
ui = py_form.Ui_MainWindow()
ui.setupUi(window)
repo = Storage(session)


addr = 'localhost'
port = 7778




class ClientChat:

    def __init__(self):
        self.set_gui_connected(False)
        # ui.stackedWidgetNewClient.

    def connect(self):
        user = ui.textEditClientConnect.toPlainText()
        # print(type(user))
        # user.lo
        # print(user.count(user))
        # self.user = Client(user)
        # self.user.connect_to_server()
        if len(user) > 11 or len(user) < 1:
            return None
        else:
            self.user = Client(user)
            self.user.connect_to_server(addr, port)
            # self.user.get_clients()
            self.set_gui_connected(True)
            # self.load_online()
            # self.load_contacts()
            self.listener = GuiReciever(self.user.sock, self.user.request_queue)

            self.listener.gotData.connect(client.update_chat)

            # Используем QThread так рекомендуется, но можно и обычный
            # th_listen = threading.Thread(target=listener.poll)
            # th_listen.daemon = True
            # th_listen.start()
            th = QThread()
            self.listener.moveToThread(th)

            # # ---------- Важная часть - связывание сигналов и слотов ----------
            # При запуске потока будет вызван метод search_text
            th.started.connect(self.listener.poll)
            th.start()


    @pyqtSlot(str)
    def update_chat(data):
        ''' Отображение сообщения в истории
        '''
        try:
            msg = data
            # window.listWidgetMessages.addItem(msg)
            ui.textEditChat.append(msg)
        except Exception as e:
            print(e)

    def set_gui_connected(self, enebled):
        ui.pushButton.setEnabled(enebled)
        ui.pushButtonRemove.setEnabled(enebled)
        ui.pushButtonOnlineRefresh.setEnabled(enebled)
        ui.pushButtonOnlineRemove.setEnabled(enebled)
        ui.pushButtonChat.setEnabled(enebled)
        ui.pushButtonConnect.setEnabled(not enebled)

    def load_contacts(self):
        # contacts = repo.get_contacts(self.user.name)
        contacts = self.user.get_contacts(self.user.name)
        print(contacts)
        ui.listWidgetContacts.clear()
        for contact in contacts:
            print(contact)
            # contact_str = str(contact)
            # contact_str = contact_str[10:-3]
            ui.listWidgetContacts.addItem(contact)


    def load_online(self):
        # закинуть в поток для автомотического обновления
        # clients = repo.get_clients()
        # self.user.get_clients()
        clients = self.user.get_clients()
        print(type(clients), clients)
        ui.listWidgetOnline.clear()
        for client in clients:
            # client_str = str(client)
            # client_str = client_str[10:-3]
            ui.listWidgetOnline.addItem(client)
        # time.sleep(5)


# load_online()
# load_contacts()
# window.show()
#

    def send(self):
        text = ui.textEditEnter.toPlainText()
        ui.textEditChat.append(text)

        index = ui.tabWidgetChat.currentIndex()
        name = ui.tabWidgetChat.tabText(index)
        if name == 'All':
            print('send all')
            self.user.send_msg(text)
        else:
            self.user.send_private_msg(self.user.name, name, text)


        ui.textEditEnter.clear()


    def add_contact(self):
        contact = ui.textEditClientAppend.toPlainText()

        self.user.add_contact(contact)
        # client.create_client(contact)

        # repo.add_client(contact)
        # repo.add_contact(client.name, contact)
        ui.listWidgetContacts.addItem(contact)
        ui.textEditClientAppend.clear()


    def remove_contact(self):
        item = ui.listWidgetContacts.currentItem()
        contact_name = item.text()
        print(contact_name)
        self.user.del_contact(contact_name)

        # repo.del_contact(client.name, contact_name)
        item = ui.listWidgetContacts.takeItem(ui.listWidgetContacts.row(item))
        del item


    def remove_online(self):
        item = ui.listWidgetOnline.currentItem()
        client_name = item.text()
        print(client_name)
        self.user.remove_client_online(client_name)
        # repo.remove_client(client_name)
        item = ui.listWidgetOnline.takeItem(ui.listWidgetOnline.row(item))
        del item


    def new_tab(self):
        item = ui.listWidgetContacts.currentItem()
        contact_name = item.text()
        widget = QtWidgets.QListWidget()
        widget.setGeometry(QtCore.QRect(10, 10, 541, 411))
        ui.tabWidgetChat.addTab(widget, contact_name)

    # def new_client(self):
    #     ui.stackedWidgetNewClient.setEnabled(True)

# listener = GuiReciever()


client = ClientChat()

# load_online()
# load_contacts()
window.show()

# client.listener.gotData.connect(client.update_chat)
#
#
#
# # Используем QThread так рекомендуется, но можно и обычный
# # th_listen = threading.Thread(target=listener.poll)
# # th_listen.daemon = True
# # th_listen.start()
# th = QThread()
# client.listener.moveToThread(th)
#
# # # ---------- Важная часть - связывание сигналов и слотов ----------
# # При запуске потока будет вызван метод search_text
# th.started.connect(client.listener.poll)
# th.start()


ui.pushButton.clicked.connect(client.send)
# ui.pushButtonAddClient.clicked.connect(add_contact)
# ui.pushButtonRemove.clicked.connect(remove_contact)
ui.pushButtonOnlineRefresh.clicked.connect(client.load_online)
# ui.pushButtonOnlineRemove.clicked.connect(remove_online)
ui.pushButtonChat.clicked.connect(client.new_tab)
# ui.pushButtonNewClient.clicked.connect(client.new_client)

ui.pushButtonConnect.clicked.connect(client.connect)


sys.exit(app.exec_())