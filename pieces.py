'''Este arquivo define as classes para cada peça do jogo de xadrez.
'''

class Piece:
    '''Classe base para todas as peças.
    '''
    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col
        self.has_moved = False
        self.symbol = ''

    def __repr__(self):
        return f"{self.color[0].upper()}{self.symbol}"

    def is_valid_move(self, new_row, new_col, board, check_king_safety=True):
        '''Verifica se um movimento é válido, incluindo a segurança do rei.
        '''
        if not (0 <= new_row < 8 and 0 <= new_col < 8):
            return False

        target_piece = board.get_piece(new_row, new_col)
        if target_piece and target_piece.color == self.color:
            return False

        if not self._is_valid_move_logic(new_row, new_col, board):
            return False

        if check_king_safety:
            # Simula o movimento para verificar se o rei fica em xeque
            original_piece = board.get_piece(new_row, new_col)
            start_row, start_col = self.row, self.col

            board.set_piece(new_row, new_col, self)
            board.set_piece(start_row, start_col, None)
            self.row, self.col = new_row, new_col

            is_safe = not board.is_in_check(self.color)

            # Desfaz a simulação
            self.row, self.col = start_row, start_col
            board.set_piece(start_row, start_col, self)
            board.set_piece(new_row, new_col, original_piece)

            return is_safe
        
        return True

    def get_possible_moves(self, board):
        '''Retorna uma lista de movimentos válidos para a peça.
        '''
        possible_moves = []
        for r in range(8):
            for c in range(8):
                if self.is_valid_move(r, c, board):
                    possible_moves.append((r, c))
        return possible_moves

    def _is_valid_move_logic(self, new_row, new_col, board):
        '''Lógica de movimento específica de cada peça (deve ser sobrescrita).
        '''
        raise NotImplementedError


class Pawn(Piece):
    '''Classe para o Peão.
    '''
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.symbol = 'P'

    def _is_valid_move_logic(self, new_row, new_col, board):
        direction = -1 if self.color == 'white' else 1
        start_row = 6 if self.color == 'white' else 1

        # Movimento para frente
        if new_col == self.col:
            if board.get_piece(new_row, new_col) is None:
                if new_row == self.row + direction:
                    return True
                if self.row == start_row and new_row == self.row + 2 * direction and \
                   board.get_piece(self.row + direction, self.col) is None:
                    return True
        # Captura
        elif abs(new_col - self.col) == 1 and new_row == self.row + direction:
            target = board.get_piece(new_row, new_col)
            if target and target.color != self.color:
                return True
        return False


class Rook(Piece):
    '''Classe para a Torre.
    '''
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.symbol = 'R'

    def _is_valid_move_logic(self, new_row, new_col, board):
        if new_row != self.row and new_col != self.col:
            return False

        # Verifica o caminho
        if new_row == self.row:
            step = 1 if new_col > self.col else -1
            for c in range(self.col + step, new_col, step):
                if board.get_piece(self.row, c) is not None:
                    return False
        else:
            step = 1 if new_row > self.row else -1
            for r in range(self.row + step, new_row, step):
                if board.get_piece(r, self.col) is not None:
                    return False
        return True


class Knight(Piece):
    '''Classe para o Cavalo.
    '''
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.symbol = 'N'

    def _is_valid_move_logic(self, new_row, new_col, board):
        dr = abs(new_row - self.row)
        dc = abs(new_col - self.col)
        return (dr == 2 and dc == 1) or (dr == 1 and dc == 2)


class Bishop(Piece):
    '''Classe para o Bispo.
    '''
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.symbol = 'B'

    def _is_valid_move_logic(self, new_row, new_col, board):
        if abs(new_row - self.row) != abs(new_col - self.col):
            return False

        row_step = 1 if new_row > self.row else -1
        col_step = 1 if new_col > self.col else -1

        r, c = self.row + row_step, self.col + col_step
        while r != new_row:
            if board.get_piece(r, c) is not None:
                return False
            r += row_step
            c += col_step
        return True


