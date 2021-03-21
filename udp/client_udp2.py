import pickle

import socket

s = socket.socket()
host = socket.gethostname()
port = 10016

s.connect((host, port))
while True:
    msg = '0'
    s.send(msg.encode('ascii'))
    r = s.recv(1024)
    p = pickle.loads(r)
    print(p)
