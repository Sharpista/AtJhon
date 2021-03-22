import pickle
import platform
import socket
import threading
import time
from threading import Thread
import psutil


def listener(client, address):
    print("Accepted connection from: ", address)
    while True:

        data_client = client.recv(4)

        if data_client.decode('ascii') == '0':
            resp = {
                "mem": psutil.virtual_memory(),
                "cpu_percent": psutil.cpu_percent(interval=0),
                "disk": psutil.disk_usage('/'),
                "plataform": platform.processor()
            }
            resp_bytes = pickle.dumps(resp)
            client.send(resp_bytes)
            time.sleep(1)


clients = set()
clients_lock = threading.Lock()

host = socket.gethostname()
port = 9999

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen()
th = []

while True:
    client, address = s.accept()

    th.append(Thread(target=listener, args=(client, address)).start())

s.close()
