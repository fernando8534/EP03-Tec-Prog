import random
import os
import readchar

class Peca:
    def __init__(self, tipo):
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
        self.x, self.y = 0, 3  # Initial position at the top center

    def rotacionar(self):
        self.rotacao = (self.rotacao + 1) % len(self.formas[self.tipo])
        self.matriz = self.formas[self.tipo][self.rotacao]


class Partida:
    def __init__(self, linhas=20, colunas=10):
        self.linhas = linhas
        self.colunas = colunas
        self.tabuleiro = [["." for _ in range(colunas)] for _ in range(linhas)]
        self.pontuacao = 0
        self.peca_atual = self._gerar_peca()
        self.game_over = False

    def _gerar_peca(self):
        tipos = ["I", "O", "T", "S", "Z", "J", "L"]
        return Peca(random.choice(tipos))

    def imprimir_tabuleiro(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        tabuleiro_temporario = [row[:] for row in self.tabuleiro]

        # Render the current piece on the temporary board
        for i, row in enumerate(self.peca_atual.matriz):
            for j, cell in enumerate(row):
                if cell == "#":
                    nx, ny = self.peca_atual.x + i, self.peca_atual.y + j
                    if 0 <= nx < self.linhas and 0 <= ny < self.colunas:
                        tabuleiro_temporario[nx][ny] = "#"

        # Print the board with the current piece
        for row in tabuleiro_temporario:
            print("".join(row))
        print(f"Pontuação: {self.pontuacao}")

    def _pode_mover(self, dx, dy):
        for i, row in enumerate(self.peca_atual.matriz):
            for j, cell in enumerate(row):
                if cell == "#":
                    nx, ny = self.peca_atual.x + i + dx, self.peca_atual.y + j + dy
                    if nx >= self.linhas or ny < 0 or ny >= self.colunas or self.tabuleiro[nx][ny] == "#":
                        return False
        return True

    def mover_peca(self, dx, dy):
        if self._pode_mover(dx, dy):
            self.peca_atual.x += dx
            self.peca_atual.y += dy
        elif dx == 1:  # Blocked while moving down
            self._fixar_peca()

    def _fixar_peca(self):
        for i, row in enumerate(self.peca_atual.matriz):
            for j, cell in enumerate(row):
                if cell == "#":
                    self.tabuleiro[self.peca_atual.x + i][self.peca_atual.y + j] = "#"
        self._remover_linhas_completas()
        self.peca_atual = self._gerar_peca()
        if not self._pode_mover(0, 0):  # New piece can't fit
            self.game_over = True

    def _remover_linhas_completas(self):
        novas_linhas = [row for row in self.tabuleiro if "." in row]
        removidas = self.linhas - len(novas_linhas)
        self.pontuacao += removidas
        self.tabuleiro = [["." for _ in range(self.colunas)] for _ in range(removidas)] + novas_linhas

    def rotacionar_peca(self):
        antiga_matriz = self.peca_atual.matriz
        antiga_rotacao = self.peca_atual.rotacao
        self.peca_atual.rotacionar()

        # Check if the new orientation is valid
        if not self._pode_mover(0, 0):
            # Revert if rotation is invalid
            self.peca_atual.matriz = antiga_matriz
            self.peca_atual.rotacao = antiga_rotacao


class Jogo:
    def __init__(self):
        self.partida = Partida()

    def iniciar(self):
        print("Controles: 'a' = Esquerda, 'd' = Direita, 's' = Baixo, 'w' = Rotacionar, 'q' = Sair")
        while not self.partida.game_over:
            self.partida.imprimir_tabuleiro()
            key = readchar.readkey()

            if key == "a":
                self.partida.mover_peca(0, -1)
            elif key == "d":
                self.partida.mover_peca(0, 1)
            elif key == "s":
                self.partida.mover_peca(1, 0)
            elif key == "w":
                self.partida.rotacionar_peca()
            elif key == "q":
                print("Saindo do jogo.")
                return

        self.partida.imprimir_tabuleiro()
        print("Game Over! Sua pontuação final foi:", self.partida.pontuacao)


if __name__ == "__main__":
    jogo = Jogo()
    jogo.iniciar()
