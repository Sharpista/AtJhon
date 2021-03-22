import os
import time

import psutil
import pygame


class Cores:
    preto = (0, 0, 0)
    branco = (255, 255, 255)
    vermelho = (255, 0, 0)
    cinza = (88, 96, 105, 1)
    azul = (3, 102, 214, 1)


class Diretorio:
    diretorios: []
    nome_diretorio = ''
    tamanho = ''
    caminho = ''
    data_criacao = ''
    data_mod = ''


class Processo:
    processos: []


class Contexto:
    cor_fundo = Cores.branco
    largura_tela = 1024
    altura_tela = 730
    tamanho = 10
    pos_x = largura_tela / 2
    pos_y = altura_tela / 2
    tela = pygame.display.set_mode((largura_tela, altura_tela))
    diretorio = Diretorio
    processos = Processo


def mostra_uso_cpu(s, l_cpu_percent):
    s.fill(Cores.cinza)
    num_cpu = len(l_cpu_percent)
    x = y = 10
    desl = 10
    alt = s.get_height() - 2 * y
    larg = (s.get_width() - 2 * y - (num_cpu + 1) * desl) / num_cpu
    d = x + desl
    for i in l_cpu_percent:
        pygame.draw.rect(s, Cores.vermelho, (d, y, larg, alt))
        pygame.draw.rect(s, Cores.azul, (d, y, larg, (1 - i / 100) * alt))
        d = d + larg + desl
    # parte mais abaixo da tela e à esquerda
    Contexto.tela.blit(s, (0, 600 / 5))


def dados_dir():
    lista = os.listdir()
    dic = {}  # cria dicionário
    for i in lista:  # Varia na lista dos arquivos e diretórios
        if os.path.isfile(i):  # checa se é um arquivo
            # Cria uma lista para cada arquivo. Esta lista contém o
            # tamanho, data de criação e data de modificação.
            dic[i] = []
            dic[i].append(os.stat(i).st_size)  # Tamanho
            dic[i].append(os.stat(i).st_atime)  # Tempo de criação
            dic[i].append(os.stat(i).st_mtime)  # Tempo de modificação

    titulo = '{:11}'.format("Tamanho")  # 10 caracteres + 1 de espaço

    # Concatenar com 25 caracteres + 2 de espaços
    titulo = titulo + '{:27}'.format("Data de Modificação")

    # Concatenar com 25 caracteres + 2 de espaços
    titulo = titulo + '{:27}'.format("Data de Criação")

    titulo = titulo + "Nome"

    for i in dic:
        kb = (dic[i][0]) / 1000
        tamanho = '{:10}'.format(str('{:.2f}'.format(kb)) + ' KB')
        tamanho, time.ctime(dic[i][2]), " ", time.ctime(dic[i][1]), " ", i


def dados_pid():
    processos = []
    for proc in psutil.process_iter():
        p = {
            "Nº PID": proc.pid,
            "Nome Executável": proc.name(),
        }
        processos.append(p)

    return processos


def dados_tela(texto, tela, pos_Y, pos_X, font_size, cor, fonte):
    pygame.font.init()
    font = pygame.font.SysFont(fonte, font_size)
    text_tela = font.render(str(texto), True, cor)
    text_rect = text_tela.get_rect()
    text_rect.topleft = (pos_Y, pos_X)
    tela.blit(text_tela, text_rect)


def tela_dir(contexto):
    contexto.diretorio = dados_dir(contexto.diretorio.caminho)
    cor = Cores()
    pos_y = 0
    tamanho = contexto.diretorio.tamanho
    nome_diretorio = contexto.diretorio.nome_diretorio
    caminho = contexto.diretorio.caminho
    data_criacao = contexto.diretorio.data_criacao
    data_mod = contexto.diretorio.data_mod
    diretorios = contexto.diretorio.diretorios

    dados_tela(caminho, Contexto.tela, 350, pos_y, 14, cor.cinza, 'Tahoma')
    pos_y += 90

    dados_tela(nome_diretorio, Contexto.tela, 350, pos_y, 20, cor.azul, 'Tahoma')
    pos_y += 89

    dados_tela(tamanho, Contexto.tela, 350, pos_y, 14, cor.cinza, 'Tahoma')
    pos_y += 88

    dados_tela(data_criacao, Contexto.tela, 350, pos_y, 14, cor.cinza, 'Tahoma')
    pos_y += 87

    dados_tela(data_mod, Contexto.tela, 350, pos_y, 14, cor.cinza, 'Tahoma')
    pos_y += 86

    dados_tela(diretorios, Contexto.tela, 350, pos_y, 14, cor.cinza, 'Tahoma')
    pos_y += 85


def tela_processos(contexto):
    cor = Cores()
    pos_y = 300
    aux = 1
    lista = dados_pid()

    for i in lista:
        dados_tela(i, contexto.tela, 350, pos_y, 14, cor.cinza, 'Tahoma')
        pos_y = 90 - aux


def montar_tela(contexto):
    # Cria relógio
    clock = pygame.time.Clock()

    # Contador de tempo
    cont = 60
    s2 = pygame.surface.Surface((Contexto.altura_tela, Contexto.largura_tela))
    pygame.display.set_caption("Assessment")
    pygame.font.init()
    scroll_y = 0
    sair = True
    while sair:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4: scroll_y = min(scroll_y + 15, 0)
                if event.button == 5: scroll_y = max(scroll_y - 15, -300)
            if event.type == pygame.QUIT:
                sair = False

        if cont == 60:
            l_cpu_percent = psutil.cpu_percent(percpu=True)
            mostra_uso_cpu(s2, l_cpu_percent)
            cont = 0

        contexto.tela.fill(contexto.cor_fundo)
        tela_dir(contexto)
        # tela_processos(contexto)
        pygame.display.flip()
        clock.tick(60)
        cont = cont + 1


def main():
    ctx = Contexto
    ctx.diretorio.caminho = input('Informe o nome do diretório: ')
    montar_tela(ctx)


if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
