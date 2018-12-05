import select
import socket
import time

data = {}


def start_server(host):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(False)
    server.bind(host)
    server.listen()
    return server


def start_client(host):
    try:
        client = socket.socket()
        client.settimeout(0.00000000000000000001)
        # client.setblocking(False)
        client.connect(host)
        return client
    except socket.error as err:
        print(err)
        return None


def start_host_internal(host):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(False)
    server.bind(host)
    server.listen(1)
    connection, client_address = soc.accept()
    connection.setblocking(0)
    return connection


client_ports = list(range(10000, 10010, 1))
ports = list(range(20000, 20010, 1))


client_ports = ports


def generate_servers(ports):
    servers = {}
    for p in ports:
        server = start_server(('127.0.0.1', p))
        servers[server.fileno()] = server
    return servers


server_list = generate_servers(ports)
inputs = list(server_list.values())
outputs = []
clients = []
running_client_ports = []
socket.socket()
while True:
    c = time.time()
    for client_p in client_ports:
        if client_p not in running_client_ports:
            client = start_client(('127.0.0.1', client_p))
            if client:
                clients.append(client.fileno())
                running_client_ports.append(client_p)

                inputs.append(client)
                outputs.append(client)
    # print(time.time() - c)
    print(clients)
    r, w, e = select.select(inputs, outputs, inputs, 1)
    for soc in r:
        if soc in server_list.values():
            connection, client_address = soc.accept()
            connection.setblocking(0)
            inputs.append(connection)
        else:
            try:
                data = soc.recv(1024)
                if data:
                    if soc not in outputs:
                        outputs.append(soc)
                else:

                    if soc in outputs:
                        outputs.remove(soc)
                    if soc.getpeername()[1] in running_client_ports:
                        running_client_ports.remove(soc.getpeername()[1])
                        clients.remove(soc)
                    inputs.remove(soc)
                    soc.close()
            except socket.error as err:
                print(err)
                if soc in outputs:
                    outputs.remove(soc)
                inputs.remove(soc)
                print(soc.getsockname())
                print(soc.fileno(), ' dead')
    for s in w:
        try:
            s.send(b'zdarova')
        except socket.error:
            if s in outputs:
                outputs.remove(s)
            if s in inputs:
                inputs.remove(s)
            if s.getpeername()[1] in running_client_ports:
                running_client_ports.remove(s.getsockname()[1])
                clients.remove(s)

    for s in e:
        # Stop listening for input on the connection
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        if s.getpeername()[1] in running_client_ports:
            running_client_ports.remove(s.getpeername()[1])
            clients.remove(s)
        s.close()
