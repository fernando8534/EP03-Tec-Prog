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
        #Gera a nova peça após de fixar a antiga
        self.peca_atual = self._gerar_peca()

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
    def __init__(self, linhas, colunas):
        self.partida = Partida(linhas, colunas)

    def iniciar(self):
        os.system('cls||clear')
        while True:
            print("Controles: 'a' = Esquerda, 'd' = Direita, 's' = Baixo, 'w' = Rotacionar Horário, 'e' = Rotacionar Anti-Horário, 'q' = Sair")
            self.partida.imprimir_tabuleiro()
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
                print("Saindo do jogo.")
                return
            os.system('cls||clear')

def iniciar_partida():
    linhas = int(input("Digite o número de linhas da tela do jogo: "))
    colunas = int(input("Digite o número de colunas da tela do jogo: "))
    jogo = Jogo(linhas, colunas)
    jogo.iniciar()
    

def carregar_partida():
    print("Hello world")

def ver_melhores_pontuacoes():
    print("Hello world")

os.system('cls||clear')
print("*** Jogo Textris - um tetris em modo texto ***")
Sair = False
while(not(Sair)):
    print("Opções do jogo:")
    print("- <i> para iniciar uma nova partida")
    print("- <c> para carregar uma partida gravada e continuá-la")
    print("- <p> para ver as 10 melhores pontuações")
    print("- <s> para sair do jogo")
    entrada = input("Digite a opção desejada: ")
    os.system('cls||clear')
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