class Queen(Piece):
    '''Classe para a Rainha.
    '''
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.symbol = 'Q'

    def _is_valid_move_logic(self, new_row, new_col, board):
        # Lógica da Torre
        if new_row == self.row or new_col == self.col:
            return Rook(self.color, self.row, self.col)._is_valid_move_logic(new_row, new_col, board)
        # Lógica do Bispo
        if abs(new_row - self.row) == abs(new_col - self.col):
            return Bishop(self.color, self.row, self.col)._is_valid_move_logic(new_row, new_col, board)
        return False


class King(Piece):
    '''Classe para o Rei.
'''
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.symbol = 'K'

    def _is_valid_move_logic(self, new_row, new_col, board):
        dr = abs(new_row - self.row)
        dc = abs(new_col - self.col)
        return dr <= 1 and dc <= 1




#=======================================================


# class Piece:
#     def __init__(self, color, row, col):
#         self.color = color
#         self.row = row
#         self.col = col
#         self.has_moved = False

#     def __repr__(self):
#         return f"{self.color[0]}{self.symbol}"

#     def is_valid_move(self, new_row, new_col, board, check_king_safety=True):
#         # Verifica se o destino está dentro do tabuleiro
#         if not (0 <= new_row < 8 and 0 <= new_col < 8):
#             return False

#         target_piece = board.get_piece(new_row, new_col)
#         # Não pode mover para uma casa ocupada por uma peça da mesma cor
#         if target_piece and target_piece.color == self.color:
#             return False

#         # Lógica específica de movimento para cada peça será implementada nas subclasses
#         # Se check_king_safety for True, simula o movimento para verificar se o rei fica em xeque
#         if check_king_safety:
#             original_piece = board.get_piece(new_row, new_col)
#             original_pos_row, original_pos_col = self.row, self.col

#             # Simula o movimento
#             board.set_piece(new_row, new_col, self)
#             board.set_piece(original_pos_row, original_pos_col, None)
#             self.row, self.col = new_row, new_col

#             is_safe = not board.is_in_check(self.color)

#             # Desfaz o movimento simulado
#             self.row, self.col = original_pos_row, original_pos_col
#             board.set_piece(original_pos_row, original_pos_col, self)
#             board.set_piece(new_row, new_col, original_piece)

#             return is_safe

#         return True # Se não for para verificar a segurança do rei, o movimento é válido por padrão (subclasses ajustarão)

#     def get_possible_moves(self, board):
#         possible_moves = []
#         for r in range(8):
#             for c in range(8):
#                 # Verifica se o movimento é válido sem considerar a segurança do rei primeiro
#                 # A segurança do rei será verificada dentro de is_valid_move quando chamado com check_king_safety=True
#                 if self._is_valid_move_logic(r, c, board) and self.is_valid_move(r, c, board, check_king_safety=True):
#                     possible_moves.append((r, c))
#         return possible_moves

#     def _is_valid_move_logic(self, new_row, new_col, board):
#         # Lógica de movimento pura da peça, sem verificar xeque ou peças da mesma cor no destino
#         # Este método deve ser sobrescrito por cada tipo de peça
#         raise NotImplementedError

# class Pawn(Piece):
#     def __init__(self, color, row, col):
#         super().__init__(color, row, col)
#         self.symbol = 'P'

#     def _is_valid_move_logic(self, new_row, new_col, board):
#         direction = -1 if self.color == 'white' else 1
#         start_row = 6 if self.color == 'white' else 1

#         # Movimento para frente
#         if new_col == self.col:
#             # Um passo
#             if new_row == self.row + direction and board.get_piece(new_row, new_col) is None:
#                 return True
#             # Dois passos (primeiro movimento)
#             if self.row == start_row and new_row == self.row + 2 * direction and \
#                board.get_piece(new_row, new_col) is None and \
#                board.get_piece(self.row + direction, self.col) is None:
#                 return True
#         # Captura
#         elif abs(new_col - self.col) == 1 and new_row == self.row + direction:
#             target_piece = board.get_piece(new_row, new_col)
#             if target_piece and target_piece.color != self.color:
#                 return True
#         # TODO: En passant
#         return False

#     def is_valid_move(self, new_row, new_col, board, check_king_safety=True):
#         if not (0 <= new_row < 8 and 0 <= new_col < 8):
#             return False

