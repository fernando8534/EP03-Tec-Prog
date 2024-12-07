import os
import random
import readchar

class Peca:
    def __init__(self, tipo, posicao):
        self.tipo = tipo
        self.formas = {
            #Aqui é um dicionario com de todas as peças com as 4 possíveis rotações delas, sendo a da posição 0 a padrão.
            "I": [["....", "####", "....", "...."], [".#..", ".#..", ".#..", ".#.."], ["....", "....", "####", "...."], ["..#.", "..#.", "..#.", "..#."]],
            "O": [["##", "##"], ["##", "##"], ["##", "##"], ["##", "##"]],
            "T": [[".#.", "###", "..."], [".#.", ".##", ".#."], ["...", "###", ".#."], [".#.", "##.", ".#."]],
            "S": [[".##", "##.", "..."], [".#.", ".##", "..#"], ["...", ".##", "##."], [".#.", ".##", "..#"]],
            "Z": [["##.", ".##", "..."], [".#.", "##.", "#.."], ["...", "##.", ".##"], [".#.", "##.", "#.."]],
            "J": [["#..", "###", "..."], [".##", ".#.", ".#."], ["...", "###", "..#"], [".#.", ".#.", "##."]],
            "L": [["..#", "###", "..."], [".#.", ".#.", ".##"], ["...", "###", "#.."], ["##.", ".#.", ".#."]],
        }   
        self.rotacao = 0
        self.matriz = self.formas[self.tipo][self.rotacao]
        self.x, self.y = 0, posicao

    def rotacionar(self, sentido):
        #Fazemos a conta da rotação atual com sua respectiva rotação mod4
        if(sentido == "R"):
            self.rotacao = (self.rotacao + 1) % 4
        elif(sentido == "L"):
            self.rotacao = (self.rotacao + 3) % 4
        self.matriz = self.formas[self.tipo][self.rotacao]

