AUTORES:
- Fernando Ramos Takara
  NUSP: 13782230
  e-mail: fernandotakara@usp.br

- Natan José Martins Domingos
  NUSP: 15481350
  e-mail: natanjmd@usp.br

DESCRIÇÃO:

O programa se trata de uma versão diferente do jogo de Tetris chamada de Textris. O jogo todo se passa no terminal, portanto, sua parte gráfica é completamente criada a partir de caracteres ASCII (daí o nome Textris) e toda a interação é feita a partir da linha de comando.

COMO EXECUTAR:

Para jogar Textris, basta instalar o arquivo e executá-lo a partir do terminal. Deste ponto em diante, todas as instruções necessárias para experienciar o jogo estarão na tela. Além disso, a documentação é gerada com uma simples execução do comando doxygen, após mudar as variáveis "INPUT" e "PROJECT_NAME" na Doxyfile. Caso o usuário queira gerar a documentação ou executar testes, basta utilizar os comandos "make doc" ou "make tests", respectivamente, ou, caso deseje, "make all" para realizar ambos, por fim, para limpar os arquivos criados pela Makefile, basta digitar "make clean".

TESTES:

Os testes foram feitos nas funções que eram razoáveis de serem submetidas a testes, visto que algumas funções implementadas manipulam diretamente estados atuais da execução do programa, os quais conferem uma grande complexidade à realização de testes manuais.

DEPENDÊNCIAS:

A versão mais antiga da lingugagem Python cujo o programa foi submetido a testes é a Python 3.8.10, portanto, tendo em mente a grande retrocompatibilidade desta linguagem, é provável que todas as versões posteriores consigam executar o programa sem grandes problemas, com alta possibilidade de quaisquer versões de Python 3 conseguirem rodá-lo. Quanto ao sistema operacional, por consequência da portabilidade e flexibilidade do Python, é plausível que rode em quaisquer versões de Linux e Windows, contudo, a seção responsável pela geração da documentação - assim como a responsável pela "limpeza" de arquivos - no arquivo Makefile é dependente de comandos característicos do Bash, logo, apenas sistemas operacionais que o utilizam são capazes de criá-la. 