import socket
import time
import select


serv_sock = socket.socket()
serv_sock.bind(('', 7777))
serv_sock.listen(5)
serv_sock.settimeout(0.2)

clients = []

while True:
    try:
        sock, addr = serv_sock.accept()

    except OSError as e:
        pass

    else:
        clients.append(sock)
        print('Client with ip {}'.format(addr))

    finally:
        who_reads = []
        who_writes = []
        e = []
        who_writes, who_reads, e = select.select(clients, clients, clients, 0)

        for who_write in who_writes:
            try:
                msg = who_write.recv(1024)

                for who_read in who_reads:
                    try:
                        who_read.send(msg)
                    except:
                        clients.remove(who_read)

                print(msg.decode())

            except: clients.remove(who_write)