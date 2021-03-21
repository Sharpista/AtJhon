import pickle

import socket

import psutil
import pygame

s = socket.socket()
host = socket.gethostname()
port = 10016

s.connect((host, port))
while True:
    msg = '0'
    s.send(msg.encode('ascii'))
    bytes = s.recv(4096)
    arq = s.recv(4096)

    cpu_info = pickle.loads(bytes)
    arquivo = pickle.loads(arq)

    print(cpu_info)
    print(arquivo)

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
            s = str(arquivo['cpu_cont'])
            s = s + " (" + str(psutil.cpu_count(logical=False)) + ")"
        else:
            a = list(filter(lambda x: x == chave, cpu_info))
            s = str(a[0])
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


    # Definição de cores utilizadas na tela
    preto = (0, 0, 0)
    branco = (255, 255, 255)
    cinza = (100, 100, 100)
    azul = (0, 0, 255)
    vermelho = (255, 0, 0)

    # Iniciando a janela principal
    largura_tela = 1024
    altura_tela = 768
    tela = pygame.display.set_mode((largura_tela, altura_tela))
    pygame.display.set_caption("Informações de CPU")
    pygame.display.init()

    # Superfície para mostrar as informações:
    s1 = pygame.surface.Surface((largura_tela, altura_tela))
    s2 = pygame.surface.Surface((largura_tela, altura_tela))

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
