# PyTermo - Um jogo de adivinhar palavras
# Copyright (C) 2023 Jonatas Isaac Barbosa Garcez

# Este programa é um software livre; você pode redistribuí-lo e/ou
# modificá-lo sob os termos da Licença Pública Geral GNU como publicada
# pela Free Software Foundation; na versão 3 da Licença, ou
# (a seu critério) qualquer versão posterior.

# Este programa é distribuído na esperança de que possa ser útil,
# mas SEM NENHUMA GARANTIA; sem uma garantia implícita de ADEQUAÇÃO
# a qualquer MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a
# Licença Pública Geral GNU para mais detalhes.

# Você deve ter recebido uma cópia da Licença Pública Geral GNU junto
# com este programa. Se não, veja <http://www.gnu.org/licenses/>.

import random
import time
import sys

# Modo de avaliação. Quando ativo, a palavra em jogo é mostrada ao utilizador no início do jogo
if len(sys.argv) > 1 and sys.argv[1] == 'teste':
    teste = True
else:
    teste = False

# Mensagem que será mostrada 1 vez no início do script
mensagem = """Bem-vindo ao jogo PyTermo.

Em cada jogada é selecionada uma palavra de 5 letras.
O jogador dispõe de 5 tentativas para tentar introduzir a palavra selecionada.
Em cada tentativa é dado feedback ao jogador acerca de letras existentes na palavra e das suas posições.

São mostrados 5 quadrados, correspondentes a cada letra, com a seguinte tipo de estrutura:
-----
-   -
-----

No caso de a uma letra existir na palavra mas não se encontrar na posição correcta (letra 'a'):
-----
- A -
-----

No caso de a letra ter sido introduzida na posição correcta (letra 'a'):
+++++
+ A +
+++++

Caso o jogador introduza a palavra correcta dentro das 5 tentativas vencerá o jogo.
Uma pontuação final será mostrada tendo em conta o número de tentativas e o tempo despendido
"""

# Pede input a perguntar se deve ser iniciada nova jogada, caso não seja iniciada, sair
def quer_jogar():
    pergunta = input("Iniciar nova jogada? (s/n)\n")
    while pergunta not in ['s', 'n']:
        pergunta = input("Iniciar nova jogada? (s/n)\n")
    if pergunta == 's':
        return True
    elif pergunta == 'n':
        print('Até à próxima!')
        exit()

# Ler lista de palavras completas a partir de ficheiro. 
lista_palavras = open('lista_palavras.txt', 'r')
palavras = lista_palavras.read().splitlines()
lista_palavras.close()
for i in range(0, len(palavras)):
    palavras[i] = palavras[i].upper()

# Função para preparar o inicio do jogo: Retornar uma palavra e gerir listas de palavras
def preparar_jogo():

    # Ler palavras já utilizadas
    palavras_usadas = open('usadas.txt', 'a+')
    palavras_usadas.seek(0)
    usadas = palavras_usadas.read().splitlines()

    # Verificar se todas as palavras já foram utilizadas e fazer reset à lista
    if len(usadas) == len(palavras):
        palavras_usadas.close()
        palavras_usadas = open('usadas.txt', 'w')
        palavras_usadas.close()
        palavras_usadas = open('usadas.txt', 'a+')
        palavras_usadas.seek(0)
        usadas = palavras_usadas.read().splitlines()

    # Criar nova lista apenas com as palavras não utilizadas
    lista_final = []
    for i in palavras:
        if i not in usadas:
            lista_final.append(i)

    # Escolher uma palavra aleatória da lista final, adicioná-la à lista de palavras usadas
    palavra_dia = random.choice(lista_final)
    palavra_dia = palavra_dia.upper()
    palavras_usadas.write(palavra_dia + '\n')
    palavras_usadas.close()

    # Retornar a palavra do dia apenas
    return palavra_dia

#Função para introduzir tentativas que verifica tamanho da tentativa. Retorna palavra jogada
def jogar_palavra():
    palavra = input('Introduz uma palavra com 5 letras:\n')
    while len(palavra) != 5:
        palavra = input('Introduz uma palavra com exatamente 5 letras:\n')
    while palavra.upper() not in palavras:
        palavra = input('A palavra que introduziste não existe. Tenta novamente:\n')
    return palavra.upper()

# Função que retorna True se a condição de vitória se cumpriu
def verifica_vitoria(palavra, palavra_dia):
    return palavra == palavra_dia

# Função que compara tentativa com palavra do dia, retornando indices de correspondencias
def comparar(palavra, palavra_dia):
    correspondencias = []
    fora_lugar = []
    today = list(palavra_dia)
    palavra_lista = list(palavra)
    for i in range(0,5):
        if today[i] == palavra_lista[i]:
            correspondencias.append(i)
        elif palavra_lista[i] in today:
            fora_lugar.append(i) 
    return correspondencias, fora_lugar

# Para dar uma referência grafica ao utilizador, a letra fora do lugar fica numa caixa de '-'
def fora_caixa(letra):
    string = ' - ' + letra + ' - '
    return string

# Para dar uma referência grafica ao utilizador, a letra no lugar correcto fica numa caixa de '+'
def dentro_caixa(letra):
    string = ' + ' + letra + ' + '
    return string

# Função que retorna linhas de stings que ilustram o feedback ao utilizador na forma de caixas
def feedback(palavra, palavra_dia):
    print('\n')
    correspondencias, fora_lugar = comparar(palavra, palavra_dia)
    limite = [' ----- '] * 5
    marcador = [' -   - '] * 5
    for i in correspondencias:
        marcador[i] = dentro_caixa(palavra[i])
        limite[i] = ' +++++ '
    for i in fora_lugar:
        marcador[i] = fora_caixa(palavra[i])
    print(''.join(limite))
    print(''.join(marcador)) 
    print(''.join(limite))
    print('\n')

# Calcular pontuação com base no tempo da jogada e número de tentativas utilizadas
def pontuacao(tempo_inicio, tentativas):
    tempo_fim = time.time()
    tempo = tempo_fim - tempo_inicio
    if tempo < 60:
        pontos_tempo = 50
    else:
        pontos_tempo = 50/round(((tempo - 30)/30), 0)
    pontos_tentativa = 50/tentativas
    pontos = pontos_tempo + pontos_tentativa
    return pontos
    

# Função que controla o loop de uma jogada que permite 5 tentativas
def motor_jogada():
    tentativas = 0
    palavra_dia = preparar_jogo()
    if teste:
        print('Modo de teste ativo. A palavra em jogo é: ' + palavra_dia)
    tempo_inicio = time.time()
    letras_tentadas = set()
    while tentativas < 5:
        palavra = jogar_palavra()
        for i in list(palavra):
            letras_tentadas.add(i)
        tentativas = tentativas + 1
        restantes = 5 - tentativas
        feedback(palavra, palavra_dia)
        print('Letras tentadas: ' + ' '.join(sorted(letras_tentadas)) + '\n')
        if verifica_vitoria(palavra, palavra_dia):
            pontos = int(round(pontuacao(tempo_inicio, tentativas),0))
            print('Parabéns! Introduziste a palavra correcta. A tua pontuação foi: ' + str(pontos) + '\n')
            break
        elif tentativas == 5:
            print('Não tens mais tentativas, infelizmente não conseguiste introduzir a palavra do dia!')
            print('A palavra era: ' + palavra_dia + '\n')
        else:
            print('Ainda não foi desta, tens mais %d tentativa(s)\n' % restantes)
    if quer_jogar():
        return True

def iniciar():
    print(mensagem)
    quer_jogar()
    while motor_jogada():
        motor_jogada()

iniciar()