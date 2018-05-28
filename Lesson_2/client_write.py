
import socket


sock = socket.socket()
sock.connect(('', 7778))

while True:
    msg = input('Введите текст: ')
    sock.send(msg.encode())