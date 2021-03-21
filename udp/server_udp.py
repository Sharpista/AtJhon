import pickle
import socket
from threading import Thread
import threading
import time
import datetime

import cpuinfo
import psutil


def listener(client, address):
    print("Accepted connection from: ", address)
    data = client.recv(4)
    if data.decode('ascii') == '0':
        arquivos = {

            "cpu_freq": psutil.cpu_freq().current,
            "cpu_cont": psutil.cpu_count(),
            "freq": psutil.cpu_count(logical=False),
            "cpu_perc": psutil.cpu_percent(percpu=True)
        }

        cpu_info = cpuinfo.get_cpu_info()

        d = [c for c in cpu_info]

        bytes_cpu = pickle.dumps(d)
        bytes_resp = pickle.dumps(arquivos)

        client.send(bytes_cpu)
        client.send(bytes_resp)
        time.sleep(2)


clients = set()
clients_lock = threading.Lock()

host = socket.gethostname()
port = 10016

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(3)
th = []

while True:
    client, address = s.accept()
    th.append(Thread(target=listener, args=(client, address)).start())

s.close()
