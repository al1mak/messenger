
import socket
from jim import JimProtocol


sock = socket.socket()
sock.connect(('', 7778))



class ClientRead:

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
            buf = sock.recv(1024)
            msg = buf.decode()

            print(msg)


client = ClientRead(sock, 'Vasya')
client.send_presence('Vasya')

# jim = JimProtocol()
#
# presence = jim.create_presence('Vasya')
# jim.send_msg(sock, presence)
#
#
# while True:
#     buf = sock.recv(1024)
#     msg = buf.decode()
#
#     print(msg)