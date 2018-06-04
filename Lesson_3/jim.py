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

    def create_msg(self, name, message):
        msg = \
            {
                'action': 'msg',
                'time': 'Client time {}'.format(time.ctime(time.time())),
                'to': 'all',
                'from': '{}'.format(name),
                'message': '{}'.format(message)
            }
        return msg
