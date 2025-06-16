# 🃏 Jogo de Pife - Estrutura de Dados e Análise de Algoritmos

Este projeto implementa uma versão interativa do jogo **Pife** (ou Pif-Paf), usando **Python** com **Tkinter** para interface gráfica, **PIL** para geração de cartas, e **pygame** para música de fundo. Foi desenvolvido com fins didáticos na disciplina de Estrutura de Dados e Análise de Algoritmos.

## 🎮 Funcionalidades

- Interface gráfica amigável para jogar entre dois jogadores.
- Sistema de compra de cartas do baralho ou da pilha de descarte.
- Verificação automática se o jogador pode bater (formar três trincas/sequências).
- Geração dinâmica das imagens das cartas.
- Música ambiente de fundo durante o jogo.

## 🧩 Estrutura do Projeto

.
├── cartas/                # Imagens geradas automaticamente das cartas
├── musica/
│   └── jazz_background.mp3
├── pife.py                # Arquivo principal do jogo
└── .gitignore             # Arquivos e pastas ignoradas pelo Git


## 🛠️ Requisitos

- Python 3.x
- Tkinter (geralmente já incluído no Python)
- PIL (Pillow)
- pygame

Instale as dependências com:

bash
pip install pillow pygame


## ▶️ Como jogar

1. Execute o arquivo pife.py:
   
bash
   python pife.py


2. Cada jogador inicia com 9 cartas.

3. Na sua vez:
   - Compre uma carta (do baralho ou do descarte).
   - Descarte uma carta.
   - Tente "bater" se tiver 3 trincas ou sequências.

4. Use Ctrl para agrupar cartas e formar trincas/sequências.

5. O jogo termina quando um jogador bate corretamente.

## 💡 Regras do Pife (resumo)

- Cada jogador tem 9 cartas.
- O objetivo é formar **3 grupos válidos** de 3 cartas:
  - **Sequências** (3 cartas do mesmo naipe em ordem crescente).
  - **Trincas** (3 cartas de mesmo valor, independente do naipe).
- Após comprar uma carta (total de 10), o jogador deve **descartar** uma.
- Pode bater apenas se restarem 9 cartas que formam 3 grupos válidos.

## 📸 Imagens Geradas

As imagens das cartas são criadas automaticamente na pasta cartas/, com símbolos e cores representando os naipes.

## 🎵 Música

A trilha sonora jazz é reproduzida em loop durante o jogo. Arquivo localizado em musica/jazz_background.mp3.

## 📚 Créditos

Projeto desenvolvido por Alvaro Wiggers, Allan Santos, Luan Brendon, Guilherme Fernandes e Thor Camara, como parte da disciplina de **Estrutura de Dados e Análise de Algoritmos**.
