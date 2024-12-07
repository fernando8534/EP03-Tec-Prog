import os
import random
import readchar

class Peca:
    def __init__(self, tipo, posicao):
        self.tipo = tipo
        self.formas = {
            "I": [["....", "####", "....", "...."]],
            "O": [["##", "##"]],
            "T": [[".#.", "###", "..."]],
            "S": [[".##", "##.", "..."]],
            "Z": [["##.", ".##", "..."]],
            "J": [["#..", "###", "..."]],
            "L": [["..#", "###", "..."]],
        }
        self.rotacao = 0
        self.matriz = self.formas[self.tipo][self.rotacao]
        self.x, self.y = 0, posicao

class Partida:
    def __init__(self, linhas, colunas):
        self.linhas = linhas
        self.colunas = colunas
        self.tabuleiro = [["." for _ in range(colunas)] for _ in range(linhas)]
        self.peca_atual = self._gerar_peca()

    def _gerar_peca(self):
        tipos = ["I", "O", "T", "S", "Z", "J", "L"]
        return Peca(random.choice(tipos), self.colunas//2 - 2)
    
    def mover_peca(self, dx, dy):
        self.peca_atual.x += dx
        self.peca_atual.y += dy

    def imprimir_tabuleiro(self):
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
            print("Controles: 'a' = Esquerda, 'd' = Direita, 's' = Baixo, 'w' = Rotacionar, 'q' = Sair")
            self.partida.imprimir_tabuleiro()
            key = readchar.readkey()

            if key == "a":
                self.partida.mover_peca(0, -1)
            elif key == "d":
                self.partida.mover_peca(0, 1)
            elif key == "s":
                self.partida.mover_peca(1, 0)
            elif key == "q":
                print("Saindo do jogo.")
                return
            os.system('cls||clear')


        self.partida.imprimir_tabuleiro()



def iniciar_partida():
    linhas = int(input("Digite o número de linhas da tela do jogo: "))
    colunas = int(input("Digite o número de colunas da tela do jogo: "))
    partida = Partida(linhas, colunas)
    jogo = Jogo(linhas, colunas)
    jogo.iniciar()

    partida.imprimir_tabuleiro()
    

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