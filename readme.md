🃏 Jogo de Pife - Estrutura de Dados e Análise de Algoritmos
Este projeto implementa uma versão interativa do jogo Pife (ou Pif-Paf), desenvolvido com Python utilizando Tkinter para a interface gráfica, PIL (Pillow) para geração das cartas e pygame para a música de fundo. Foi criado como parte da disciplina de Estrutura de Dados e Análise de Algoritmos, com foco na aplicação de conceitos como Pilha, Fila e Listas.

🎮 Funcionalidades
Interface Gráfica Amigável: Permite que dois jogadores joguem de forma interativa.

Compra de Cartas: Jogadores podem comprar cartas do baralho ou da pilha de descarte.

Verificação de Bater: O jogo verifica automaticamente se um jogador pode "bater", ou seja, formar 3 trincas ou sequências.

Geração Dinâmica das Cartas: As imagens das cartas são criadas automaticamente.

Música de Fundo: Trilha sonora de jazz tocando em loop durante a partida.

🧩 Estrutura do Projeto
bash
Copiar
.
├── cartas/                # Imagens geradas automaticamente das cartas
├── musica/                # Arquivo de música de fundo
│   └── jazz_background.mp3
├── pife.py                # Arquivo principal do jogo
└── .gitignore             # Arquivos e pastas ignoradas pelo Git
🛠️ Requisitos
Para rodar o projeto, é necessário ter o seguinte instalado:

Python 3.x

Tkinter (geralmente já incluído no Python)

Pillow (PIL) para manipulação de imagens

pygame para a música de fundo

Instale as dependências com o seguinte comando:

bash
Copiar
pip install pillow pygame
▶️ Como Jogar
Executando o Jogo:

Para iniciar, execute o arquivo principal do jogo:

bash
Copiar
python pife.py
Início do Jogo:

Cada jogador começa com 9 cartas.

Durante a sua vez:

Compre uma carta: Escolha uma carta do baralho ou da pilha de descarte.

Descarte uma carta: Após comprar, descarte uma carta de sua mão.

Forme Trincas ou Sequências: Tente formar trincas ou sequências com suas cartas.

Formando Trincas/Sequências:

Para agrupar cartas e formar trincas ou sequências, use a tecla Ctrl.

Final do Jogo:

O jogo termina quando um jogador forma 3 trincas ou sequências, completando a "bateria".

💡 Regras do Pife (Resumo)
Objetivo: Formar 3 grupos válidos de 3 cartas.

Sequências: 3 cartas do mesmo naipe em ordem crescente.

Trincas: 3 cartas de mesmo valor, independente do naipe.

Como Jogar:

Cada jogador tem 9 cartas.

Após comprar uma carta (total de 10), o jogador deve descartar uma carta.

O jogador só pode "bater" quando tiver 3 grupos válidos formados com suas cartas.

📸 Imagens Geradas
As imagens das cartas são criadas automaticamente na pasta cartas/. Cada carta é representada por seu valor e naipe, sendo gerada com cores e símbolos distintos para os naipes.

🎵 Música de Fundo
A música ambiente é um arquivo jazz que toca em loop durante toda a partida, localizado em musica/jazz_background.mp3.

📚 Créditos
Este projeto foi desenvolvido por Álvaro Wiggers, Allan Santos, Luan Brendon, Guilherme Fernandes e Thor Camara, como parte da disciplina Estrutura de Dados e Análise de Algoritmos da Universidade UNISUL - Pedra Branca.
