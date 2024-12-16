# -*- coding: utf-8 -*-
"""!
@file ep3.py
@brief Um arquivo que implementa uma versão do jogo Tetris chamada Textris
"""
import os, random, readchar, pickle, datetime

"""!
@class Peca

@brief Implementa as funcionalidades específicas de cada peça de Textris

@details A classe implementa as peças de jogo com base em suas características de tipo, forma e posição no tabuleiro de Tetris.
"""
class Peca:
    """!
    @brief Construtor da peça
    
    @param tipo Tipo (formato) da peça
    @param posicao Posição da peça no tabuleiro
    """
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

    """!
    @brief Rotaciona a peça
    
    @details Baseia-se nas listas do dicionário "formas" - que contém todas as possíveis rotações de cada peça - para decidir qual
    forma de rotação a peça assumirá. Caso a rotação seja para a direita, acessa a próxima posição da lista em questão, caso seja 
    para a esquerda, acessa a posição anterior. Todas as contas são feitas utilizando aritmética modular com o intuito de manter a
    propriedade cíclica da rotação.

    @param sentido Sentido de rotação da peça. R é horário, enquanto L se trata do sentido anti-horário.
    """
    def rotacionar(self, sentido):
        #Fazemos a conta da rotação atual com sua respectiva rotação mod4
        if(sentido == "R"):
            self.rotacao = (self.rotacao + 1) % 4
        elif(sentido == "L"):
            self.rotacao = (self.rotacao + 3) % 4
        self.matriz = self.formas[self.tipo][self.rotacao]
    
    """!
    @brief Retorna o tipo da peça
    """
    def retorna_tipo(self):
        return self.tipo

