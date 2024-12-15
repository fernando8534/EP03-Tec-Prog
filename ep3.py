import os, random, readchar, pickle
from datetime import datetime

class Peca:
    def __init__(self, tipo, posicao):
        self.tipo = tipo
        self.formas = {
            #Aqui é um dicionário de todas as peças com as 4 possíveis rotações delas, sendo a da posição 0 a padrão.
            "I": [["....", "IIII", "....", "...."], [".I..", ".I..", ".I..", ".I.."], ["....", "....", "IIII", "...."], ["..I.", "..I.", "..I.", "..I."]],
            "O": [["OO", "OO"], ["OO", "OO"], ["OO", "OO"], ["OO", "OO"]],
            "T": [[".T.", "TTT", "..."], [".T.", ".TT", ".T."], ["...", "TTT", ".T."], [".T.", "TT.", ".T."]],
            "S": [[".SS", "SS.", "..."], [".S.", ".SS", "..S"], ["...", ".SS", "SS."], [".S.", ".SS", "..S"]],
            "Z": [["ZZ.", ".ZZ", "..."], [".Z.", "ZZ.", "Z.."], ["...", "ZZ.", ".ZZ"], [".Z.", "ZZ.", "Z.."]],
            "J": [["J..", "JJJ", "..."], [".JJ", ".J.", ".J."], ["...", "JJJ", "..J"], [".J.", ".J.", "JJ."]],
            "L": [["..L", "LLL", "..."], [".L.", ".L.", ".LL"], ["...", "LLL", "L.."], ["LL.", ".L.", ".L."]],
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
    
    def retorna_tipo(self):
        return self.tipo

class Partida:
    def __init__(self, linhas, colunas, jogador, tabuleiro=None, peca_atual=None, pontuacao=None):
        self.linhas = linhas
        self.colunas = colunas
        self.jogador = jogador
        self.game_over = False
        if tabuleiro is not None:
            #gera um tabuleiro já preenchido, para jogos previamente salvos
            self.tabuleiro = tabuleiro
            self.peca_atual = peca_atual
            self.pontuacao = pontuacao
        else:
            #Gera o tabuleiro vazio, para jogos novos
            self.tabuleiro = [["." for _ in range(colunas)] for _ in range(linhas)]
            self.peca_atual = self._gerar_peca()
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
                if bloco != ".":
                    #Checa se é permitido a movimentação do usuário
                    nx, ny = self.peca_atual.x + i + dx, self.peca_atual.y + j + dy
                    if nx >= self.linhas or ny < 0 or ny >= self.colunas or self.tabuleiro[nx][ny] != ".":
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
                if bloco != ".":
                    self.tabuleiro[self.peca_atual.x + i][self.peca_atual.y + j] = self.peca_atual.retorna_tipo()
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
                if bloco != ".":
                    nx, ny = self.peca_atual.x + i, self.peca_atual.y + j
                    if 0 <= nx < self.linhas and 0 <= ny < self.colunas:
                        tabuleiro_temporario[nx][ny] = self.peca_atual.retorna_tipo()
        
        for row in tabuleiro_temporario:
            print("".join(row))

    def salvar_partida(self):
        horario = datetime.now().strftime("%d-%m-%Y-%H:%M")
        nomeArq = self.jogador + "-" + horario + ".pkl"
        with open(nomeArq, 'wb') as a:
            pickle.dump(Partida(self.linhas, self.colunas, self.jogador, self.tabuleiro, self.peca_atual, self.pontuacao), a)
        
class Jogo:
    def __init__(self, linhas, colunas, jogador, tabuleiro=None, peca_atual=None, pontuacao=None):
        self.salvar = False
        if tabuleiro is not None:
            self.partida = Partida(linhas, colunas, jogador, tabuleiro, peca_atual, pontuacao)
        else:
            self.partida = Partida(linhas, colunas, jogador)

    def iniciar(self):
        self.salvar = False
        os.system('cls||clear')
        while not(self.partida.game_over):
            self.partida.imprimir_tabuleiro()
            print("Controles: 'a' = Esquerda, 'd' = Direita, 's' = Baixo, 'w' = Rotacionar Horário, 'e' = Rotacionar Anti-Horário, 'y' = Salvar Jogo, 'q' = Sair")
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
            elif key == "y":
                self.partida.salvar_partida()
                self.salvar = True
                break
            elif key == "q":
                print("Saindo do jogo. \n")
                self.partida.game_over = True
            os.system('cls||clear')
        if self.salvar:
            print("Partida salva!\n")
        else:
            self.partida.imprimir_tabuleiro()
            print("Fim de partida!")
            print("Pontuação final: ", self.partida.pontuacao, "\n")

    def jogo_salvo(self):
        return self.salvar

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

def iniciar_partida(partida_salva=None):
    if partida_salva is not None:
        #inicia um jogo já salvo
        with open(partida_salva, 'rb') as a:
            partida_salva = pickle.load(a)
        jogador = partida_salva.jogador
        linhas = partida_salva.linhas
        colunas = partida_salva.colunas
        tabuleiro = partida_salva.tabuleiro
        peca_atual = partida_salva.peca_atual
        pontuacao = partida_salva.pontuacao
        jogo = Jogo(linhas, colunas, jogador, tabuleiro, peca_atual, pontuacao)

    else:
        #inicia uma nova partida
        jogador = input("Digite o nome do jogador: ")
        linhas = int(input("Digite o número de linhas da tela do jogo: "))
        colunas = int(input("Digite o número de colunas da tela do jogo: "))
        jogo = Jogo(linhas, colunas, jogador)
    
    jogo.iniciar()
    if(not(jogo.jogo_salvo())):
        rank.atualizar_ranking(jogador, jogo.partida.pontuacao)
    
def carregar_partida():
    os.system('cls||clear')
    caminho_pasta = '.' #indica a pasta atual
    arqs_pkl = [arq for arq in os.listdir(caminho_pasta) if arq.endswith('.pkl')]
    if (len(arqs_pkl) == 0):
        print("Não há partidas salvas.\n")
    else:
        print("Escolha uma partida para carregar:\n")
        print(' ')
        for indice, arq in enumerate(arqs_pkl):
            print(f"{indice + 1}. {arq}")
        print(' ')
        try:
            escolha = int(input("Insira o índice correspondente à partida salva: "))
            print(' ')
            if 1 <= escolha <= len(arqs_pkl):
                arq_escolhido = arqs_pkl[escolha - 1]
                iniciar_partida(arq_escolhido)
            else:
                print("O índice selecionado não existe.")
        except ValueError:
            print("Escolha inválida, tente novamente:\n")
            print(" ")
            
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
        os.system('cls||clear')
        print("*** Entrada inválida, tente novamente ***")
    if entrada == "i":
        iniciar_partida()
    elif entrada == "c":
        carregar_partida()
    elif entrada == "p":
        ver_melhores_pontuacoes()
    elif entrada == "s":
        Sair = True
