import socket
import time
import select
from jim import JimProtocol

serv_sock = socket.socket()
serv_sock.bind(('', 7778))
serv_sock.listen(5)
serv_sock.settimeout(0.2)


class Server():

    def __init__(self):
        self.clients = []
        self.jim = JimProtocol()
        self.clients = []
        self.who_reads = []
        self.who_writes = []
        self.e = []

    def presence_answer(self, presence_message):
        if 'action' in presence_message and \
                presence_message['action'] == 'presence':
            return {'response': 200}
        else:
            return {'response': 400, 'error': 'Не верный запрос'}


    def main_loop_in_server(self):

        while True:

            try:
                sock, addr = serv_sock.accept()

            except OSError as e:
                pass

            else:
                self.clients.append(sock)
                presence = self.jim.recive_msg(sock)
                answer = self.presence_answer(presence)
                self.jim.send_msg(sock, answer)
                print('Client with ip {}'.format(addr))

            finally:
                self.who_writes, self.who_reads, self.e = select.select(self.clients, self.clients, self.clients, 0)

                for who_write in self.who_writes:
                    try:
                        msg = who_write.recv(1024)

                        for who_read in self.who_reads:
                            try:
                                who_read.send(msg)
                            except:
                                self.clients.remove(who_read)

                        print(msg.decode())
                        message = self.jim.recive_msg(who_write)
                        print(message)

                    except:
                        self.clients.remove(who_write)


server = Server()
server.main_loop_in_server()