import copy
import select
import socket
import time

data = {}


def start_server(host):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(False)
    server.bind(host)
    server.listen(100)
    return server


for i in range(10):
    data[i] = {'port': 10000 + i}
    server = start_server(('localhost', 10000 + i))
    data[i]['sock'] = server

socks = [data[i]['sock'] for i in data]
inputs, outputs, exceptions = copy.copy(socks), [], []

while True:
    c = time.time()
    readers, writers, exceptable = select.select(inputs, outputs, exceptions, 1)
    for s in readers:
        if s in socks:
            connection, client_address = s.accept()
            connection.setblocking(0)
            inputs.append(connection)
            outputs.append(connection)
        else:
            try:
                data = s.recv(1024)
                if data:
                    if s not in outputs:
                        outputs.append(s)
                else:
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close()
            except socket.error:
                print(s)
                inputs.remove(s)
                if s in outputs:
                    outputs.remove(s)
    for s in writers:
        pass
    if exceptable:
        break
    for s in exceptable:

        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        addr = s.getpeername()
        s.close()
        s = start_server(addr)
        inputs.append(s)
