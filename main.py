#!/usr/bin/env python3
"""
Jogo de Xadrez em Python
Desenvolvido com Pygame

Para executar o jogo:
python3 main.py

Controles:
- Clique na peça para selecioná-la
- Clique no destino para mover a peça
- As casas verdes mostram os movimentos possíveis
- A casa amarela mostra a peça selecionada

Funcionalidades implementadas:
- Movimentos válidos para todas as peças
- Verificação de xeque
- Prevenção de movimentos que deixam o rei em xeque
- Interface gráfica interativa
- Alternância de turnos
"""

from gui import ChessGUI

def main():
    print("Iniciando o Jogo de Xadrez...")
    print("Clique nas peças para selecioná-las e mover.")
    print("Feche a janela para sair do jogo.")
    
    try:
        game_gui = ChessGUI()
        game_gui.run()
    except Exception as e:
        print(f"Erro ao executar o jogo: {e}")
        print("Certifique-se de que o Pygame está instalado corretamente.")

if __name__ == "__main__":
    main()
