

import socket


sock = socket.socket()
sock.connect(('', 7778))

while True:
    buf = sock.recv(1024)
    msg = buf.decode()

    print(msg)