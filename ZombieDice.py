# Nome: Pedro Luiz Mizael da Cruz
# Curso: Análise e Desenvolvimento de Sistemas

import random
import time
from collections import namedtuple

print("\nBem-vindo ao Zombie Dice!")


# Função que simula uma mensagem de carregamento
def carregando():
    print("\nCarregando...\n")
    time.sleep(0.7)


def tempo():
    time.sleep(0.3)


if input('\nGostaria de ler as regras do jogo? (S/N). Digite "S" para sim e "N" para não. ').upper().strip() == "S":
    print("\nComo o jogo funciona:"
          '\nComeça o jogador que venceu a ultima partida, ou o jogador que falar "cééérebroo" mais parecido com um '
          'zumbi.'
          "\nVamos utilizar um copo com 13 dados dentro, onde 6 deles são verdes, 4 amarelos e 3 vermelhos."
          "\nCada dado representa uma vítima e as cores significam a raridade de cada símbolo."
          "\nOs dados tem 3 símbolos: cérebro, espingarda e pegadas."
          "\n- Cérebro: quer dizer que você devorou uma vítima."
          "\n- Pegadas: sua vítima fugiu."
          "\n- Espingarda: sua vítima atirou em você."
          "\nNo seu turno você irá pegar 3 dados aleatórios do copo e rolar eles."
          "\nExemplo: ao rolar os dados você tirou 1 cérebro, 1 passo e 1 tiro, você pode escolher se quer continuar "
          "ou passar a vez e ficar com os cérebros que já comeu. "
          "\nSe você escolher continuar você vai pegar os dados que não são cérebro e completar com os dados do copo "
          "para 3 dados novamente e rolar os dados de novo. "
          "\nSe você levar 3 tiros na sua rodada você perde todos os cérebros que comeu naquela rodada e passa sua vez."
          "\nO jogador que comer 13 cérebros primeiro ganha!")

carregando()

print("Vamos começar!")
tempo()

Dado = namedtuple("Dado", ['cor', 'lados'])

# Lista todos os dados
def criarDados():
    dadoVerde = Dado('verde', ['C', 'C', 'C', 'P', 'P', 'T'])
    dadoAmarelo = Dado('amarelo', ['C', 'C', 'P', 'P', 'T', 'T'])
    dadoVermelho = Dado('vermelho', ['C', 'P', 'P', 'T', 'T', 'T'])

    listaDados = []
    for i in range(6):
        listaDados.append(dadoVerde)
    for i in range(4):
        listaDados.append(dadoAmarelo)
    for i in range(3):
        listaDados.append(dadoVermelho)

    random.shuffle(listaDados)
    return listaDados


# Função para inserir quais serão os jogadores que irão jogar
def criarJogadores():
    jogadores = []

    numJogadores = 0
    while numJogadores < 2:
        try:
            numJogadores = int(input("\nDigite o número de jogadores: "))
            tempo()
            if numJogadores < 2:
                print("\nVocê precisa de pelo menos 2 jogadores!")
                tempo()
        except ValueError:
            print("\nOcorreu um erro, tente novamente.")
            tempo()

    for i in range(numJogadores):
        nome = input(f"\nDigite o nome do jogador {i + 1}: ").title().strip()
        tempo()
        jogador = {'nome': nome, 'pontuacao': 0}
        jogadores.append(jogador)

    print("\nSorteando a ordem dos jogadores...")
    time.sleep(0.7)

    # Randomiza a ordem dos jogadores
    random.shuffle(jogadores)
    print("\n===ORDEM DOS JOGADORES===")
    n = 1
    for jogador in jogadores:
        print(f"{n}. {jogador['nome']}")
        n += 1
        tempo()

    return jogadores

# Mostra quem é o jogador da vez
def turno(jogador):
    input(f"\n{jogador['nome']}, é a sua vez! Pressione <enter> para sortear os dados.")

    listaDados = criarDados()
    pontuacaoTemp = {'cerebros': 0, 'tiros': 0}
    dadosNaMao = []

    # Mostra os dados pegos no turno e adiciona na pontuação de cada jogador
    while True:
        while len(dadosNaMao) < 3:
            dadosNaMao.append(listaDados.pop())
        carregando()
        print("Os dados sorteados foram...\n")
        tempo()

        for dado in reversed(dadosNaMao):
            random.shuffle(dado.lados)
            ladoSorteado = random.choice(dado.lados)

            if ladoSorteado == 'C':
                print("Cérebro - você devorou um cérebro.")
                pontuacaoTemp['cerebros'] += 1
                tempo()
                listaDados.append(dadosNaMao.pop(dadosNaMao.index(dado)))
            elif ladoSorteado == 'T':
                print("Espingarda - você levou um tiro.")
                pontuacaoTemp['tiros'] += 1
                tempo()
                listaDados.append(dadosNaMao.pop(dadosNaMao.index(dado)))
            else:
                print("Pegadas - sua vítima figiu.")
                tempo()

            random.shuffle(listaDados)

        # Mostra o placar de pontos durante o jogo
        print("\n===PONTUAÇÃO ATUAL==="
              f"\n- Cérebros: {pontuacaoTemp['cerebros']}"
              f"\n- Tiros: {pontuacaoTemp['tiros']}")
        tempo()

        # Condição que verifica se o jogador atual levou 3 tiros, caso tenha tomado 3 tiros ele passa a vez e perde os cérebros que havia pego
        if pontuacaoTemp['tiros'] < 3:
            if input("\nDeseja continuar jogando? (S/N) ").upper().strip() == "N":
                print(f"\nVocê devorou {pontuacaoTemp['cerebros']} cérebros neste turno!")
                jogador['pontuacao'] += pontuacaoTemp['cerebros']
                tempo()
                break
        else:
            print(f"\nVocê tomou muitos tiros e acabou perdendo {pontuacaoTemp['cerebros']} cérebros.")
            tempo()
            break


# Mostra os pontos dos jogadores 
def placar(jogadores):
    print("\n===PLACAR===")
    for jogador in jogadores:
        print(f"- {jogador['nome']}: {jogador['pontuacao']} pontos")


jogadores = criarJogadores()

fimDoJogo = False

# Verifica se nenhum dos jogadores devorou 13 cérebros, caso alguns deles tenha devorado o jogo acabará e mostrará quem foi o vencedor
while not fimDoJogo:
    for jogador in jogadores:
        turno(jogador)
        if jogador['pontuacao'] >= 13:
            vencedor = jogador['nome']
            fimDoJogo = True
        if not fimDoJogo:
            placar(jogadores)
        else:
            print(f"\n {vencedor} devorou 13 cérebros e portanto venceu!")
            placar(jogadores)