#         target_piece = board.get_piece(new_row, new_col)
#         if target_piece and target_piece.color == self.color:
#             return False

#         if not self._is_valid_move_logic(new_row, new_col, board):
#             return False

#         if check_king_safety:
#             original_piece = board.get_piece(new_row, new_col)
#             original_pos_row, original_pos_col = self.row, self.col

#             board.set_piece(new_row, new_col, self)
#             board.set_piece(original_pos_row, original_pos_col, None)
#             self.row, self.col = new_row, new_col

#             is_safe = not board.is_in_check(self.color)

#             self.row, self.col = original_pos_row, original_pos_col
#             board.set_piece(original_pos_row, original_pos_col, self)
#             board.set_piece(new_row, new_col, original_piece)

#             return is_safe
#         return True

# class Rook(Piece):
#     def __init__(self, color, row, col):
#         super().__init__(color, row, col)
#         self.symbol = 'R'

#     def _is_valid_move_logic(self, new_row, new_col, board):
#         if new_row == self.row:
#             step = 1 if new_col > self.col else -1
#             for c in range(self.col + step, new_col, step):
#                 if board.get_piece(self.row, c) is not None:
#                     return False
#         elif new_col == self.col:
#             step = 1 if new_row > self.row else -1
#             for r in range(self.row + step, new_row, step):
#                 if board.get_piece(r, self.col) is not None:
#                     return False
#         else:
#             return False
#         return True

#     def is_valid_move(self, new_row, new_col, board, check_king_safety=True):
#         if not (0 <= new_row < 8 and 0 <= new_col < 8):
#             return False

#         target_piece = board.get_piece(new_row, new_col)
#         if target_piece and target_piece.color == self.color:
#             return False

#         if not self._is_valid_move_logic(new_row, new_col, board):
#             return False

#         if check_king_safety:
#             original_piece = board.get_piece(new_row, new_col)
#             original_pos_row, original_pos_col = self.row, self.col

#             board.set_piece(new_row, new_col, self)
#             board.set_piece(original_pos_row, original_pos_col, None)
#             self.row, self.col = new_row, new_col

#             is_safe = not board.is_in_check(self.color)

#             self.row, self.col = original_pos_row, original_pos_col
#             board.set_piece(original_pos_row, original_pos_col, self)
#             board.set_piece(new_row, new_col, original_piece)

#             return is_safe
#         return True

# class Knight(Piece):
#     def __init__(self, color, row, col):
#         super().__init__(color, row, col)
#         self.symbol = 'N'

#     def _is_valid_move_logic(self, new_row, new_col, board):
#         dr = abs(new_row - self.row)
#         dc = abs(new_col - self.col)
#         return (dr == 1 and dc == 2) or (dr == 2 and dc == 1)

#     def is_valid_move(self, new_row, new_col, board, check_king_safety=True):
#         if not (0 <= new_row < 8 and 0 <= new_col < 8):
#             return False

#         target_piece = board.get_piece(new_row, new_col)
#         if target_piece and target_piece.color == self.color:
#             return False

#         if not self._is_valid_move_logic(new_row, new_col, board):
#             return False

#         if check_king_safety:
#             original_piece = board.get_piece(new_row, new_col)
#             original_pos_row, original_pos_col = self.row, self.col

#             board.set_piece(new_row, new_col, self)
#             board.set_piece(original_pos_row, original_pos_col, None)
#             self.row, self.col = new_row, new_col

#             is_safe = not board.is_in_check(self.color)

#             self.row, self.col = original_pos_row, original_pos_col
#             board.set_piece(original_pos_row, original_pos_col, self)
#             board.set_piece(new_row, new_col, original_piece)

#             return is_safe
#         return True

# class Bishop(Piece):
#     def __init__(self, color, row, col):
#         super().__init__(color, row, col)
#         self.symbol = 'B'

#     def _is_valid_move_logic(self, new_row, new_col, board):
#         if abs(new_row - self.row) != abs(new_col - self.col):
#             return False

#         row_step = 1 if new_row > self.row else -1
#         col_step = 1 if new_col > self.col else -1

