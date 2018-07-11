import json
import time


class JimProtocol:

    def msg_in_bytes(self, msg):
        buf = json.dumps(msg).encode()
        return buf

    def bytes_in_msg(self, bytes):
        bytes.decode()
        msg = json.loads(bytes)
        return msg

    def send_msg(self, sock, msg):
        buf = self.msg_in_bytes(msg)
        sock.send(buf)

    def recive_msg(self, sock):
        buf = sock.recv(1024)
        msg = self.bytes_in_msg(buf)
        return msg

    def create_presence(self, name):
        msg = \
            {
                'action': 'presence',
                'time': 'Client time {}'.format(time.ctime(time.time())),
                'type': 'status',
                'user': '{}'.format(name)
            }
        return msg

    def create_answer_msg(self, action, name, message):
        msg = \
            {
                'action': '{}'.format(action),
                'time': 'Client time {}'.format(time.ctime(time.time())),
                'to': 'all',
                'from': '{}'.format(name),
                'message': '{}'.format(message)
            }
        return msg

    def presence_answer(self, answer):
        msg = \
            {
                'action': 'presence',
                'answer': '{} {}'.format(time.ctime(time.time()), answer)
            }
        return msg

    def create_msg(self, name, message):
        msg = \
            {
                'action': 'msg',
                'time': 'Client time {}'.format(time.ctime(time.time())),
                'to': 'all',
                'from': name,
                'message': message
            }
        return msg

    def create_msg_to_user(self, from_name, message):
        msg = \
            {
                'action': 'msg_to_user',
                'time': 'Client time {}'.format(time.ctime(time.time())),
                'from': from_name,
                'message': message
            }
        return msg

    def join_to_chat(self, client_name, contact_name):
        msg = \
            {
                'action': 'join',
                'time': 'Client time {}'.format(time.ctime(time.time())),
                'from': '{}'.format(client_name),
                'name': '{}'.format(contact_name)
            }
        return msg

    def del_contact(self, client_name, contact_name):
        msg = \
            {
                'action': 'leave',
                'time': 'Client time {}'.format(time.ctime(time.time())),
                'client': '{}'.format(client_name),
                'contact': '{}'.format(contact_name)
            }
        return msg

    def remove_client(self, client_name):
        msg = \
            {
                'action': 'remove',
                'time': 'Client time {}'.format(time.ctime(time.time())),
                'client': '{}'.format(client_name)
            }
        return msg

    def new_client(self, client_name):
        msg = \
            {
                'action': 'create',
                'time': 'Client time {}'.format(time.ctime(time.time())),
                'client': '{}'.format(client_name)
            }
        return msg

    def get_clients(self):
        msg = \
            {
                'action': 'getClients',
                'time': 'Client time {}'.format(time.ctime(time.time()))
            }
        return msg

    def set_clients(self, clients):
        msg = \
            {
                'action': 'setClients',
                'time': 'Client time {}'.format(time.ctime(time.time())),
                'clients': clients
            }
        return msg

    def get_contacts(self, client_name):
        msg = \
            {
                'action': 'getContacts',
                'time': 'Client time {}'.format(time.ctime(time.time())),
                'client_name': '{}'.format(client_name)
            }
        print('jim1')
        return msg

    def set_contacts(self, client_name, contacts):
        msg = \
            {
                'action': 'setContacts',
                'time': 'Client time {}'.format(time.ctime(time.time())),
                'to': '{}'.format(client_name),
                'contacts': contacts
            }
        print('jim2')
        return msg

    def msg_private(self, from_name, to_name, message):
        msg = \
            {
                'action': 'msg_to_user',
                'time': 'Client time {}'.format(time.ctime(time.time())),
                'to': to_name,
                'from': from_name,
                'message': message
            }
        return msg