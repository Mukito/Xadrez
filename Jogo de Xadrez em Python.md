# Jogo de Xadrez em Python

Este projeto visa criar um jogo de xadrez tradicional em Python, executável no VSCode, com interface gráfica e movimentos válidos das peças, permitindo a jogabilidade em modo livre para uma pessoa.

## Arquitetura Proposta

A arquitetura do jogo será baseada no padrão Model-View-Controller (MVC) para garantir modularidade e facilitar a manutenção:

*   **Model (Lógica do Jogo):** Responsável por toda a lógica interna do xadrez. Isso inclui a representação do tabuleiro, das peças, validação de movimentos, regras do jogo (xeque, xeque-mate, empate, etc.). A biblioteca `python-chess` pode ser utilizada para auxiliar na validação de movimentos e manipulação do estado do jogo.

*   **View (Interface Gráfica):** Responsável pela apresentação visual do tabuleiro e das peças ao usuário. Será implementada utilizando a biblioteca `Pygame`, que permitirá desenhar o tabuleiro, as peças, e gerenciar eventos de interação do usuário (cliques, arrastar e soltar).

*   **Controller (Controle de Jogo):** Atuará como intermediário entre o Model e a View. Ele receberá as entradas do usuário da View, as interpretará, passará para o Model para processamento da lógica do jogo e, em seguida, atualizará a View com o novo estado do jogo.

## Estrutura de Pastas

```
chess_game/
├── main.py             # Ponto de entrada do jogo
├── board.py            # Definição do tabuleiro e suas operações
├── pieces.py           # Definição das classes das peças (Peão, Torre, Cavalo, etc.)
├── game.py             # Lógica principal do jogo (regras, turnos, etc.)
├── gui.py              # Funções relacionadas à interface gráfica com Pygame
├── assets/             # Imagens das peças e outros recursos gráficos
└── README.md           # Descrição do projeto e arquitetura
```

## Tecnologias Utilizadas

*   **Python 3.x**
*   **Pygame:** Para a interface gráfica.
*   **python-chess (opcional):** Para validação de movimentos e manipulação do estado do jogo (a ser avaliado se será totalmente integrado ou apenas como referência).