#         r, c = self.row + row_step, self.col + col_step
#         while r != new_row:
#             if board.get_piece(r, c) is not None:
#                 return False
#             r += row_step
#             c += col_step
#         return True

#     def is_valid_move(self, new_row, new_col, board, check_king_safety=True):
#         if not (0 <= new_row < 8 and 0 <= new_col < 8):
#             return False

#         target_piece = board.get_piece(new_row, new_col)
#         if target_piece and target_piece.color == self.color:
#             return False

#         if not self._is_valid_move_logic(new_row, new_col, board):
#             return False

#         if check_king_safety:
#             original_piece = board.get_piece(new_row, new_col)
#             original_pos_row, original_pos_col = self.row, self.col

#             board.set_piece(new_row, new_col, self)
#             board.set_piece(original_pos_row, original_pos_col, None)
#             self.row, self.col = new_row, new_col

#             is_safe = not board.is_in_check(self.color)

#             self.row, self.col = original_pos_row, original_pos_col
#             board.set_piece(original_pos_row, original_pos_col, self)
#             board.set_piece(new_row, new_col, original_piece)

#             return is_safe
#         return True

# class Queen(Piece):
#     def __init__(self, color, row, col):
#         super().__init__(color, row, col)
#         self.symbol = 'Q'

#     def _is_valid_move_logic(self, new_row, new_col, board):
#         # Movimento de torre
#         if new_row == self.row or new_col == self.col:
#             return Rook(self.color, self.row, self.col)._is_valid_move_logic(new_row, new_col, board)
#         # Movimento de bispo
#         elif abs(new_row - self.row) == abs(new_col - self.col):
#             return Bishop(self.color, self.row, self.col)._is_valid_move_logic(new_row, new_col, board)
#         return False

#     def is_valid_move(self, new_row, new_col, board, check_king_safety=True):
#         if not (0 <= new_row < 8 and 0 <= new_col < 8):
#             return False

#         target_piece = board.get_piece(new_row, new_col)
#         if target_piece and target_piece.color == self.color:
#             return False

#         if not self._is_valid_move_logic(new_row, new_col, board):
#             return False

#         if check_king_safety:
#             original_piece = board.get_piece(new_row, new_col)
#             original_pos_row, original_pos_col = self.row, self.col

#             board.set_piece(new_row, new_col, self)
#             board.set_piece(original_pos_row, original_pos_col, None)
#             self.row, self.col = new_row, new_col

#             is_safe = not board.is_in_check(self.color)

#             self.row, self.col = original_pos_row, original_pos_col
#             board.set_piece(original_pos_row, original_pos_col, self)
#             board.set_piece(new_row, new_col, original_piece)

#             return is_safe
#         return True

# class King(Piece):
#     def __init__(self, color, row, col):
#         super().__init__(color, row, col)
#         self.symbol = 'K'

#     def _is_valid_move_logic(self, new_row, new_col, board):
#         dr = abs(new_row - self.row)
#         dc = abs(new_col - self.col)

#         # Movimento normal do rei (uma casa em qualquer direção)
#         if dr <= 1 and dc <= 1:
#             return True

#         # TODO: Roque
#         return False

#     def is_valid_move(self, new_row, new_col, board, check_king_safety=True):
#         if not (0 <= new_row < 8 and 0 <= new_col < 8):
#             return False

#         target_piece = board.get_piece(new_row, new_col)
#         if target_piece and target_piece.color == self.color:
#             return False

#         if not self._is_valid_move_logic(new_row, new_col, board):
#             return False

#         if check_king_safety:
#             original_piece = board.get_piece(new_row, new_col)
#             original_pos_row, original_pos_col = self.row, self.col

#             board.set_piece(new_row, new_col, self)
#             board.set_piece(original_pos_row, original_pos_col, None)
#             self.row, self.col = new_row, new_col

#             is_safe = not board.is_in_check(self.color)

#             self.row, self.col = original_pos_row, original_pos_col
#             board.set_piece(original_pos_row, original_pos_col, self)
#             board.set_piece(new_row, new_col, original_piece)

#             return is_safe
#         return True

