import os

def iniciar_partida():
    print("Hello world")

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
    else:
        Sair = True