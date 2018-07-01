import socket
from jim import JimProtocol
from threading import Thread
import time


class Client:

    def __init__(self, name):
        self.jim = JimProtocol()
        self.name = name
        self.clients_online = []
        # self.client_chat = ClientChat()
        #self.sock = sock

    def action(self, msg):
        if 'action' in msg and \
                msg['action'] == 'msg':
            msg = '{} {} send message to all: {}'\
                .format(time.ctime(), msg.get('from'), msg.get('message'))
            # print(msg)
            return msg
        elif 'action' in msg and \
                msg['action'] == 'presence':
            msg = 'console', msg
            return msg
        elif 'action' in msg and \
                msg['action'] == 'setClients':
            clients = msg.get('clients')

            # clients = clients.split(',')
            print(type(clients), clients)
            self.clients_online = clients
            list = clients.split(' ')
            self.clients_online = list
            return list

    def connect_to_server(self):
        self.sock = socket.socket()
        self.sock.connect(('', 7778))
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
            # buf = self.sock.recv(1024)
            # msg = buf.decode()
            msg = self.jim.recive_msg(self.sock)
            msg = self.action(msg)
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

    def get_contact(self):
        msg = self.jim.get_contact(self.name)
        self.jim.send_msg(self.sock, msg)





# client = Client(name='Kolya')
# client.connect_to_server()