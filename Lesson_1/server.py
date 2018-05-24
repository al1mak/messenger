
import socket
import time
from lib import Server

serv_sock = socket.socket()
serv_sock.bind(('', 7777))
serv_sock.listen(5)

sock, address = serv_sock.accept()
print('Client with ip {}\n'
      '{}'. format(address, time.ctime(time.time())))
serv = Server(sock)
serv.main_loop_for_server()
