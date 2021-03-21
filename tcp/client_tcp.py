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



# Mostra as informações de CPU escolhidas:
def mostra_info_cpu():
    s1.fill(branco)
    mostra_texto(s1, "Nome:", "brand_raw", 10)
    mostra_texto(s1, "Arquitetura:", "arch", 30)
    mostra_texto(s1, "Palavra (bits):", "bits", 50)
    mostra_texto(s1, "Frequência (MHz):", "hz_actual_friendly", 70)
    mostra_texto(s1, "Núcleos (físicos):", "count", 90)
    tela.blit(s1, (0, 0))


# Mostra texto de acordo com uma chave:
def mostra_texto(s1, nome, chave, pos_y):
    text = font.render(nome, True, preto)
    s1.blit(text, (10, pos_y))
    if chave == "freq":
        s = str(round(arquivo['freq'], 2))
    elif chave == "nucleos":
        s = str(arquivo['cpu_count'])
        s = s + " (" + str(psutil.cpu_count(logical=False)) + ")"
    else:
        a = list(filter(lambda x: x == chave, cpu_info))[1:-1]
        s = str(a)
        text = font.render(s, True, cinza)
        s1.blit(text, (160, pos_y))


def mostra_uso_cpu(s, l_cpu_percent):
    s.fill(cinza)
    num_cpu = len(l_cpu_percent)
    x = y = 10
    desl = 10
    alt = s.get_height() - 2 * y
    larg = (s.get_width() - 2 * y - (num_cpu + 1) * desl) / num_cpu
    d = x + desl
    for i in l_cpu_percent:
        pygame.draw.rect(s, vermelho, (d, y, larg, alt))
        pygame.draw.rect(s, azul, (d, y, larg, (1 - i / 100) * alt))
        d = d + larg + desl
    # parte mais abaixo da tela e à esquerda
    tela.blit(s, (0, altura_tela / 5))

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
    larg = largura_tela - 2 * 5
    s3.fill(cinza)
    pygame.draw.rect(s3, vermelho, (20, 50, larg, 70))
    tela.blit(s3, (0, 0))
    larg = larg * mem.percent / 100
    pygame.draw.rect(s3, azul, (20, 50, larg, 70))
    tela.blit(s3, (0, 0))
    total = round(mem.total / (1024 * 1024 * 1024), 2)
    texto_barra = "Uso de Memória (Total: " + str(total) + "GB) (Utilizando: " + str(mem.percent) + " %):"
    text = font.render(texto_barra, 1, branco)
    tela.blit(text, (20, 10))


def desenha_barra_cpu():
    cpu = mostraCPU()
    largura = largura_tela - 2 * 5
    s4.fill(cinza)
    pygame.draw.rect(s4, vermelho, (20, 50, largura, 70))
    tela.blit(s4, (0, altura_tela / 4))
    largura = largura * cpu / 100
    pygame.draw.rect(s4, azul, (20, 50, largura, 70))
    tela.blit(s4, (0, altura_tela / 6))
    texto_barra = "Uso de CPU: (" + str(cpu) + " %):"
    texto_proc = "Cpu: (" + str(platform.processor()) + "):"
    text = font.render(texto_barra, 1, branco)
    text_proc = font.render(texto_proc, 1, branco)
    tela.blit(text, (20, (altura_tela / 4)))
    tela.blit(text_proc, (20, (altura_tela / 4) + 25))


def desenha_uso_hd():
    disco = mostraDisco()
    largura = largura_tela - 2 * 5
    s5.fill(cinza)
    pygame.draw.rect(s5, vermelho, (20, 50, largura, 70))
    tela.blit(s5, (0, 2 * altura_tela / 6))
    largura = largura * disco.percent / 100
    pygame.draw.rect(s5, azul, (20, 50, largura, 70))
    tela.blit(s3, (0, 2 * altura_tela / 4))
    texto_barra = "Uso de Disco: (" + str(disco.percent) + " %):"
    text = font.render(texto_barra, 1, branco)
    tela.blit(text, (20, (2 * altura_tela / 4)))


def desenha_uso_hd2():
    disco = mostraDisco()
    largura = largura_tela - 2 * 5
    s6.fill(cinza)
    pygame.draw.rect(s6, vermelho, (20, 50, largura, 70))
    tela.blit(s6, (0, 3 * altura_tela / 6))
    largura = largura * disco.percent / 100
    pygame.draw.rect(s6, azul, (20, 50, largura, 70))
    tela.blit(s6, (0, 3 * altura_tela / 4))
    texto_barra = "Uso de Disco: (" + str(disco.percent) + " %):"
    text = font.render(texto_barra, 1, branco)
    tela.blit(text, (20, (3 * altura_tela / 4)))


# Definição de cores utilizadas na tela
preto = (0, 0, 0)
branco = (255, 255, 255)
cinza = (100, 100, 100)
azul = (0, 0, 255)
vermelho = (255, 0, 0)

# Iniciando a janela principal
largura_tela = 1378
altura_tela = 768
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Informações de CPU")
pygame.display.init()

# Superfície para mostrar as informações:
s1 = pygame.surface.Surface((largura_tela, altura_tela))
s2 = pygame.surface.Surface((largura_tela, altura_tela))
s3 = pygame.surface.Surface((largura_tela, altura_tela))
s4 = pygame.surface.Surface((largura_tela, altura_tela))
s5 = pygame.surface.Surface((largura_tela, altura_tela))
s6 = pygame.surface.Surface((largura_tela, altura_tela))

# Para usar na fonte
pygame.font.init()
font = pygame.font.Font(None, 24)

# Cria relógio
clock = pygame.time.Clock()

# Contador de tempo
cont = 60

terminou = True
scroll_y = 0

# Repetição para capturar eventos e atualizar tela
while terminou:
    # Checar os eventos do mouse aqui:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminou = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4: scroll_y = min(scroll_y + 15, 0)
            if event.button == 5: scroll_y = max(scroll_y - 15, -300)

    # Fazer a atualização a cada segundo:
    if cont == 60:
        mostra_info_cpu()
        lista = list(map(int, arquivo['cpu_perc']))
        l_cpu_percent = lista
        mostra_uso_cpu(s2, l_cpu_percent)
        cont = 0

    # Atualiza o desenho na tela
    pygame.display.update()
    pygame.display.flip()

    # 60 frames por segundo
    clock.tick(60)
    cont = cont + 1

# Finaliza a janela
pygame.display.quit()
s.close()
