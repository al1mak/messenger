import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtWidgets, uic, QtCore
import py_form
from db.db import session
from db.db_lib import Storage
from client import Client
from threading import Thread
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal, pyqtSlot
from chat_form import Ui_ChatForm
import socket



# ___________________________________________________________________




# ___________________________________________________________________



app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()
ui = py_form.Ui_MainWindow()
ui.setupUi(window)
repo = Storage(session)

# user = Client(name='Kolya')
# user.connect_to_server()


# ___________________________________________________________________

# class ReceiveHandler(QObject):
#     ''' Обработчик входящего сетевого соединения
#     '''
#     gotData = pyqtSignal(str)
#     finished = pyqtSignal(int)
#
#     def __init__(self, sock):
#         super().__init__()
#         self.sock = sock
#         self.is_active = False
#         print(sock)
#
#     def poll(self):
#         self.is_active = True
#         print('33')
#         while True:
#             if not self.is_active:
#                 print('2332')
#                 break
#             # Обратите внимание - отключение не сработает сразу,
#             # т.к. поток будет ждать данных в функции recv.
#             print('22')
#             data = self.sock.recv(1024).decode('utf-8')
#
#             # Чтобы поток не ожидал получение данных из сокета,
#             # нужно настроить таймаут приёма данных
#
#             if data:
#                 print('33')
#                 self.gotData.emit(' >> ' + data)
#             else:
#                 print('33')
#                 break
#         print('33')
#         self.finished.emit(0)
#
#     def stop(self):
#         print('3')
#         self.is_active = False



# class ChatDialog(QtWidgets.QDialog):
#     ''' Класс GUI-формы "Чата"
#     '''
#     sentData = pyqtSignal(str)
#
#     def __init__(self, parent=None, ip='localhost', port=7777):
#         QtWidgets.QDialog.__init__(self, parent)
#         self.ui = Ui_ChatForm()
#         self.ui.setupUi(self)
#         self.ui.connectButton.clicked.connect(self.start_chat)
#         self.ui.disconnectButton.clicked.connect(self.finished)
#
#         self.receiver = None
#         self.thread = None
#         self.sock = None
#         self.ip = ip
#         self.port = port
#         self.is_active = False
#
#     @pyqtSlot(str)
#     def update_chat(self, data):
#         ''' Отображение сообщения в истории
#         '''
#         msg = str(time.ctime()) + data
#         # self.ui.historyList.addItem(msg)
#         ui.textEditChat.append(msg)
#
#
#     def stop_chat(self):
#         ''' Остановка входящих соединений '''
#         if self.receiver is not None:
#             self.is_active = False
#             self.receiver.stop()
#
#     def finished(self):
#         ''' Действия при отключении
#         '''
#         self.is_active = False
#         self.receiver.stop()
#         self.sock.close()
#         self.setGuiConnected(False)
#
#     def setGuiConnected(self, enabled):
#         ''' Настройка GUI при подключении/отключении
#         '''
#         self.ui.historyList.setEnabled(enabled)
#         self.ui.newMsgText.setEnabled(enabled)
#         self.ui.sendButton.setEnabled(enabled)
#         self.ui.clearTextButton.setEnabled(enabled)
#         self.ui.connectButton.setEnabled(not enabled)
#         self.ui.disconnectButton.setEnabled(enabled)
#
#     def send_message(self):
#         ''' Добавление сообщений в "историю"
#         '''
#         data = self.ui.newMsgText.toPlainText()
#         self.sock.sendall(data.encode('utf-8'))
#         self.sentData.emit(' << ' + data)
#
#     def start_chat(self):
#         ''' Запуск чата
#         '''
#         if not self.is_active:
#             self.is_active = True
#             self.setGuiConnected(True)
#
#             # self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             # self.sock.connect((self.ip, self.port))
#
#             self.sock = client.sock
#
#             self.receiver = ReceiveHandler(self.sock)
#             self.receiver.gotData.connect(self.update_chat)
#             self.sentData.connect(self.update_chat)
#
#             # Создание потока и помещение объекта-монитора в этот поток
#             self.thread = QThread()
#             self.receiver.moveToThread(self.thread)
#
#             # ---------- Важная часть - связывание сигналов и слотов ----------
#             # При запуске потока будет вызван метод search_text
#             self.thread.started.connect(self.receiver.poll)
#
#             # При завершении поиска необходимо завершить поток и изменить GUI
#             self.receiver.finished.connect(self.thread.quit)
#             self.receiver.finished.connect(self.finished)
#
#             # Завершение процесса поиска по кнопке "Остановить"
#             self.ui.sendButton.clicked.connect(self.send_message)
#
#             # Запуск потока, который запустит self.monitor.search_text
#             self.thread.start()
# class ChatDialog(QtWidgets.QDialog):
#     ''' Класс GUI-формы "Чата"
#     '''
#     @pyqtSlot(str)
#     def update_chat(self, data):
#         msg = str(time.ctime()) + data
#         ui.textEditChat.append(msg)
#         # self.ui.historyList.addItem(msg)
#
# # sock = socket.socket()
# # sock.connect(('', 7777))
# sock = client.sock
# chat = ChatDialog()
# receiver = ReceiveHandler(sock)
# receiver.gotData.connect(chat.update_chat)
# # sentData.connect(self.update_chat)
#
#             # Создание потока и помещение объекта-монитора в этот поток
# thread = QThread()
# receiver.moveToThread(thread)
#
#             # ---------- Важная часть - связывание сигналов и слотов ----------
#             # При запуске потока будет вызван метод search_text
# thread.started.connect(receiver.poll)


# ___________________________________________________________________

class ClientChat:

    def __init__(self):
        self.set_gui_connected(False)

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
            self.user.connect_to_server()
            self.set_gui_connected(True)
            self.load_online()
            self.load_contacts()

    def set_gui_connected(self, enebled):
        ui.pushButton.setEnabled(enebled)
        ui.pushButtonRemove.setEnabled(enebled)
        ui.pushButtonOnlineRefresh.setEnabled(enebled)
        ui.pushButtonOnlineRemove.setEnabled(enebled)
        ui.pushButtonChat.setEnabled(enebled)
        ui.pushButtonConnect.setEnabled(not enebled)


    def load_contacts(self):
        contacts = repo.get_contacts(self.user.name)
        ui.listWidgetContacts.clear()
        for contact in contacts:
            contact_str = str(contact)
            contact_str = contact_str[10:-3]
            ui.listWidgetContacts.addItem(contact_str)


    def load_online(self):
        # clients = repo.get_clients()
        self.user.get_clients()
        clients = self.user.clients_online
        print(type(clients))
        ui.listWidgetOnline.clear()
        for client in clients:
            # client_str = str(client)
            # client_str = client_str[10:-3]
            ui.listWidgetOnline.addItem(client)


# load_online()
# load_contacts()
# window.show()
#

    def send(self):
        text = ui.textEditEnter.toPlainText()
        ui.textEditChat.append(text)
        self.user.send_msg(text)
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


client = ClientChat()

# load_online()
# load_contacts()
window.show()




# ui.pushButton.clicked.connect(send)
# ui.pushButtonAddClient.clicked.connect(add_contact)
# ui.pushButtonRemove.clicked.connect(remove_contact)
ui.pushButtonOnlineRefresh.clicked.connect(client.load_online)
# ui.pushButtonOnlineRemove.clicked.connect(remove_online)
# ui.pushButtonChat.clicked.connect(new_tab)
ui.pushButtonConnect.clicked.connect(client.connect)


sys.exit(app.exec_())