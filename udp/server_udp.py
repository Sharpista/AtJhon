import os
import pickle
import socket
import threading
import time
from threading import Thread
import cpuinfo
import psutil


def dados_dir():
    lista = os.listdir()
    lista_arq = []  # lista para guardar os arquivos
    lista_dir = []  # lista para guardar os diretórios
    for i in lista:
        if os.path.isfile(i):
            lista_arq.append(i)
        else:
            lista_dir.append(i)

    # Checa se tem arquivo na lista
    if len(lista_arq) > 0:
        for i in lista_arq:
            return "Arquivos:" + "\t" + i  # insere uma tabulação no início

    # Checa se tem diretório na lista
    if len(lista_dir) > 0:
        for i in lista_dir:
            return "Diretorios:" + "\t" + i  # insere uma tabulação no início


def dados_pid():
    processos = []
    for proc in psutil.process_iter():
        p = {
            "Nº PID": proc.pid,
            "Nome": proc.name(),
        }
        processos.append(p)

    return processos


def listener(client, address):
    print("Accepted connection from: ", address)
    while True:

        data_client1 = client.recv(4)

        if data_client1.decode('ascii') == '0':
            arquivos = [

                psutil.cpu_freq().current,
                psutil.cpu_count(),
                psutil.cpu_count(logical=False),
                psutil.cpu_percent(percpu=True),

            ]

            cpu_info = cpuinfo.get_cpu_info()

            pids = list(filter(lambda x: x['Nome'] != "" or None, dados_pid())),

            outros = {
                "ip_servidor": socket.gethostbyname(socket.gethostname()),
                "diretorios": dados_dir(),
            }

            bytes_cpu = pickle.dumps(cpu_info)
            bytes_resp = pickle.dumps(arquivos)
            byte_pids = pickle.dumps(pids)
            byte_outros = pickle.dumps(outros)

            client.send(bytes_cpu)
            client.send(bytes_resp)
            client.send(byte_pids)
            client.send(byte_outros)
            time.sleep(1)


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
