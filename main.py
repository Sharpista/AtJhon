import os
import time

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

class Contexto:
    cor_fundo = Cores.branco
    largura_tela = 1024
    altura_tela = 730
    tamanho = 10
    pos_x = largura_tela / 2
    pos_y = altura_tela / 2
    tela = pygame.display.set_mode((largura_tela, altura_tela))
    diretorio = Diretorio
    nome_diretorio = ''

def dados_dir(dir):
    diretorio = Diretorio
    if os.path.isdir(dir):
        somador = 0
        somador = somador + os.stat(dir).st_size
        diretorio.tamanho = str(somador)
        # diretorio.caminho = dir
        diretorio.data_criacao = time.ctime(os.path.getmtime(dir))
        diretorio.data_mod = time.ctime(os.path.getctime(dir))
        # diretorio.diretorios = [d[0] for d in os.walk(dir)]
        return diretorio
    else:
        return "O diretório", '\''+dir+'\'', "não existe."

def dados_tela(texto, tela, pos_Y, pos_X, font_size, cor, fonte):
    pygame.font.init()
    font = pygame.font.SysFont(fonte, font_size)
    text_tela = font.render(str(texto), True, cor)
    text_rect = text_tela.get_rect()
    text_rect.topleft = (pos_Y, pos_X)
    tela.blit(text_tela, text_rect)


def tela_dir(diretorio):
    cor = Cores()
    pos_y = 300
    # tamanho = diretorio.tamanho
    nome_diretorio = diretorio.nome_diretorio
    caminho = diretorio.caminho
    data_criacao = diretorio.data_criacao
    data_mod = diretorio.data_mod
    diretorios = diretorio.diretorios
    dados_tela(nome_diretorio, Contexto, 300, pos_y, 20, cor.azul, 'Tahoma')
    pos_y += 30
    dados_tela(data_criacao, Contexto, 350, pos_y, 14, cor.cinza, 'Tahoma')
    pos_y += 50


def montar_tela(contexto, diretorio):
    pygame.display.set_caption("Assessment")
    pygame.font.init()
    sair = True
    while sair:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sair = False
        contexto.tela.fill(contexto.cor_fundo)
        tela_dir(diretorio)
        pygame.display.update()

def main():
    nome_dir = input('Informe o nome do diretório: ')
    Diretorio.nome_diretorio = nome_dir
    montar_tela(Contexto, Diretorio)

if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()