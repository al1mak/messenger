
import socket
from jim import JimProtocol


sock = socket.socket()
sock.connect(('', 7778))


class ClientWrite:

    def __init__(self, sock, name):
        self.jim = JimProtocol()
        self.name = name
        self.sock = sock

    def send_presence(self, name):
        presence = self.jim.create_presence(name)
        self.jim.send_msg(self.sock, presence)
        self.main_loop_in_client()

    def main_loop_in_client(self):
        while True:
            msg = input('Введите текст: ')
            json_msg = self.jim.create_msg(self.name, msg)
            self.jim.send_msg(sock, json_msg)


client = ClientWrite(sock, 'Dima')
client.send_presence('Dima')