
import socket
from jim import JimProtocol


# sock = socket.socket()
# sock.connect(('', 7778))



class ClientRead:

    def __init__(self, name):
        self.jim = JimProtocol()
        self.name = name
        #self.sock = sock

    def connect_to_server(self):
        self.sock = socket.socket()
        self.sock.connect(('', 7778))
        self.send_presence(self.name)

    def send_presence(self, name):
        presence = self.jim.create_presence(name)
        self.jim.send_msg(self.sock, presence)
        self.main_loop_in_client()

    def main_loop_in_client(self):

        while True:
            buf = self.sock.recv(1024)
            msg = buf.decode()

            print(msg)


# client = ClientRead(sock, 'Vasya')
# client.send_presence('Vasya')
