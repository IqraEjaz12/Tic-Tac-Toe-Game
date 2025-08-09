import pygame
import sys
import math

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 700
BOARD_SIZE = 450
PADDING = 50
LINE_WIDTH = 15
WIN_LINE_WIDTH = 15
CIRCLE_WIDTH = 15
CROSS_WIDTH = 20

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (241, 196, 15)
BUTTON_HOVER_COLOR = (243, 156, 18)

# Game variables
ROWS, COLS = 3, 3
SQUARE_SIZE = BOARD_SIZE // COLS

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# Fonts
font = pygame.font.SysFont('Arial', 50)
title_font = pygame.font.SysFont('Arial', 70)
button_font = pygame.font.SysFont('Arial', 40)


class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = BUTTON_COLOR
        self.hover_color = BUTTON_HOVER_COLOR
        self.is_hovered = False

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 3, border_radius=10)

        text_surf = button_font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False


class TicTacToe:
    def __init__(self):
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.player = 'X'
        self.game_over = False
        self.winner = None
        self.winning_line = None
        self.restart_button = Button(WIDTH // 2 - 100, HEIGHT - 80, 200, 50, "Restart Game")

    def make_move(self, row, col):
        if self.board[row][col] is None and not self.game_over:
            self.board[row][col] = self.player

            # Check for win
            if self.check_win(row, col):
                self.game_over = True
                self.winner = self.player
            # Check for draw
            elif self.check_draw():
                self.game_over = True
            else:
                # Switch player
                self.player = 'O' if self.player == 'X' else 'X'

    def check_win(self, row, col):
        # Check row
        if self.board[row][0] == self.board[row][1] == self.board[row][2] == self.player:
            self.winning_line = ('row', row)
            return True

        # Check column
        if self.board[0][col] == self.board[1][col] == self.board[2][col] == self.player:
            self.winning_line = ('col', col)
            return True

        # Check diagonal
        if row == col and self.board[0][0] == self.board[1][1] == self.board[2][2] == self.player:
            self.winning_line = ('diag', 1)
            return True

        # Check anti-diagonal
        if row + col == 2 and self.board[0][2] == self.board[1][1] == self.board[2][0] == self.player:
            self.winning_line = ('diag', 2)
            return True

        return False

    def check_draw(self):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] is None:
                    return False
        return True

    def reset(self):
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.player = 'X'
        self.game_over = False
        self.winner = None
        self.winning_line = None

    def draw(self, surface):
        # Draw title
        title = title_font.render("TIC TAC TOE", True, TEXT_COLOR)
        surface.blit(title, (WIDTH // 2 - title.get_rect().width // 2, 10))

        # Draw game status
        if not self.game_over:
            status = font.render(f"Player {self.player}'s Turn", True, TEXT_COLOR)
            surface.blit(status, (WIDTH // 2 - status.get_rect().width // 2, HEIGHT - 130))
        elif self.winner:
            status = font.render(f"Player {self.winner} Wins!", True, TEXT_COLOR)
            surface.blit(status, (WIDTH // 2 - status.get_rect().width // 2, HEIGHT - 130))
        else:
            status = font.render("Game Draw!", True, TEXT_COLOR)
            surface.blit(status, (WIDTH // 2 - status.get_rect().width // 2, HEIGHT - 130))

        # Draw restart button
        self.restart_button.draw(surface)

        # Draw board
        board_rect = pygame.Rect(PADDING, PADDING + 50, BOARD_SIZE, BOARD_SIZE)
        pygame.draw.rect(surface, LINE_COLOR, board_rect, border_radius=10)
        pygame.draw.rect(surface, (0, 0, 0), board_rect, 3, border_radius=10)

        # Draw grid lines
        # Vertical lines
        pygame.draw.line(surface, LINE_COLOR,
                         (PADDING + SQUARE_SIZE, PADDING + 50),
                         (PADDING + SQUARE_SIZE, PADDING + 50 + BOARD_SIZE),
                         LINE_WIDTH)
        pygame.draw.line(surface, LINE_COLOR,
                         (PADDING + 2 * SQUARE_SIZE, PADDING + 50),
                         (PADDING + 2 * SQUARE_SIZE, PADDING + 50 + BOARD_SIZE),
                         LINE_WIDTH)

        # Horizontal lines
        pygame.draw.line(surface, LINE_COLOR,
                         (PADDING, PADDING + 50 + SQUARE_SIZE),
                         (PADDING + BOARD_SIZE, PADDING + 50 + SQUARE_SIZE),
                         LINE_WIDTH)
        pygame.draw.line(surface, LINE_COLOR,
                         (PADDING, PADDING + 50 + 2 * SQUARE_SIZE),
                         (PADDING + BOARD_SIZE, PADDING + 50 + 2 * SQUARE_SIZE),
                         LINE_WIDTH)

        # Draw X's and O's
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] == 'X':
                    self.draw_x(surface, row, col)
                elif self.board[row][col] == 'O':
                    self.draw_o(surface, row, col)

        # Draw winning line
        if self.winning_line:
            if self.winning_line[0] == 'row':
                row = self.winning_line[1]
                y = PADDING + 50 + row * SQUARE_SIZE + SQUARE_SIZE // 2
                pygame.draw.line(surface, CROSS_COLOR if self.winner == 'X' else CIRCLE_COLOR,
                                 (PADDING + 20, y),
                                 (PADDING + BOARD_SIZE - 20, y),
                                 WIN_LINE_WIDTH)
            elif self.winning_line[0] == 'col':
                col = self.winning_line[1]
                x = PADDING + col * SQUARE_SIZE + SQUARE_SIZE // 2
                pygame.draw.line(surface, CROSS_COLOR if self.winner == 'X' else CIRCLE_COLOR,
                                 (x, PADDING + 50 + 20),
                                 (x, PADDING + 50 + BOARD_SIZE - 20),
                                 WIN_LINE_WIDTH)
            elif self.winning_line[0] == 'diag':
                if self.winning_line[1] == 1:  # Main diagonal
                    pygame.draw.line(surface, CROSS_COLOR if self.winner == 'X' else CIRCLE_COLOR,
                                     (PADDING + 20, PADDING + 50 + 20),
                                     (PADDING + BOARD_SIZE - 20, PADDING + 50 + BOARD_SIZE - 20),
                                     WIN_LINE_WIDTH)
                else:  # Anti-diagonal
                    pygame.draw.line(surface, CROSS_COLOR if self.winner == 'X' else CIRCLE_COLOR,
                                     (PADDING + BOARD_SIZE - 20, PADDING + 50 + 20),
                                     (PADDING + 20, PADDING + 50 + BOARD_SIZE - 20),
                                     WIN_LINE_WIDTH)

    def draw_x(self, surface, row, col):
        x = PADDING + col * SQUARE_SIZE + SQUARE_SIZE // 2
        y = PADDING + 50 + row * SQUARE_SIZE + SQUARE_SIZE // 2
        offset = SQUARE_SIZE // 3

        pygame.draw.line(surface, CROSS_COLOR,
                         (x - offset, y - offset),
                         (x + offset, y + offset),
                         CROSS_WIDTH)
        pygame.draw.line(surface, CROSS_COLOR,
                         (x + offset, y - offset),
                         (x - offset, y + offset),
                         CROSS_WIDTH)

    def draw_o(self, surface, row, col):
        x = PADDING + col * SQUARE_SIZE + SQUARE_SIZE // 2
        y = PADDING + 50 + row * SQUARE_SIZE + SQUARE_SIZE // 2
        radius = SQUARE_SIZE // 3

        pygame.draw.circle(surface, CIRCLE_COLOR, (x, y), radius, CIRCLE_WIDTH)


def main():
    game = TicTacToe()
    clock = pygame.time.Clock()

    while True:
        mouse_pos = pygame.mouse.get_pos()
        game.restart_button.check_hover(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Handle restart button
                if game.restart_button.handle_event(event):
                    game.reset()

                # Handle board clicks
                if not game.game_over:
                    x, y = event.pos
                    # Check if click is inside the board
                    if PADDING <= x <= PADDING + BOARD_SIZE and PADDING + 50 <= y <= PADDING + 50 + BOARD_SIZE:
                        col = (x - PADDING) // SQUARE_SIZE
                        row = (y - PADDING - 50) // SQUARE_SIZE
                        game.make_move(row, col)

        # Draw everything
        screen.fill(BG_COLOR)
        game.draw(screen)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()