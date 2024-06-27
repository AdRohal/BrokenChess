import pygame
import random
from chess_board import ChessBoard, BOARD_SIZE, SQUARE_SIZE, Color

def main_menu(screen):
    font = pygame.font.SysFont(None, 74)
    button_font = pygame.font.SysFont(None, 50)
    button_text = button_font.render('Start', True, pygame.Color('Black'))
    button_rect = button_text.get_rect(center=(400, 400))

    while True:
        screen.fill(pygame.Color('Black'))
        title_text = font.render('Chess Game', True, pygame.Color('White'))
        screen.blit(title_text, (250, 100))
        pygame.draw.rect(screen, pygame.Color('White'), button_rect.inflate(20, 20))
        screen.blit(button_text, button_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return True

        pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()

    if not main_menu(screen):
        return

    chess_board = ChessBoard()
    running = True
    user_turn = True  # User starts first
    winner = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and user_turn and not winner:
                x, y = event.pos
                x = x // SQUARE_SIZE
                y = y // SQUARE_SIZE
                if chess_board.handle_click(x, y):
                    user_turn = False  # End user's turn after a valid move
                    winner = chess_board.check_winner()

        screen.fill((0, 0, 0))
        chess_board.display_board(screen)

        if winner:
            font = pygame.font.SysFont(None, 74)
            text = font.render(f'{winner} wins!', True, pygame.Color('Red'))
            screen.blit(text, (200, 350))
        pygame.display.flip()
        clock.tick(60)

        if not user_turn and not winner:
            make_ai_move(chess_board)
            user_turn = True  # End AI's turn after making a move
            winner = chess_board.check_winner()

def make_ai_move(chess_board):
    possible_moves = []
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            piece = chess_board.board[y][x]
            if piece.color == Color.BLACK:
                moves = piece.valid_moves(chess_board.board, x, y)
                for move in moves:
                    possible_moves.append(((x, y), move))

    if possible_moves:
        move = random.choice(possible_moves)
        chess_board.move_piece(move[0], move[1])

if __name__ == "__main__":
    main()
