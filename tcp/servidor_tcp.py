import pickle
import socket, os

import psutil
from cpuinfo import cpuinfo

import socket, os

# Cria o socket
socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Obtem o nome da máquina
host = socket.gethostname()
porta = 9999
socket_servidor.bind((host, porta))
socket_servidor.listen()

(socket_cliente, addr) = socket_servidor.accept()

print("Conectado a:", str(addr))

while True:

    msg = socket_cliente.recv(4)

    if msg.decode('ascii') == 'fim':
        break
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

    socket_cliente.send(bytes_cpu)
    socket_cliente.send(bytes_resp)


socket_cliente.close()
socket_servidor.close()
