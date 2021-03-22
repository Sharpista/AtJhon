import pickle
import socket


def imprime(l):
    print(f"""
        PIDS:{l['pids']}
        IP: {l['ip_servidor']}
        INTERFACES: {l['interfaces']}
        DIRETORIOS: {l['diretorios']}
        MÁQUINAS: {l['maquinas_sub']}
    """)


HOST = socket.gethostname()
PORT = 5000

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest = (HOST, PORT)

udp.sendto(b'', dest)

(pacote, remetente) = udp.recvfrom(20000)

dicionario = pickle.loads(pacote)

imprime(dicionario)

udp.close()