"""!
@class Partida

@brief Implementa todos os aspectos inerentes a uma instância de partida de Textris

@details Atribui a um objeto as características de linhas, colunas, tabuleiro - que se trata da combinação de linhas e colunas, além
das peças já fixadas, peças que ainda não foram fixadas - mas já apareceram no tabuleiro (parâmetro importante especialmente para a 
funcionalidade de gravar o jogo), do jogador e sua respectiva pontuação.
"""
class Partida:
    """!
    @brief Construtor para uma instância de Partida

    @details As linhas e colunas formam o tabuleiro no qual os blocos se empilharão, cada partida também tem necessariamente um jogador 
    atribuído a ela. Os argumentos opcionais "tabuleiro", "peca_atual" e "pontuacao" são passados para carregar uma partida 
    previamente gravada.

    @param linhas Quantidade de linhas do tabuleiro 
    @param colunas Quantidade de colunas do tabuleiro 
    @param jogador Jogador da partida
    @param tabuleiro Tabuleiro possivelmente já com peças fixadas
    @param peca_atual Peça atual ainda não fixada pelo jogador 
    @param pontuacao Pontuação do jogador
    """
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
        
    """!
    @brief Gera uma peça

    @details Gera um tetrimino de formato selecionado pseudo-aleatoriamente entre todas as possibilidades e com posição inicial 
    no topo das colunas e região central das linhas
    """
    def _gerar_peca(self):
        #Gera a peça aleatória
        tipos = ["I", "O", "T", "S", "Z", "J", "L"]
        return Peca(random.choice(tipos), self.colunas//2 - 2)
    
    """!
    @brief Move a peça
    
    @details Atualiza a posição da peça de acordo com as coordenadas x e y novas

    @param dx Distância entre a coordenada vertical da peça e a linha mais acima no tabuleiro
    @param dy Distância entre a coordenada horizontal da peça e a coluna mais à esquerda no tabuleiro
    """
    def mover_peca(self, dx, dy):
        if self._pode_mover(dx, dy):
            self.peca_atual.x += dx
            self.peca_atual.y += dy
        elif dx == 1: 
            self._fixar_peca()

    """!
    @brief Verifica se é possível mover a peça
    
    @param dx Distância entre a coordenada vertical da peça e a linha mais acima no tabuleiro
    @param dy Distância entre a coordenada horizontal da peça e a coluna mais à esquerda no tabuleiro 

    @return Verdadeiro se o deslocamento é possível, falso caso contrário
    """
    def _pode_mover(self, dx, dy):
        for i, row in enumerate(self.peca_atual.matriz):
            for j, bloco in enumerate(row):
                if bloco != ".":
                    #Checa se é permitido a movimentação do usuário
                    nx, ny = self.peca_atual.x + i + dx, self.peca_atual.y + j + dy
                    if nx >= self.linhas or ny < 0 or ny >= self.colunas or self.tabuleiro[nx][ny] != ".":
                        return False
        return True

    """!
    @brief Rotaciona a peça
    
    @param posicao Posição atual da peça
    """
    def rotacionar_peca(self, posicao):
        antiga_matriz = self.peca_atual.matriz
        antiga_rotacao = self.peca_atual.rotacao
        self.peca_atual.rotacionar(posicao)
        #Checa se a rotação é válida
        if not self._pode_mover(0, 0):
            self.peca_atual.matriz = antiga_matriz
            self.peca_atual.rotacao = antiga_rotacao

    """!
    @brief Fixa a peça no tabuleiro
    """
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

    """!
    @brief Remove as linhas completas
    """
    def _remover_linhas_completas(self):
        linhas_incompletas = [row for row in self.tabuleiro if "." in row]
        removidas = self.linhas - len(linhas_incompletas)
        self.pontuacao += removidas
        self.tabuleiro = [["." for _ in range(self.colunas)] for _ in range(removidas)] + linhas_incompletas

    """!
    @brief Imprime o tabuleiro no estado atual da partida
    """
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

    """!
    @brief Salva a partida com o nome do jogador, data e horário atuais
    """
    def salvar_partida(self):
        horario = datetime.datetime.now().strftime("%d-%m-%Y-%H:%M")
        nomeArq = self.jogador + "-" + horario + ".pkl" # .pkl se trata da extensão de arquivo utilizada pelo módulo pickle
        with open(nomeArq, 'wb') as a:
            pickle.dump(Partida(self.linhas, self.colunas, self.jogador, self.tabuleiro, self.peca_atual, self.pontuacao), a)
        
"""!
@class Jogo

@brief Implementa as características do jogo de Textris.

@details Classe que atribui dinamização à classe Partida, isto é, realiza o intermédio entre a classe Partida e input do usuário,
conferindo, apropriadamente, o aspecto de um jogo à instância de partida.   
"""
class Jogo:
    """!
    @brief Construtor para uma instância de Jogo

    @details Todos os argumentos serão passados para a criação de uma instância de Partida, a qual está um nível de hierarquia abaixo
    da classe Jogo.

    @param linhas Quantidade de linhas do tabuleiro 
    @param colunas Quantidade de colunas do tabuleiro 
    @param jogador Jogador da partida
    @param tabuleiro Tabuleiro possivelmente já com peças fixadas
    @param peca_atual Peça atual ainda não fixada pelo jogador 
    @param pontuacao Pontuação do jogador
    """
    def __init__(self, linhas, colunas, jogador, tabuleiro=None, peca_atual=None, pontuacao=None):
        self.salvar = False
        if tabuleiro is not None:
            self.partida = Partida(linhas, colunas, jogador, tabuleiro, peca_atual, pontuacao)
        else:
            self.partida = Partida(linhas, colunas, jogador)

    """!
    @brief Inicia uma partida de Textris

    @details Através de funções para a leitura de input, a função constantemente realiza as atualizações necessárias
    no tabuleiro simultaneamente ao input do jogador
    """
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

    """!
    @brief Retorna o estado de gravação do jogo
    """
    def jogo_salvo(self):
        return self.salvar

"""!
@class Ranking

@brief Administra a colocação dos jogadores
"""
class Ranking:
    """!
    @brief Construtor para o sistema de colocação do Textris
    """
    def __init__(self):
        self.rank = [[i for i in range(-1, 1)] for _ in range(10)]
    
    """!
    @brief Atualiza a colocação de acordo com uma nova pontuação
    
    @details Itera sobre as 10 posições e, caso faça sentido, insere uma nova colocação de acordo com a nova pontuação, realizando os ajustes
    necessário para as colocações anteriores

    @param jogador Nome do jogador
    @param pontuacao Pontuação atribuída ao jogador
    """
    def atualizar_ranking(self, jogador, pontuacao):
        for i in range (10):
            if pontuacao > self.rank[i][0]:
                for j in range (8, i - 1, -1):
                        self.rank[j + 1] = self.rank[j]
                self.rank[i] = [pontuacao, jogador]
                break
    
    """!
    @brief Imprime as colocações dos jogadores
    """
    def mostrar_ranking(self):
        for i in range(10):
            if(-1 == self.rank[i][0]):
                print(i + 1, ". " , sep="")
            else:
                print(i + 1, ". ", self.rank[i][0], " ", self.rank[i][1], sep="")

"""!
@brief Inicia um jogo novo ou carrega um jogo já existente

@param arq_partida_salva Nome de um arquivo que contém informações de uma partida previamente gravada por um jogador
"""
def iniciar_partida(arq_partida_salva=None):
    if arq_partida_salva is not None:
        #inicia um jogo já salvo
        with open(arq_partida_salva, 'rb') as a:
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

"""!
@brief Carrega uma partida salva anteriormente
"""
def carregar_partida():
    os.system('cls||clear')
    caminho_pasta = '.' #indica a pasta atual
    arqs_pkl = [arq for arq in os.listdir(caminho_pasta) if arq.endswith('.pkl')]
    if len(arqs_pkl) == 0:
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

"""!
@brief Mostra o ranking de colocações dos jogadores
"""
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