from pieces import Pawn, Rook, Knight, Bishop, Queen, King

class Board:
    def __init__(self):
        self.board = self.create_board()

    def create_board(self):
        board = [[None for _ in range(8)] for _ in range(8)]
        return board

    def display(self):
        print("  a b c d e f g h")
        print(" +-----------------")
        for r in range(8):
            row_str = [str(8 - r) + "|"]
            for c in range(8):
                piece = self.board[r][c]
                if piece:
                    row_str.append(piece.__repr__().lower() if piece.color == 'black' else piece.__repr__().upper())
                else:
                    row_str.append("..")
            print(" ".join(row_str) + "|")
        print(" +-----------------")

    def get_piece(self, row, col):
        if 0 <= row < 8 and 0 <= col < 8:
            return self.board[row][col]
        return None

    def set_piece(self, row, col, piece):
        if 0 <= row < 8 and 0 <= col < 8:
            self.board[row][col] = piece

    def find_king(self, color):
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if isinstance(piece, King) and piece.color == color:
                    return r, c
        return None

    def is_square_attacked(self, row, col, attacking_color):
        # Verifica se a casa (row, col) está sendo atacada pela cor 'attacking_color'
        for r_piece in range(8):
            for c_piece in range(8):
                piece = self.board[r_piece][c_piece]
                if piece and piece.color == attacking_color:
                    # Simula o movimento da peça para a casa (row, col)
                    # e verifica se é um movimento válido para atacar aquela casa.
                    # A verificação de xeque no próprio rei da peça atacante é ignorada aqui,
                    # pois estamos apenas verificando se a casa pode ser atacada.
                    # A lógica de is_valid_move da peça já considera bloqueios e capturas.
                    try:
                        if piece.is_valid_move(row, col, self, check_king_safety=False):
                            return True
                    except NotImplementedError:
                        pass # Peças sem is_valid_move implementado ainda
        return False

    def is_in_check(self, color):
        king_pos = self.find_king(color)
        if not king_pos:
            return False # Rei não encontrado (erro ou fim de jogo)

        king_row, king_col = king_pos
        attacking_color = 'black' if color == 'white' else 'white'

        return self.is_square_attacked(king_row, king_col, attacking_color)

    def initialize_pieces(self):
        # Este método será preenchido após a criação das classes de peças
        pass

