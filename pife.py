import tkinter as tk
from tkinter import messagebox
import random

from collections import deque

class Jogador:
    def __init__(self, nome):
        self.nome = nome
        self.mao = []

    def comprar(self, baralho=None, pilha_descarte=None):
        if pilha_descarte:
            self.mao.append(pilha_descarte.pop())
        elif baralho:
            self.mao.append(baralho.pop())

    def descartar(self, carta, pilha_descarte):
        self.mao.remove(carta)
        pilha_descarte.append(carta)

    def pode_bater(self):
        return verificar_mao_valida(self.mao)

def criar_baralho():
    naipes = ['♠', '♥', '♦', '♣']
    valores = ['A'] + [str(n) for n in range(2, 11)] + ['J', 'Q', 'K']
    return [f"{v}{n}" for v in valores for n in naipes]

def verificar_mao_valida(mao):
    if len(mao) != 9:
        return False
    combinacoes = encontrar_combinacoes(mao)
    return sum(len(c) for c in combinacoes) == 9

def encontrar_combinacoes(mao):
    from collections import Counter
    
    valores_ordem = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7,
                     '8':8, '9':9, '10':10, 'J':11, 'Q':12, 'K':13}

    combinacoes = []
    mao_restante = mao[:]

    while True:
        # Trinca
        cont = Counter([c[:-1] for c in mao_restante])
        trinca = [v for v, cnt in cont.items() if cnt >= 3]
        if trinca:
            grupo = [c for c in mao_restante if c[:-1] == trinca[0]][:3]
            combinacoes.append(grupo)
            for c in grupo:
                mao_restante.remove(c)
            continue

        # Sequência
        for naipe in ['♠', '♥', '♦', '♣']:
            seq = [c for c in mao_restante if c[-1] == naipe]
            seq_valores = sorted([valores_ordem[c[:-1]] for c in seq])

            for i in range(len(seq_valores) - 2):
                if seq_valores[i+1] == seq_valores[i]+1 and seq_valores[i+2] == seq_valores[i]+2:
                    grupo = []
                    for v in [seq_valores[i], seq_valores[i+1], seq_valores[i+2]]:
                        for c in seq:
                            if valores_ordem[c[:-1]] == v:
                                grupo.append(c)
                                seq.remove(c)
                                break
                    combinacoes.append(grupo)
                    for c in grupo:
                        mao_restante.remove(c)
                    break
            else:
                continue
            break
        else:
            break

    return combinacoes

class JogoPife:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo de Pife")

        self.baralho = criar_baralho()
        random.shuffle(self.baralho)

        self.pilha_descarte = []
        self.fila_jogadores = deque()

        self.jogadores = [Jogador("Jogador 1"), Jogador("Jogador 2")]
        for j in self.jogadores:
            for _ in range(9):
                j.comprar(self.baralho)
            self.fila_jogadores.append(j)

        self.jogador_atual = self.fila_jogadores[0]
        self.status = tk.Label(root, text=f"{self.jogador_atual.nome}, sua vez")
        self.status.pack()

        self.frame_mao = tk.Frame(root)
        self.frame_mao.pack()

        self.frame_compras = tk.Frame(root)
        self.frame_compras.pack()

        self.btn_comprar = tk.Button(self.frame_compras, text="Comprar do Baralho", command=self.comprar_baralho)
        self.btn_comprar.pack(side='left')

        self.btn_comprar_descarte = tk.Button(self.frame_compras, text="Comprar do Descarte", command=self.comprar_descarte)
        self.btn_comprar_descarte.pack(side='left')

        self.btn_bater = tk.Button(root, text="Bater", command=self.bater)
        self.btn_bater.pack()

        self.label_descarte = tk.Label(root, text="Descarte: Vazio")
        self.label_descarte.pack()

        self.atualizar_interface()

    def atualizar_interface(self):
        for widget in self.frame_mao.winfo_children():
            widget.destroy()

        for carta in self.jogador_atual.mao:
            btn = tk.Button(self.frame_mao, text=carta, command=lambda c=carta: self.descartar(c))
            btn.pack(side='left')

        if self.pilha_descarte:
            self.label_descarte.config(text=f"Descarte: {self.pilha_descarte[-1]}")
        else:
            self.label_descarte.config(text="Descarte: Vazio")

    def comprar_baralho(self):
        if len(self.jogador_atual.mao) >= 10:
            messagebox.showinfo("Aviso", "Você já comprou, descarte uma carta.")
            return
        if self.baralho:
            self.jogador_atual.comprar(self.baralho)
            self.status.config(text="Escolha uma carta para descartar.")
            self.atualizar_interface()
        else:
            messagebox.showinfo("Info", "Baralho vazio!")

    def comprar_descarte(self):
        if len(self.jogador_atual.mao) >= 10:
            messagebox.showinfo("Aviso", "Você já comprou, descarte uma carta.")
            return
        if self.pilha_descarte:
            self.jogador_atual.comprar(None, self.pilha_descarte)
            self.status.config(text="Escolha uma carta para descartar.")
            self.atualizar_interface()
        else:
            messagebox.showinfo("Info", "Descarte vazio!")

    def descartar(self, carta):
        if len(self.jogador_atual.mao) != 10:
            messagebox.showinfo("Aviso", "Compre antes de descartar.")
            return

        self.jogador_atual.descartar(carta, self.pilha_descarte)
        self.proximo_turno()

    def bater(self):
        if self.jogador_atual.pode_bater():
            messagebox.showinfo("Vitória!", f"{self.jogador_atual.nome} bateu e venceu!")
            self.root.quit()
        else:
            messagebox.showinfo("Erro", "Sua mão não está completa para bater.")

    def proximo_turno(self):
        self.fila_jogadores.rotate(-1)
        self.jogador_atual = self.fila_jogadores[0]
        self.status.config(text=f"{self.jogador_atual.nome}, sua vez")
        self.atualizar_interface()

if __name__ == '__main__':
    root = tk.Tk()
    jogo = JogoPife(root)
    root.mainloop()
