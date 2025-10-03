import pygame
import sys
from game import Game

class ChessGUI:
    def __init__(self):
        pygame.init()
        self.BOARD_SIZE = 640
        self.SQUARE_SIZE = self.BOARD_SIZE // 8
        self.screen = pygame.display.set_mode((self.BOARD_SIZE, self.BOARD_SIZE + 100))
        pygame.display.set_caption("Jogo de Xadrez")
        
        # Cores
        self.WHITE_SQUARE_COLOR = (240, 217, 181)
        self.BLACK_SQUARE_COLOR = (181, 136, 99)
        self.HIGHLIGHT_COLOR = (255, 255, 0, 128)
        self.POSSIBLE_MOVE_COLOR = (0, 255, 0, 128)
        self.TEXT_COLOR = (0, 0, 0)
        
        # Fonte
        self.font = pygame.font.Font(None, 36)
        
        # Jogo
        self.game = Game()
        
        # Estado da interface
        self.selected_piece = None
        self.selected_pos = None
        self.possible_moves = []
        
        # Carregar imagens das peças
        self.piece_images = self.load_piece_images()

    def load_piece_images(self):
        try:
            # Usar convert() para preparar para a colorkey
            all_pieces_img = pygame.image.load("assets/chess_pieces.png").convert()
        except pygame.error as e:
            print(f"Erro ao carregar imagem: {e}")
            print("Certifique-se de que \
assets/chess_pieces.png\" existe e está acessível.")
            sys.exit()

        images = {}
        original_piece_width = all_pieces_img.get_width() // 6
        original_piece_height = all_pieces_img.get_height() // 4

        piece_order_symbols = [("K", 0), ("Q", 1), ("R", 2), ("B", 3), ("N", 4), ("P", 5)]
        
        # Usar a linha 0 para peças brancas (contorno) e a linha 1 para peças pretas (preenchidas)
        # A imagem fornecida tem as peças pretas preenchidas com preto, o que impede a transparência do branco.
        # Vamos tentar usar as linhas 2 e 3, que são mais detalhadas e podem ter um fundo mais consistente.
        # Após inspecionar a imagem, as linhas 0 e 2 são brancas, e as linhas 1 e 3 são pretas.
        # Para ter um fundo branco para set_colorkey, precisamos de imagens com fundo branco.
        # A imagem que o usuário enviou mostra que as peças brancas e pretas estão na linha 0 e 1, respectivamente, com fundo branco.
        # Vamos usar a linha 0 para as peças brancas e a linha 1 para as peças pretas, e aplicar o set_colorkey.
        
        color_row_map = {
            "white": 0, # Peças brancas na primeira linha da imagem
            "black": 1  # Peças pretas na segunda linha da imagem
        }

        for color, img_row_idx in color_row_map.items():
            for piece_symbol, img_col_idx in piece_order_symbols:
                x = img_col_idx * original_piece_width
                y = img_row_idx * original_piece_height
                
                piece_rect = pygame.Rect(x, y, original_piece_width, original_piece_height)
                
                # Criar uma nova superfície para cada peça para lidar com a transparência
                piece_surface = pygame.Surface((original_piece_width, original_piece_height))
                piece_surface.blit(all_pieces_img, (0, 0), piece_rect)
                
                # Definir o fundo branco como transparente
                piece_surface.set_colorkey((255, 255, 255))
                
                # Redimensionar a peça para o tamanho do quadrado
                piece_surface = pygame.transform.scale(piece_surface, (self.SQUARE_SIZE, self.SQUARE_SIZE))
                
                images[(color, piece_symbol)] = piece_surface
        return images

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                color = self.WHITE_SQUARE_COLOR if (row + col) % 2 == 0 else self.BLACK_SQUARE_COLOR
                rect = pygame.Rect(col * self.SQUARE_SIZE, row * self.SQUARE_SIZE, 
                                 self.SQUARE_SIZE, self.SQUARE_SIZE)
                pygame.draw.rect(self.screen, color, rect)

    def draw_pieces(self):
        for row in range(8):
            for col in range(8):
                piece = self.game.board.get_piece(row, col)
                if piece:
                    piece_img = self.piece_images.get((piece.color, piece.symbol))
                    if piece_img:
                        img_rect = piece_img.get_rect()
                        img_rect.center = (col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2,
                                          row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2)
                        self.screen.blit(piece_img, img_rect)

    def draw_highlights(self):
        if self.selected_pos:
            row, col = self.selected_pos
            highlight_surface = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE), pygame.SRCALPHA)
            highlight_surface.fill(self.HIGHLIGHT_COLOR)
            self.screen.blit(highlight_surface, (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE))
        
        for move_row, move_col in self.possible_moves:
            move_surface = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE), pygame.SRCALPHA)
            move_surface.fill(self.POSSIBLE_MOVE_COLOR)
            self.screen.blit(move_surface, (move_col * self.SQUARE_SIZE, move_row * self.SQUARE_SIZE))

    def draw_info(self):
        info_y = self.BOARD_SIZE + 10
        turn_text = f"Turno: {self.game.current_turn.capitalize()}"
        text_surface = self.font.render(turn_text, True, self.TEXT_COLOR)
        self.screen.blit(text_surface, (10, info_y))
        
        if self.game.board.is_in_check(self.game.current_turn):
            check_text = "XEQUE!"
            check_surface = self.font.render(check_text, True, (255, 0, 0))
            self.screen.blit(check_surface, (200, info_y))

    def get_square_from_mouse(self, mouse_pos):
        x, y = mouse_pos
        if 0 <= x < self.BOARD_SIZE and 0 <= y < self.BOARD_SIZE:
            col = x // self.SQUARE_SIZE
            row = y // self.SQUARE_SIZE
            return row, col
        return None

    def handle_click(self, pos):
        square = self.get_square_from_mouse(pos)
        if not square:
            return
        
        row, col = square
        piece = self.game.board.get_piece(row, col)
        
        if self.selected_piece is None:
            if piece and piece.color == self.game.current_turn:
                self.selected_piece = piece
                self.selected_pos = (row, col)
                self.possible_moves = piece.get_possible_moves(self.game.board)
        else:
            if (row, col) in self.possible_moves:
                start_row, start_col = self.selected_pos
                if self.game.make_move(start_row, start_col, row, col):
                    print(f"Movimento realizado: {start_row},{start_col} -> {row},{col}")
                else:
                    print("Movimento inválido")
            
            self.selected_piece = None
            self.selected_pos = None
            self.possible_moves = []

    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.handle_click(event.pos)
            
            self.screen.fill((255, 255, 255))
            
            self.draw_board()
            self.draw_highlights()
            self.draw_pieces()
            self.draw_info()
            
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()