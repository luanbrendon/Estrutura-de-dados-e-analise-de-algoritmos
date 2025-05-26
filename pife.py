import tkinter as tk
from tkinter import messagebox
import random
from collections import deque

# Cria baralho
def criar_baralho():
    naipes = ['♥', '♦', '♣', '♠']
    valores = ['A'] + [str(n) for n in range(2, 11)] + ['J', 'Q', 'K']
    baralho = [f"{valor}{naipe}" for naipe in naipes for valor in valores]
    random.shuffle(baralho)
    return baralho

# Jogador
class Jogador:
    def __init__(self, nome):
        self.nome = nome
        self.mao = []
        self.historico_acoes = []

    def comprar(self, origem, pilha_descarte=None):
        if origem:
            carta = origem.pop()
            self.mao.append(carta)
            self.historico_acoes.append(('comprar', carta))
            return carta
        elif pilha_descarte:
            carta = pilha_descarte.pop()
            self.mao.append(carta)
            self.historico_acoes.append(('comprar_descarte', carta))
            return carta
        return None

    def descartar(self, carta, pilha_descarte):
        if carta in self.mao:
            self.mao.remove(carta)
            pilha_descarte.append(carta)
            self.historico_acoes.append(('descartar', carta))
            return True
        return False

    def desfazer(self, pilha_descarte):
        if not self.historico_acoes:
            return "Sem ações para desfazer!"
        acao, carta = self.historico_acoes.pop()
        if acao.startswith('comprar'):
            self.mao.remove(carta)
            return f"Desfez compra de {carta}"
        elif acao == 'descartar':
            self.mao.append(carta)
            pilha_descarte.pop()
            return f"Desfez descarte de {carta}"

    def venceu(self):
        # Simples: mão vazia ou formada só por trincas/sequências
        if len(self.mao) == 0:
            return True

        # Verifica trincas ou sequências
        cartas = sorted(self.mao, key=lambda x: x[:-1])
        return self.check_combinacoes(cartas)

    def check_combinacoes(self, cartas):
        # Exemplo simples: se mão tem múltiplos de 3, considera vitória
        return len(cartas) % 3 == 0

# Jogo com interface
class JogoPifeGUI:
    def __init__(self, root, nomes):
        self.root = root
        self.root.title("Pife Paf")
        
        self.baralho = criar_baralho()
        self.pilha_descarte = []
        self.jogadores = [Jogador(nome) for nome in nomes]
        self.fila_turnos = deque(self.jogadores)
        
        for jogador in self.jogadores:
            for _ in range(9):
                jogador.comprar(self.baralho)

        self.jogador_atual = self.fila_turnos[0]

        # Elementos da interface
        self.info = tk.Label(root, text="Jogo de Pife")
        self.info.pack()

        self.mao_label = tk.Label(root, text="")
        self.mao_label.pack()

        self.descarte_label = tk.Label(root, text="")
        self.descarte_label.pack()

        self.compra_baralho_btn = tk.Button(root, text="Comprar Baralho", command=self.comprar_baralho)
        self.compra_baralho_btn.pack()

        self.compra_descarte_btn = tk.Button(root, text="Pegar Descarte", command=self.comprar_descarte)
        self.compra_descarte_btn.pack()

        self.descartar_entry = tk.Entry(root)
        self.descartar_entry.pack()

        self.descartar_btn = tk.Button(root, text="Descartar", command=self.descartar)
        self.descartar_btn.pack()

        self.desfazer_btn = tk.Button(root, text="Desfazer", command=self.desfazer)
        self.desfazer_btn.pack()

        self.status = tk.Label(root, text="")
        self.status.pack()

        self.atualizar_interface()

    def atualizar_interface(self):
        self.mao_label.config(text=f"{self.jogador_atual.nome} - Mão: {self.jogador_atual.mao}")
        topo = self.pilha_descarte[-1] if self.pilha_descarte else "Vazio"
        self.descarte_label.config(text=f"Topo Descarte: {topo}")
        self.status.config(text=f"Baralho: {len(self.baralho)} cartas")

    def proximo_turno(self):
        self.fila_turnos.rotate(-1)
        self.jogador_atual = self.fila_turnos[0]
        self.atualizar_interface()

    def comprar_baralho(self):
        if self.baralho:
            self.jogador_atual.comprar(self.baralho)
            self.atualizar_interface()
        else:
            messagebox.showinfo("Info", "Baralho vazio!")

    def comprar_descarte(self):
        if self.pilha_descarte:
            self.jogador_atual.comprar(None, self.pilha_descarte)
            self.atualizar_interface()
        else:
            messagebox.showinfo("Info", "Descarte vazio!")

    def descartar(self):
        carta = self.descartar_entry.get()
        if self.jogador_atual.descartar(carta, self.pilha_descarte):
            self.atualizar_interface()
            if self.jogador_atual.venceu():
                messagebox.showinfo("Vitória", f"{self.jogador_atual.nome} venceu!")
                self.root.quit()
            else:
                self.proximo_turno()
        else:
            messagebox.showerror("Erro", "Carta inválida ou não na mão.")

    def desfazer(self):
        msg = self.jogador_atual.desfazer(self.pilha_descarte)
        messagebox.showinfo("Desfazer", msg)
        self.atualizar_interface()

# Executa o jogo
if __name__ == "__main__":
    root = tk.Tk()
    nomes = ["Jogador 1", "Jogador 2"]
    jogo = JogoPifeGUI(root, nomes)
    root.mainloop()
