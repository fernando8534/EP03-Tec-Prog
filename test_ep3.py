from ep3 import Peca, Partida, Jogo, Ranking

class test_Peca:
    def test_rotacionar():
        peca = Peca("I", 3)
        peca.rotacionar(R)
        assert peca.matriz[peca.tipo][peca.rotacao] == [".I..", ".I..", ".I..", ".I.."]

        peca.rotacionar(L)
        peca.rotacionar(L)
        assert peca.matriz[peca.tipo][peca.rotacao] == ["..I.", "..I.", "..I.", "..I."]

    def test_retorna_tipo(self):
        peca = Peca("T", 3)
        assert peca.retorna_tipo == "T"

class test_Partida:
    def test__gerar_peca():
        peca = _gerar_peca()
        assert peca.tipo in ["I", "O", "T", "S", "Z", "J", "L"]

    def test_mover_peca():
        peca = Peca("Z", 5)
        peca.mover_peca(0, 1)
        assert peca.y == 1

    def rotacionar_peca():
        test_rotacionar()

class test_Ranking:
    rank = Ranking()
    def test_atualizar_ranking():
        Ranking.atualizar_ranking("George Orwell", 1984)
        assert rank == [[1984,"George Orwell"], [-1, 0], [-1, 0], [-1, 0], [-1, 0], [-1, 0], [-1, 0], [-1, 0], [-1, 0], [-1, 0]]