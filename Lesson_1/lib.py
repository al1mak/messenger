import time
import json


class Server:

    def __init__(self, sock):
        self.sock = sock

    def main_loop_for_server(self):

        while True:
            self.receive_msg()

    def message_processing(self, client_msg):

        if client_msg.get('action') == 'presence':
            answer = self.answer_to_client(1)
            self.send_msg(answer)

    def send_msg(self, msg):

        self.sock.send(json.dumps(msg).encode())

    def receive_msg(self):

        result_buf = self.sock.recv(1024)
        result = json.loads(result_buf.decode())
        self.message_processing(result)
        return result

    def answer_to_client(self, param):

        if param == 1:
            return '200 - OK'


class Client:

    def __init__(self, sock):
        self.sock = sock

    def main_loop_for_client(self):
        self.request()

        while True:
            result_buf = self.sock.recv(1024)
            result = json.loads(result_buf.decode())
            print(result)

    def request(self):
        req = \
            {
                'action': 'presence',
                'time': 'Client time {}'.format(time.ctime(time.time())),
                'type': 'status',
                'user': {
                    'account_name': 'Max',
                    'status': 'Yep, I am here!'
                }
            }

        req_buf = json.dumps(req).encode()
        self.sock.send(req_buf)

