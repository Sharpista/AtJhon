# import psutil
import os
from os.path import join
from time import time

import pygame, sys, platform, psutil
import pygame.display

# Inicialização Pygame
pygame.init()
pygame.font.init()

# Define e mostra a tela


largura_tela = 1376
altura_tela = 800


tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.init()

# Título da Tela e ciclo de atualização da tela
pygame.display.set_caption("Gerenciador de tarefas.")
clock = pygame.time.Clock()
count = 60

# Configuração do tamanho da fonte a ser usada
font = pygame.font.Font(None, 32)

# Definições de superfícies das barras
s1 = pygame.surface.Surface((largura_tela, altura_tela / 5))
s2 = pygame.surface.Surface((largura_tela, altura_tela / 5))
s3 = pygame.surface.Surface((largura_tela, altura_tela / 5))
s4 = pygame.surface.Surface((largura_tela, altura_tela / 5))
s5 = pygame.surface.Surface((largura_tela, altura_tela / 5))

# Definição de cores utilizadas na tela
cordofundo = (0, 0, 0)
cordabarra = (0, 0, 255)
cordoindice = (255, 0, 0)
cordafonte = (255, 255, 255)

def getDiretorio():
    try:
        diretorio = input("Entre com o caminho do diretório : ")
        arquivos = [f for f in os.listdir(diretorio)]
        arq = []
        for i in arquivos:
            tipo = i , extension = os.path.splitext(diretorio)
            obj = {
                "Nome Arquivo": i,
                "Tamanho":os.path.getsize(join(diretorio, i)),
                "Diretório": join(diretorio, i),
                "Data de criação": time.ctime(os.path.getmtime(i)),
                "Data de Modificação": time.ctime(os.path.getctime(i)),
                "Tipo": tipo
            }
            arq.append(obj)

        return [m for m in arq]

    except Exception as erro:
        print(str(erro))




def mostraMem():
    mem = psutil.virtual_memory()
    return mem


def mostraCPU():
    cpu = psutil.cpu_percent(interval=0)
    return cpu


def mostraDisco():
    disco = psutil.disk_usage('.')
    return disco


def desenha_barra_mem():
    mem = psutil.virtual_memory()
    larg = largura_tela - 2 * 20
    s1.fill(cordofundo)
    pygame.draw.rect(s1, cordabarra, (20, 50, larg, 70))
    tela.blit(s1, (0, 0))
    larg = larg * mem.percent / 100
    pygame.draw.rect(s1, cordoindice, (20, 50, larg, 70))
    tela.blit(s1, (0, 0))
    total = round(mem.total / (1024 * 1024 * 1024), 2)
    texto_barra = "Uso de Memória (Total: " + str(total) + "GB) (Utilizando: " + str(mem.percent) + " %):"
    text = font.render(texto_barra, 1, cordafonte)
    tela.blit(text, (20, 10))


def desenha_barra_cpu():
    cpu = mostraCPU()
    largura = largura_tela - 2 * 20
    s2.fill(cordofundo)
    pygame.draw.rect(s2, cordabarra, (20, 50, largura, 70))
    tela.blit(s2, (0, altura_tela / 4))
    largura = largura * cpu / 100
    pygame.draw.rect(s2, cordoindice, (20, 50, largura, 70))
    tela.blit(s2, (0, altura_tela / 4))
    texto_barra = "Uso de CPU: (" + str(cpu) + " %):"
    texto_proc = "Cpu: (" + str(platform.processor()) + "):"
    text = font.render(texto_barra, 1, cordafonte)
    text_proc = font.render(texto_proc, 1, cordafonte)
    tela.blit(text, (20, (altura_tela / 4)))
    tela.blit(text_proc, (20, (altura_tela / 4) + 25))


def desenha_uso_hd():
    disco = mostraDisco()
    largura = largura_tela - 2 * 20
    s3.fill(cordofundo)
    pygame.draw.rect(s3, cordabarra, (20, 50, largura, 70))
    tela.blit(s3, (0, 2 * altura_tela / 4))
    largura = largura * disco.percent / 100
    pygame.draw.rect(s3, cordoindice, (20, 50, largura, 70))
    tela.blit(s3, (0, 2 * altura_tela / 4))
    texto_barra = "Uso de Disco: (" + str(disco.percent) + " %):"
    text = font.render(texto_barra, 1, cordafonte)
    tela.blit(text, (20, (2 * altura_tela / 4)))


def desenha_uso_hd2():
    disco = mostraDisco()
    largura = largura_tela - 2 * 20
    s4.fill(cordofundo)
    pygame.draw.rect(s4, cordabarra, (20, 50, largura, 70))
    tela.blit(s4, (0, 3 * altura_tela / 4))
    largura = largura * disco.percent / 100
    pygame.draw.rect(s4, cordoindice, (20, 50, largura, 70))
    tela.blit(s4, (0, 3 * altura_tela / 4))
    texto_barra = "Uso de Disco: (" + str(disco.percent) + " %):"
    text = font.render(texto_barra, 1, cordafonte)
    tela.blit(text, (20, (3 * altura_tela / 4)))





# Loop da Tela
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if count == 60:
            desenha_barra_cpu()
            desenha_barra_mem()
            desenha_uso_hd()
            desenha_uso_hd2()

            count = 0

        pygame.display.update()

        clock.tick(60)
        count += 1