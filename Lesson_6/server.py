import socket
import time
import select
from jim import JimProtocol
from db.db_lib import Storage
from db.db import session

# repo = Storage(session)

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
        self.repo = Storage(session)
        self.from_name = ''
        self.user_and_sock = {}

    def action(self, msg):
        if 'action' in msg and \
                msg['action'] == 'msg':
            print(msg)
            print('msg')
            # name = msg.get('from')
            # message = msg.get('message')
            answer_msg = '{} {} send message to all: {}'\
                .format(time.ctime(), msg.get('from'), msg.get('message'))
            self.from_name = msg.get('from')
            return msg
        elif 'action' in msg and msg['action'] == 'join':
            client_name = msg.get('from')
            contact_name = msg.get('name')
            self.repo.add_contact(client_name, contact_name)
            print('user: {} add to {}'.format(client_name, contact_name))
            return None
        elif 'action' in msg and msg['action'] == 'leave':
            client_name = msg.get('client')
            contact_name = msg.get('contact')
            self.repo.del_contact(client_name, contact_name)
            print('client: {} del {} from friend list'.format(client_name, contact_name))
            return None
        elif 'action' in msg and msg['action'] == 'remove':
            client_name = msg.get('client')
            self.repo.remove_client(client_name)
            print('{} is removed'.format(client_name))
            return None
        elif 'action' in msg and msg['action'] == 'create':
            client_name = msg.get('client')
            self.repo.add_client(client_name)
            print('New client: {}!'.format(client_name))
            return None
        elif 'action' in msg and msg['action'] == 'getClients':
            # clients = self.user_and_sock.keys()
            # print(type(clients))
            # clients = self.repo.get_clients()
            # clients_array = []
            # for client in clients:
            #     client_str = str(client)
            #     client_str.join()
            #     client_str = client_str[10:-3]
            #     clients_array.append(client_str)
            # msg = self.jim.set_clients(clients)
            str = ' '.join(self.clients)
            print(str)
            msg = self.jim.set_clients(str)
            return msg
            # return clients_array
        elif 'action' in msg and msg['action'] == 'getContacts':
            contact = self.repo.get_contacts(msg.get('client_name'))
            print(contact)
        elif 'action' in msg and msg['action'] == 'msg_to_user':
            pass
        else:
            return None

    def reads_msg(self, w_clients, all_clients):
        for sock in w_clients:
            try:
                jmsg = self.jim.recive_msg(sock)
                msg = self.action(jmsg)
                print('1')
                if msg is not None:
                    self.write_clients(msg, self.who_reads, self.clients)
            except:
                sock.cloce()
                all_clients.remove(sock)

    def write_clients(self, msgs, r_clients, all_clients):
        for sock in r_clients:
            try:
                print('3')
                msg = self.jim.create_answer_msg('msg', self.from_name, msgs)
                self.jim.send_msg(sock, msgs)
                print(msgs)
            except:
                sock.cloce()
                all_clients.remove(sock)
            # for msg in msgs:
            #     try:
            #         self.jim.send_msg(sock, msg)
            #         print(msg)
            #     except:
            #         sock.cloce()
            #         all_clients.remove(sock)

    def presence_answer(self, presence_message):
        if 'action' in presence_message and \
                presence_message['action'] == 'presence':
            answer = self.jim.presence_answer({'response': 200})
            return answer
        else:
            answer = self.jim.presence_answer({'response': 400, 'error': 'Не верный запрос'})
            return answer


    def main_loop_in_server(self):
        while True:
            try:
                sock, addr = serv_sock.accept()
                presence = self.jim.recive_msg(sock)
                self.repo.add_client(presence.get('user'))
                self.user_and_sock[presence.get('user')] = sock
                self.clients.append(presence.get('user'))
                print(self.user_and_sock)
                answer = self.presence_answer(presence)
                self.jim.send_msg(sock, answer)
            except OSError as e:
                pass
            else:
                # self.clients.append(sock)
                # presence = self.jim.recive_msg(sock)
                # # #print(presence.get('user'))
                # repo.add_client(presence.get('user'))
                # answer = self.presence_answer(presence)
                # self.jim.send_msg(sock, answer)
                print('Client with ip {}'.format(addr))
            finally:
                # wait = 0
                # self.who_writes = []
                # self.who_reads = []
                try:
                    self.who_writes, \
                    self.who_reads,\
                    self.e = \
                        select.select(self.user_and_sock.values(),
                                      self.user_and_sock.values(),
                                      self.user_and_sock.values(), 0)
                    self.reads_msg(self.who_writes, self.clients)
                    # self.write_clients(msg, self.who_reads, self.clients)
                except:
                    pass


server = Server()
server.main_loop_in_server()