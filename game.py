from board import Board
from pieces import Pawn, Rook, Knight, Bishop, Queen, King

class Game:
    def __init__(self):
        self.board = Board()
        self.initialize_game()
        self.current_turn = 'white'

    def initialize_game(self):
        # Coloca os peões
        for col in range(8):
            self.board.set_piece(1, col, Pawn('black', 1, col))
            self.board.set_piece(6, col, Pawn('white', 6, col))

        # Coloca as torres
        self.board.set_piece(0, 0, Rook('black', 0, 0))
        self.board.set_piece(0, 7, Rook('black', 0, 7))
        self.board.set_piece(7, 0, Rook('white', 7, 0))
        self.board.set_piece(7, 7, Rook('white', 7, 7))

        # Coloca os cavalos
        self.board.set_piece(0, 1, Knight('black', 0, 1))
        self.board.set_piece(0, 6, Knight('black', 0, 6))
        self.board.set_piece(7, 1, Knight('white', 7, 1))
        self.board.set_piece(7, 6, Knight('white', 7, 6))

        # Coloca os bispos
        self.board.set_piece(0, 2, Bishop('black', 0, 2))
        self.board.set_piece(0, 5, Bishop('black', 0, 5))
        self.board.set_piece(7, 2, Bishop('white', 7, 2))
        self.board.set_piece(7, 5, Bishop('white', 7, 5))

        # Coloca as rainhas
        self.board.set_piece(0, 3, Queen('black', 0, 3))
        self.board.set_piece(7, 3, Queen('white', 7, 3))

        # Coloca os reis
        self.board.set_piece(0, 4, King('black', 0, 4))
        self.board.set_piece(7, 4, King('white', 7, 4))

    def make_move(self, start_row, start_col, end_row, end_col):
        piece = self.board.get_piece(start_row, start_col)

        if not piece or piece.color != self.current_turn:
            print("Movimento inválido: Nenhuma peça sua na posição inicial ou não é seu turno.")
            return False

        if piece.is_valid_move(end_row, end_col, self.board):
            # Realiza o movimento
            target_piece = self.board.get_piece(end_row, end_col)
            if target_piece:
                print(f"Peça {target_piece.__repr__()} capturada!")

            self.board.set_piece(end_row, end_col, piece)
            self.board.set_piece(start_row, start_col, None)
            piece.row = end_row
            piece.col = end_col
            piece.has_moved = True

            # Troca o turno
            self.current_turn = 'black' if self.current_turn == 'white' else 'white'
            return True
        else:
            print("Movimento inválido para a peça selecionada.")
            return False

    def display_board(self):
        self.board.display()

# Exemplo de uso (para teste inicial)
if __name__ == "__main__":
    game = Game()
    game.display_board()

    print("\nTentando mover peão branco de (6,0) para (4,0)")
    game.make_move(6, 0, 4, 0)
    game.display_board()

    print("\nTentando mover peão preto de (1,1) para (3,1)")
    game.make_move(1, 1, 3, 1)
    game.display_board()

    print("\nTentando mover cavalo branco de (7,1) para (5,2)")
    game.make_move(7, 1, 5, 2)
    game.display_board()

    print("\nTentando mover peão branco de (4,0) para (3,1) (captura)")
    game.make_move(4, 0, 3, 1)
    game.display_board()

    print("\nTentando mover rei branco para casa atacada (deve ser inválido)")
    # Move o rei branco para uma posição que seria atacada pelo peão preto em (3,1)
    # Isso é apenas um teste, a posição real do rei branco é (7,4)
    # Para testar o xeque, precisamos de um cenário mais controlado.
    # Por enquanto, vamos tentar um movimento inválido simples.
    game.make_move(7, 4, 6, 4) # Rei branco tenta mover uma casa para frente
    game.display_board()

    print("\nVerificando se o rei branco está em xeque:", game.board.is_in_check('white'))
    print("Verificando se o rei preto está em xeque:", game.board.is_in_check('black'))

