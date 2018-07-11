from jim import JimProtocol
import time
from PyQt5.QtCore import QObject, pyqtSignal

class Receiver:

    def __init__(self, sock, request_queue):
        self.request_queue = request_queue
        self.sock = sock
        self.is_alive = False
        self.jim = JimProtocol()

    def poll(self):

        self.is_alive = True
        while True:
            if not self.is_alive:
                break
            msg = self.jim.recive_msg(self.sock)
            try:
                if 'action' in msg and \
                        msg['action'] == 'msg':
                    msg = '{} {} send message to all: {}' \
                        .format(time.ctime(), msg.get('from'), msg.get('message'))
                    return msg
                elif 'action' in msg and \
                        msg['action'] == 'presence':
                    msg = 'console', msg
                    return msg
                elif 'action' in msg and \
                        msg['action'] == 'setClients':
                    clients = msg.get('clients')
                    self.request_queue.put(clients)
                elif 'action' in msg and \
                        msg['action'] == 'setContacts':
                    contacts = msg.get('contacts')
                    self.request_queue.put(contacts)
                elif 'action' in msg and \
                        msg['action'] == 'msg_to_user':
                    from_name = msg.get('from')
                    message = msg.get('message')
                    msg = '{}: {}'.format(from_name, message)
                    return msg
            except Exception as e:
                print(e)

class GuiReciever(Receiver, QObject):
    """GUI обработчик входящих сообщений"""
    # мы его наследуюем от QObject чтобы работала модель сигнал слот
    # можно и не наследовать, но тогда надо передавать объект в который мы будем сообщения выводить
    # через сигнал слот более гибко т.к. мы можем обработать сигнал как хотим уже внутри gui
    # событий (сигнал) что пришли данные
    gotData = pyqtSignal(str)
    # событие (сигнал) что прием окончен
    finished = pyqtSignal(int)

    def __init__(self, sock, request_queue):
        # инициализируем как Receiver
        Receiver.__init__(self, sock, request_queue)
        # инициализируем как QObject
        QObject.__init__(self)

    def process_message(self, message):
        """Обработка сообщения"""
        # Генерируем сигнал (сообщаем, что произошло событие)
        # В скобках передаем нужные нам данные
        # text = '{} >>> {}'.format(message.from_, message.message)
        print(message)
        self.gotData.emit(message)

    def poll(self):
        super().poll()
        # Когда обработка событий закончиться сообщаем об этом генерируем сигнал finished
        self.finished.emit(0)