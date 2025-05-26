import random
from collections import deque

# Função para criar um baralho simples
def criar_baralho():
    naipes = ['♥', '♦', '♣', '♠']
    valores = ['A'] + [str(n) for n in range(2, 11)] + ['J', 'Q', 'K']
    baralho = [f"{valor}{naipe}" for naipe in naipes for valor in valores]
    random.shuffle(baralho)
    return baralho

# Classe para representar o jogador
class Jogador:
    def __init__(self, nome):
        self.nome = nome
        self.mao = []  # Lista de cartas na mão
        self.historico_acoes = []  # Pilha para histórico

    def comprar_carta(self, baralho):
        if baralho:
            carta = baralho.pop()
            self.mao.append(carta)
            self.historico_acoes.append(('comprar', carta))
            print(f"{self.nome} comprou {carta}.")
        else:
            print("O baralho acabou!")

    def descartar_carta(self, pilha_descarte):
        if self.mao:
            print(f"Cartas na mão: {self.mao}")
            carta = input(f"{self.nome}, escolha a carta para descartar: ")
            if carta in self.mao:
                self.mao.remove(carta)
                pilha_descarte.append(carta)  # Pilha de descarte
                self.historico_acoes.append(('descartar', carta))
                print(f"{self.nome} descartou {carta}.")
            else:
                print("Carta inválida.")
        else:
            print("Sem cartas para descartar.")

    def desfazer_acao(self, pilha_descarte):
        if not self.historico_acoes:
            print(f"{self.nome} não tem ações para desfazer.")
            return
        acao, carta = self.historico_acoes.pop()
        if acao == 'comprar':
            self.mao.remove(carta)
            print(f"{self.nome} desfez a compra de {carta}.")
        elif acao == 'descartar':
            self.mao.append(carta)
            pilha_descarte.pop()  # Remove do topo da pilha
            print(f"{self.nome} desfez o descarte de {carta}.")

# Classe principal do jogo
class JogoPife:
    def __init__(self, nomes_jogadores):
        self.baralho = criar_baralho()
        self.pilha_descarte = []  # Pilha de descarte
        self.jogadores = [Jogador(nome) for nome in nomes_jogadores]
        self.fila_turnos = deque(self.jogadores)

        # Distribui 9 cartas para cada jogador
        for jogador in self.jogadores:
            for _ in range(9):
                jogador.comprar_carta(self.baralho)

    def jogar_turno(self):
        jogador = self.fila_turnos.popleft()
        print(f"\nÉ a vez de {jogador.nome}")

        print(f"Mão atual: {jogador.mao}")
        print(f"Topo do descarte: {self.pilha_descarte[-1] if self.pilha_descarte else 'Vazio'}")

        escolha = input("Deseja comprar do (b)aralho, pegar do (d)escarte ou (u)ndesfazer última ação? ").strip().lower()

        if escolha == 'b':
            jogador.comprar_carta(self.baralho)
        elif escolha == 'd':
            if self.pilha_descarte:
                carta = self.pilha_descarte.pop()
                jogador.mao.append(carta)
                jogador.historico_acoes.append(('comprar_descarte', carta))
                print(f"{jogador.nome} pegou {carta} do descarte.")
            else:
                print("Pilha de descarte vazia.")
        elif escolha == 'u':
            jogador.desfazer_acao(self.pilha_descarte)
        else:
            print("Escolha inválida.")

        jogador.descartar_carta(self.pilha_descarte)

        # Retorna o jogador ao fim da fila
        self.fila_turnos.append(jogador)

    def mostrar_status(self):
        print("\nStatus do jogo:")
        for jogador in self.jogadores:
            print(f"{jogador.nome} - Cartas: {jogador.mao}")
        print(f"Baralho restante: {len(self.baralho)} cartas")
        print(f"Pilha de descarte: {self.pilha_descarte}")

# Função principal
def main():
    nomes = ['Jogador 1', 'Jogador 2']
    jogo = JogoPife(nomes)

    # Rodadas limitadas para exemplo
    for _ in range(5):
        jogo.jogar_turno()
        jogo.mostrar_status()

if __name__ == "__main__":
    main()
