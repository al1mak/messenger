
import time
import socket
from lib import Client

sock = socket.socket()
sock.connect(('127.0.0.1', 7777))

client = Client(sock)
client.main_loop_for_client()