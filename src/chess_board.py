import pygame
from chess_piece import ChessPiece, Piece, Color

BOARD_SIZE = 8
SQUARE_SIZE = 100

class ChessBoard:
    def __init__(self):
        self.board = [[ChessPiece(Piece.EMPTY, Color.NONE) for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.setup_board()
        self.selected_piece = None
        self.selected_pos = None

    def setup_board(self):
        for i in range(BOARD_SIZE):
            self.board[1][i] = ChessPiece(Piece.PAWN, Color.BLACK)
            self.board[6][i] = ChessPiece(Piece.PAWN, Color.WHITE)
        setup_order = [Piece.ROOK, Piece.KNIGHT, Piece.BISHOP, Piece.QUEEN, Piece.KING, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK]
        for i, piece in enumerate(setup_order):
            self.board[0][i] = ChessPiece(piece, Color.BLACK)
            self.board[7][i] = ChessPiece(piece, Color.WHITE)

    def display_board(self, screen):
        colors = [pygame.Color(238, 238, 210), pygame.Color(118, 150, 86)]
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = colors[(row + col) % 2]
                pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                piece = self.board[row][col]
                if piece.piece != Piece.EMPTY:
                    piece.set_position(col * SQUARE_SIZE, row * SQUARE_SIZE)
                    piece.draw(screen)

    def move_piece(self, start_pos, end_pos):
        piece = self.board[start_pos[1]][start_pos[0]]
        if end_pos in piece.valid_moves(self.board, start_pos[0], start_pos[1]):
            self.board[end_pos[1]][end_pos[0]] = piece
            self.board[start_pos[1]][start_pos[0]] = ChessPiece(Piece.EMPTY, Color.NONE)
            return True
        return False

    def select_piece(self, x, y):
        if self.board[y][x].color == Color.WHITE:
            self.selected_piece = self.board[y][x]
            self.selected_pos = (x, y)

    def handle_click(self, x, y):
        if self.selected_piece:
            if (x, y) in self.selected_piece.valid_moves(self.board, self.selected_pos[0], self.selected_pos[1]):
                self.move_piece(self.selected_pos, (x, y))
                self.selected_piece = None
                self.selected_pos = None
                return True  # Move was successful
            else:
                self.selected_piece = None
                self.selected_pos = None
                return False  # Move was not successful
        else:
            self.select_piece(x, y)
            return False  # Piece selection, not a move

    def check_winner(self):
        white_king = False
        black_king = False
        for row in self.board:
            for piece in row:
                if piece.piece == Piece.KING:
                    if piece.color == Color.WHITE:
                        white_king = True
                    elif piece.color == Color.BLACK:
                        black_king = True
        if not white_king:
            return "Black"
        elif not black_king:
            return "White"
        return None
