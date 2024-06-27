import pygame
from enum import Enum


class Piece(Enum):
    EMPTY = 0
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6


class Color(Enum):
    NONE = 0
    WHITE = 1
    BLACK = 2


class ChessPiece:
    def __init__(self, piece, color):
        self.piece = piece
        self.color = color
        self.image = None
        self.rect = None
        self.load_images()

    def load_images(self):
        if self.piece == Piece.EMPTY:
            return
        color_name = "black" if self.color == Color.BLACK else "white"
        piece_name = self.piece.name.lower()
        filename = f"images/{color_name}_{piece_name}.png"
        original_image = pygame.image.load(filename).convert_alpha()

        # Resize image (adjust as needed)
        scale_factor = 1.5  # Adjust to find a size between normal and too big
        width = int(original_image.get_width() * scale_factor)
        height = int(original_image.get_height() * scale_factor)
        self.image = pygame.transform.scale(original_image, (width, height))
        self.rect = self.image.get_rect()

    def set_position(self, x, y):
        self.rect.topleft = (x, y)

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect)

    def valid_moves(self, board, x, y):
        moves = []
        if self.piece == Piece.PAWN:
            direction = -1 if self.color == Color.WHITE else 1
            # Move forward
            if board[y + direction][x].piece == Piece.EMPTY:
                moves.append((x, y + direction))
                # Double move from starting position
                if (self.color == Color.WHITE and y == 6) or (self.color == Color.BLACK and y == 1):
                    if board[y + 2 * direction][x].piece == Piece.EMPTY:
                        moves.append((x, y + 2 * direction))
            # Captures
            if x > 0 and board[y + direction][x - 1].color != self.color and board[y + direction][x - 1].color != Color.NONE:
                moves.append((x - 1, y + direction))
            if x < 7 and board[y + direction][x + 1].color != self.color and board[y + direction][x + 1].color != Color.NONE:
                moves.append((x + 1, y + direction))
        elif self.piece == Piece.KNIGHT:
            potential_moves = [(x + 2, y + 1), (x + 2, y - 1), (x - 2, y + 1), (x - 2, y - 1),
                               (x + 1, y + 2), (x + 1, y - 2), (x - 1, y + 2), (x - 1, y - 2)]
            for move in potential_moves:
                if 0 <= move[0] < 8 and 0 <= move[1] < 8:
                    if board[move[1]][move[0]].color != self.color:
                        moves.append(move)
        elif self.piece == Piece.BISHOP:
            for i in range(1, 8):
                if 0 <= x + i < 8 and 0 <= y + i < 8:
                    if board[y + i][x + i].color != self.color:
                        moves.append((x + i, y + i))
                        if board[y + i][x + i].color != Color.NONE:
                            break
                    else:
                        break
            for i in range(1, 8):
                if 0 <= x - i < 8 and 0 <= y + i < 8:
                    if board[y + i][x - i].color != self.color:
                        moves.append((x - i, y + i))
                        if board[y + i][x - i].color != Color.NONE:
                            break
                    else:
                        break
            for i in range(1, 8):
                if 0 <= x + i < 8 and 0 <= y - i < 8:
                    if board[y - i][x + i].color != self.color:
                        moves.append((x + i, y - i))
                        if board[y - i][x + i].color != Color.NONE:
                            break
                    else:
                        break
            for i in range(1, 8):
                if 0 <= x - i < 8 and 0 <= y - i < 8:
                    if board[y - i][x - i].color != self.color:
                        moves.append((x - i, y - i))
                        if board[y - i][x - i].color != Color.NONE:
                            break
                    else:
                        break
        elif self.piece == Piece.ROOK:
            for i in range(1, 8):
                if 0 <= x + i < 8:
                    if board[y][x + i].color != self.color:
                        moves.append((x + i, y))
                        if board[y][x + i].color != Color.NONE:
                            break
                    else:
                        break
            for i in range(1, 8):
                if 0 <= x - i < 8:
                    if board[y][x - i].color != self.color:
                        moves.append((x - i, y))
                        if board[y][x - i].color != Color.NONE:
                            break
                    else:
                        break
            for i in range(1, 8):
                if 0 <= y + i < 8:
                    if board[y + i][x].color != self.color:
                        moves.append((x, y + i))
                        if board[y + i][x].color != Color.NONE:
                            break
                    else:
                        break
            for i in range(1, 8):
                if 0 <= y - i < 8:
                    if board[y - i][x].color != self.color:
                        moves.append((x, y - i))
                        if board[y - i][x].color != Color.NONE:
                            break
                    else:
                        break
        elif self.piece == Piece.QUEEN:
            # Combining bishop and rook moves
            bishop_piece = ChessPiece(Piece.BISHOP, self.color)
            rook_piece = ChessPiece(Piece.ROOK, self.color)
            moves.extend(bishop_piece.valid_moves(board, x, y))
            moves.extend(rook_piece.valid_moves(board, x, y))
        elif self.piece == Piece.KING:
            potential_moves = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1),
                               (x + 1, y + 1), (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1)]
            for move in potential_moves:
                if 0 <= move[0] < 8 and 0 <= move[1] < 8:
                    if board[move[1]][move[0]].color != self.color:
                        moves.append(move)
        return moves