class Partida:
    def __init__(self, linhas, colunas):
        self.linhas = linhas
        self.colunas = colunas
        #Gera o tabuleiro vazio
        self.tabuleiro = [["." for _ in range(colunas)] for _ in range(linhas)]
        self.peca_atual = self._gerar_peca()
        self.game_over = False
        self.pontuacao = 0

    def _gerar_peca(self):
        #Gera a peça aleatória
        tipos = ["I", "O", "T", "S", "Z", "J", "L"]
        return Peca(random.choice(tipos), self.colunas//2 - 2)
    
    def mover_peca(self, dx, dy):
        if self._pode_mover(dx, dy):
            self.peca_atual.x += dx
            self.peca_atual.y += dy
        elif dx == 1: 
            self._fixar_peca()

    def _pode_mover(self, dx, dy):
        for i, row in enumerate(self.peca_atual.matriz):
            for j, bloco in enumerate(row):
                if bloco == "#":
                    #Checa se é permitido a movimentação do usuário
                    nx, ny = self.peca_atual.x + i + dx, self.peca_atual.y + j + dy
                    if nx >= self.linhas or ny < 0 or ny >= self.colunas or self.tabuleiro[nx][ny] == "#":
                        return False
        return True
    
    def rotacionar_peca(self, posicao):
        antiga_matriz = self.peca_atual.matriz
        antiga_rotacao = self.peca_atual.rotacao
        self.peca_atual.rotacionar(posicao)
        #Checa se a rotação é válida
        if not self._pode_mover(0, 0):
            self.peca_atual.matriz = antiga_matriz
            self.peca_atual.rotacao = antiga_rotacao


    def _fixar_peca(self):
        #Coloca a peça no tabuleiro principal
        for i, row in enumerate(self.peca_atual.matriz):
            for j, bloco in enumerate(row):
                if bloco == "#":
                    self.tabuleiro[self.peca_atual.x + i][self.peca_atual.y + j] = "#"
        #Gera a nova peça após de fixar a antiga e remove as linhas completas
        self.peca_atual = self._gerar_peca()
        self._remover_linhas_completas()
        #Checa se cabe a nova peça
        if not self._pode_mover(0, 0):  
            self.game_over = True

    def _remover_linhas_completas(self):
        linhas_incompletas = [row for row in self.tabuleiro if "." in row]
        removidas = self.linhas - len(linhas_incompletas)
        self.pontuacao += removidas
        self.tabuleiro = [["." for _ in range(self.colunas)] for _ in range(removidas)] + linhas_incompletas

    def imprimir_tabuleiro(self):
        #Imprime o estado do tabuleiro com a peça que o usuário está movimentando
        tabuleiro_temporario = [row[:] for row in self.tabuleiro]

        for i, row in enumerate(self.peca_atual.matriz):
            for j, bloco in enumerate(row):
                if bloco == "#":
                    nx, ny = self.peca_atual.x + i, self.peca_atual.y + j
                    if 0 <= nx < self.linhas and 0 <= ny < self.colunas:
                        tabuleiro_temporario[nx][ny] = "#"
        
        for row in tabuleiro_temporario:
            print("".join(row))
        
class Jogo:
    def __init__(self, linhas, colunas, jogador):
        self.partida = Partida(linhas, colunas)

    def iniciar(self):
        os.system('cls||clear')
        while not(self.partida.game_over):
            self.partida.imprimir_tabuleiro()
            print("Controles: 'a' = Esquerda, 'd' = Direita, 's' = Baixo, 'w' = Rotacionar Horário, 'e' = Rotacionar Anti-Horário, 'q' = Sair")
            print("Pontuação = ", self.partida.pontuacao)
            key = readchar.readkey()
            if key == "a":
                self.partida.mover_peca(0, -1)
            elif key == "d":
                self.partida.mover_peca(0, 1)
            elif key == "s":
                self.partida.mover_peca(1, 0)
            elif key == "w":
                self.partida.rotacionar_peca("R")
            elif key == "e":
                self.partida.rotacionar_peca("L")
            elif key == "q":
                print("Saindo do jogo. \n")
                self.partida.game_over = True
            os.system('cls||clear')

        self.partida.imprimir_tabuleiro()
        print("Fim de partida!")
        print("Pontuação final: ", self.partida.pontuacao, "\n")


class Ranking:
    def __init__(self):
        self.rank = [[i for i in range(-1, 1)] for _ in range(10)]
    
    def atualizar_ranking(self, jogador, pontuacao):
        for i in range (10):
            if pontuacao > self.rank[i][0]:
                for j in range (8, i - 1, -1):
                        self.rank[j + 1] = self.rank[j]
                self.rank[i] = [pontuacao, jogador]
                break
    
    def mostrar_ranking(self):
        for i in range(10):
            if(-1 == self.rank[i][0]):
                print(i + 1, ". " , sep="")
            else:
                print(i + 1, ". ", self.rank[i][0], " ", self.rank[i][1], sep="")


def iniciar_partida():
    jogador = input("Digite o nome do jogador: ")
    linhas = int(input("Digite o número de linhas da tela do jogo: "))
    colunas = int(input("Digite o número de colunas da tela do jogo: "))
    jogo = Jogo(linhas, colunas, jogador)
    jogo.iniciar()
    rank.atualizar_ranking(jogador, jogo.partida.pontuacao)
    

def carregar_partida():
    os.system('cls||clear')
    print("Hello world")

def ver_melhores_pontuacoes():
    os.system('cls||clear')
    print("*** Jogo Textris - Melhores pontuações ***")
    rank.mostrar_ranking()
    print()

rank = Ranking()
os.system('cls||clear')
Sair = False
while(not(Sair)):
    print("*** Jogo Textris - um tetris em modo texto ***")
    print("Opções do jogo:")
    print("- <i> para iniciar uma nova partida")
    print("- <c> para carregar uma partida gravada e continuá-la")
    print("- <p> para ver as 10 melhores pontuações")
    print("- <s> para sair do jogo")
    entrada = input("Digite a opção desejada: ")
    if(entrada != "i" and entrada != "c" and entrada != "p" and entrada != "s"):
        print("Entrada inválida, tente novamente")
    if entrada == "i":
        iniciar_partida()
    elif entrada == "c":
        carregar_partida()
    elif entrada == "p":
        ver_melhores_pontuacoes()
    elif entrada == "s":
        Sair = True
