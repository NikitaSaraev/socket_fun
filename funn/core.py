import select
import socket

data = {}


def start_server(host):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(False)
    server.bind(host)
    server.listen()
    return server


def start_client(host):
    client = socket.socket()
    try:
        client.connect(host)
        return client
    except socket.error:
        return None


ports = list(range(10000, 10010, 1))


def generate_servers(ports):
    servers = {}
    for p in ports:
        server = start_server(('127.0.0.1', p))
        servers[server.fileno()] = server
    return servers


server_list = generate_servers(ports)
inputs = list(server_list.values())
outputs = []

while True:

    r, w, e = select.select(inputs, outputs, inputs, 1)
    for soc in r:
        if soc in server_list.values():
            connection, client_address = soc.accept()
            connection.setblocking(0)
            inputs.append(connection)
        else:
            data = soc.recv(1024)
            if data:
                if soc not in outputs:
                    outputs.append(soc)
            else:
                if soc in outputs:
                    outputs.remove(soc)
                inputs.remove(soc)
                soc.close()
    for s in w:
        print(s.fileno())
    # Handle "exceptional conditions"
    for s in e:
        # Stop listening for input on the connection
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
