import pickle

import pygame
import psutil
import socket
import platform

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((socket.gethostname(), 9999))
msg = input('msg: ')
s.send(msg.encode('ascii'))

bytes = s.recv(4096)
arq = s.recv(4096)

cpu_info = pickle.loads(bytes)
arquivo = pickle.loads(arq)

if msg == 'fim':
    s.send(msg.encode('ascii'))




s.close()
