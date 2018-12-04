import select
import socket


def start_client(host):
    sock = socket.socket()
    sock.connect(host)
    return sock


data = {}
for i in range(10):
    data[i] = {'port': 10000 + i}
    # server = start_server(('localhost', 10000 + i))
    # data[i]['sock'] = server
inputs, outputs, excepts = [], [], []
while True:
    for d in data:
        try:
            if not data[d].get('sock'):
                data[d]['sock'] = start_client(('127.0.0.1', data[d]['port']))
        except:
            pass
    inputs = [data[s]['sock'] for s in data if data[s].get('sock')]
    readers, writers, exceptable = select.select(inputs, inputs, excepts, 1)
    print(excepts)
    for s in readers:
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
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            for d in data:
                if data[d] == s:
                    data[d] = None
            print('restarting socket {}'.format(s))
            s.close()
    for s in writers:
        s.send(b';((')
    if exceptable:
        break
    for s in exceptable:
        pass
