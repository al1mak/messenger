import socket
from jim import JimProtocol
from threading import Thread
import time
from queue import Queue
from reseiver import Receiver


class Client:

    def __init__(self, name):
        self.jim = JimProtocol()
        self.name = name
        self.request_queue = Queue()
        # self.receiver = Receiver(self.sock, self.request_queue)

    # def action(self, msg):
    #     if 'action' in msg and \
    #             msg['action'] == 'msg':
    #         msg = '{} {} send message to all: {}'\
    #             .format(time.ctime(), msg.get('from'), msg.get('message'))
    #         return msg
    #     elif 'action' in msg and \
    #             msg['action'] == 'presence':
    #         msg = 'console', msg
    #         return msg
    #     elif 'action' in msg and \
    #             msg['action'] == 'setClients':
    #         clients = msg.get('clients')
    #         self.request_queue.put(clients)
    #     elif 'action' in msg and \
    #             msg['action'] == 'setContacts':
    #         contacts = msg.get('contacts')
    #         self.request_queue.put(contacts)
    #     elif 'action' in msg and \
    #             msg['action'] == 'msg_to_user':
    #         from_name = msg.get('from')
    #         message = msg.get('message')
    #         msg = '{}: {}'.format(from_name, message)
    #         return msg

    def connect_to_server(self, addr, port):
        self.sock = socket.socket()
        self.sock.connect((addr, port))
        self.receiver = Receiver(self.sock, self.request_queue)
        self.send_presence(self.name)

    def send_presence(self, name):
        presence = self.jim.create_presence(name)
        self.jim.send_msg(self.sock, presence)
        t = Thread(target=self.read_loop)
        t.daemon = True
        t.start()

    def send_msg(self, msg):
        json_msg = self.jim.create_msg(self.name, msg)
        self.jim.send_msg(self.sock, json_msg)

    def read_loop(self):
        while True:
            msg = self.receiver.poll()
            # msg = self.jim.recive_msg(self.sock)
            # msg = self.action(msg)
            print(msg)

    def add_contact(self, client_name):
        msg = self.jim.join_to_chat(self.name, client_name)
        self.jim.send_msg(self.sock, msg)

    def del_contact(self, client_name):
        msg = self.jim.del_contact(self.name, client_name)
        self.jim.send_msg(self.sock, msg)

    def remove_client_online(self, client_name):
        msg = self.jim.remove_client(client_name)
        self.jim.send_msg(self.sock, msg)

    def create_client(self, client_name):
        msg = self.jim.new_client(client_name)
        self.jim.send_msg(self.sock, msg)

    def get_clients(self):
        msg = self.jim.get_clients()
        self.jim.send_msg(self.sock, msg)
        msg = self.request_queue.get()
        return msg

    def get_contacts(self, name):
        msg = self.jim.get_contacts(name)
        self.jim.send_msg(self.sock, msg)
        msg = self.request_queue.get()
        return msg

    def send_private_msg(self, from_name, to_name, message):
        msg = self.jim.msg_private(from_name, to_name, message)
        self.jim.send_msg(self.sock, msg)



