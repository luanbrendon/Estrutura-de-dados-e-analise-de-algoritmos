import tkinter as tk
from tkinter import messagebox
import random
from collections import deque
import os
from PIL import Image, ImageTk, ImageDraw, ImageFont
import pygame

# Inicializa o mixer do pygame
pygame.mixer.init()
pygame.mixer.music.load("musica/jazz_background.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

# Função para gerar as imagens das cartas
def gerar_imagens_cartas(pasta="cartas"):
    os.makedirs(pasta, exist_ok=True)
    naipes = ['♠', '♥', '♦', '♣']
    valores = ['A'] + [str(n) for n in range(2, 11)] + ['J', 'Q', 'K']

    try:
        fonte = ImageFont.truetype("arial.ttf", 24)
    except:
        fonte = ImageFont.load_default()

    for naipe in naipes:
        for valor in valores:
            carta = f"{valor}{naipe}"
            cor = "red" if naipe in ['♥', '♦'] else "black"

            img = Image.new("RGB", (80, 120), "white")
            draw = ImageDraw.Draw(img)
            draw.rectangle([0, 0, 79, 119], outline="black", width=2)
            draw.text((10, 10), valor, font=fonte, fill=cor)
            draw.text((10, 90), naipe, font=fonte, fill=cor)

            img.save(os.path.join(pasta, f"{carta}.png"))

# Funções do jogo
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
        cont = Counter([c[:-1] for c in mao_restante])
        trinca = [v for v, cnt in cont.items() if cnt >= 3]
        if trinca:
            grupo = [c for c in mao_restante if c[:-1] == trinca[0]][:3]
            combinacoes.append(grupo)
            for c in grupo:
                mao_restante.remove(c)
            continue

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

# Classe principal do jogo
class JogoPife:
    def __init__(self, root):
        gerar_imagens_cartas    ()

        self.root = root
        self.root.title("Jogo de Pife")
        self.root.geometry("1000x600")
        self.root.configure(bg="#006400")

        self.ctrl_pressed = False
        self.root.bind("<Control_L>", self.ctrl_press)
        self.root.bind("<KeyRelease-Control_L>", self.ctrl_release)

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

        self.status = tk.Label(root, text=f"{self.jogador_atual.nome}, sua vez", font=("Arial", 14), bg="#006400", fg="white")
        self.status.pack(pady=10)

        self.mesa_frame = tk.Frame(root, bg="#006400")
        self.mesa_frame.pack(pady=10)

        self.frame_mao = tk.Frame(root, bg="#006400")
        self.frame_mao.pack(pady=10)

        self.frame_compras = tk.Frame(root, bg="#006400")
        self.frame_compras.pack(pady=10)

        self.btn_comprar = tk.Button(self.frame_compras, text="Comprar do Baralho", command=self.comprar_baralho)
        self.btn_comprar.pack(side='left', padx=5)

        self.btn_comprar_descarte = tk.Button(self.frame_compras, text="Comprar do Descarte", command=self.comprar_descarte)
        self.btn_comprar_descarte.pack(side='left', padx=5)

        self.btn_bater = tk.Button(root, text="Bater", command=self.bater)
        self.btn_bater.pack(pady=5)

        self.selecoes = {}
        self.grupo_atual = 0
        self.cores_usadas = set()
        self.cores_por_grupo = {}

        self.atualizar_interface()

    def nova_cor(self):
        while True:
            cor = "#%06x" % random.randint(0, 0xFFFFFF)
            if cor not in self.cores_usadas:
                self.cores_usadas.add(cor)
                return cor

    def ctrl_press(self, event=None):
        self.ctrl_pressed = True

    def ctrl_release(self, event=None):
        self.ctrl_pressed = False
        self.grupo_atual += 1

    def carregar_imagem_carta(self, carta):
        path = os.path.join("cartas", f"{carta}.png")
        if os.path.exists(path):
            img = Image.open(path)
            return ImageTk.PhotoImage(img)
        return None

    def atualizar_interface(self):
        for widget in self.frame_mao.winfo_children():
            widget.destroy()
        for widget in self.mesa_frame.winfo_children():
            widget.destroy()

        for carta in self.jogador_atual.mao:
            img = self.carregar_imagem_carta(carta)
            if img:
                frame = tk.Frame(self.frame_mao, bd=2, relief="solid")
                grupo = self.selecoes.get(carta)
                if grupo is not None:
                    cor = grupo[1]
                    frame.config(highlightbackground=cor, highlightcolor=cor, highlightthickness=3)
                btn = tk.Button(frame, image=img, command=lambda c=carta: self.carta_clicada(c))
                btn.image = img
                btn.pack()
                frame.pack(side='left', padx=5)

        if self.pilha_descarte:
            topo = self.pilha_descarte[-1]
            img = self.carregar_imagem_carta(topo)
            if img:
                lbl = tk.Label(self.mesa_frame, text="Topo da pilha", bg="#006400", fg="white")
                lbl.pack()
                carta_img = tk.Label(self.mesa_frame, image=img, bg="#006400")
                carta_img.image = img
                carta_img.pack()
        else:
            lbl = tk.Label(self.mesa_frame, text="Descarte: Vazio", bg="#006400", fg="white")
            lbl.pack()

    def carta_clicada(self, carta):
        if self.ctrl_pressed:
            if carta in self.selecoes:
                del self.selecoes[carta]
            else:
                if self.grupo_atual not in self.cores_por_grupo:
                    self.cores_por_grupo[self.grupo_atual] = self.nova_cor()
                cor = self.cores_por_grupo[self.grupo_atual]
                self.selecoes[carta] = (self.grupo_atual, cor)
        else:
            if len(self.jogador_atual.mao) == 10:
                self.descartar(carta)
            else:
                messagebox.showinfo("Aviso", "Você só pode descartar depois de comprar uma carta.")
        self.atualizar_interface()

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
        self.selecoes.clear()
        self.cores_usadas.clear()
        self.cores_por_grupo.clear()
        self.grupo_atual = 0
        self.proximo_turno()

    def bater(self):
        combinacoes = encontrar_combinacoes(self.jogador_atual.mao)
        if sum(len(c) for c in combinacoes) == 9:
            # Limpa a tela de jogo
            for widget in self.root.winfo_children():
                widget.destroy()

            lbl_vitoria = tk.Label(self.root, text=f"{self.jogador_atual.nome} bateu e venceu!", font=("Arial", 20),
                                   bg="#006400", fg="white")
            lbl_vitoria.pack(pady=20)

            frame_combinacoes = tk.Frame(self.root, bg="#006400")
            frame_combinacoes.pack(pady=10)

            for grupo in combinacoes:
                grupo_frame = tk.Frame(frame_combinacoes, bg="#006400", bd=2, relief="groove")
                grupo_frame.pack(side='left', padx=10)
                for carta in grupo:
                    img = self.carregar_imagem_carta(carta)
                    if img:
                        lbl = tk.Label(grupo_frame, image=img, bg="#006400")
                        lbl.image = img
                        lbl.pack(side='left', padx=2)

            btn_sair = tk.Button(self.root, text="Encerrar Jogo", font=("Arial", 14), command=self.root.quit)
            btn_sair.pack(pady=20)
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
