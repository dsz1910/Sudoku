import pygame


class SudokuBoard:

    HEIGHT = 750
    WIDTH = 850
    BOARD_X = WIDTH * 0.94
    BOARD_Y = HEIGHT * 0.7
    SQUARE_X = BOARD_X / 3
    SQUARE_Y = BOARD_Y / 3
    BOX_X = SQUARE_X / 3
    BOX_Y = SQUARE_Y / 3
    BOARD_LEN = WIDTH * 0.03
    BOARD_TOP = HEIGHT * 0.05

    def __init__(self, window):
        self.window = window
        self.text_font = pygame.font.Font(pygame.font.match_font('verdana'), 30)
        self.thick_lines = (
            ((self.BOARD_LEN + self.SQUARE_X, self.BOARD_TOP), (self.BOARD_LEN + self.SQUARE_X, self.BOARD_TOP + self.BOARD_Y - 1)),
            ((self.BOARD_LEN + self.BOARD_X * (2/3), self.BOARD_TOP), (self.BOARD_LEN + self.BOARD_X * (2/3), self.BOARD_TOP + self.BOARD_Y - 1)),
            ((self.BOARD_LEN, self.BOARD_TOP + self.BOARD_Y * (2/3)), (self.BOARD_LEN + self.BOARD_X - 1, self.BOARD_TOP + self.BOARD_Y * (2/3))),
            ((self.BOARD_LEN, self.BOARD_TOP + self.SQUARE_Y), (self.BOARD_LEN + self.BOARD_X - 1, self.BOARD_TOP + self.SQUARE_Y))
        )
        
    def draw_black_line(self, start, end, thickness=3, color=(0, 0, 0)):
        pygame.draw.line(self.window, color, start, end, thickness)

    def draw_gray_lines(self):
        for i in range(1, 9):
            color = 'gray'
            thickness = 2
            if i % 3 != 0:
                pygame.draw.line(self.window, color, (self.BOARD_LEN + i * self.BOX_X, self.BOARD_TOP), (self.BOARD_LEN + i * self.BOX_X, self.BOARD_TOP + self.BOARD_Y - 1), thickness)
                pygame.draw.line(self.window, color, (self.BOARD_LEN, self.BOARD_TOP + i * self.BOX_Y), (self.BOARD_LEN + self.BOARD_X - 1, self.BOARD_TOP + i * self.BOX_Y), thickness)

    def draw_board(self):
        self.draw_gray_lines()
        for line in self.thick_lines:
            self.draw_black_line(line[0], line[1])
        pygame.draw.rect(self.window, (0, 0, 0), (self.BOARD_LEN, self.BOARD_TOP, self.BOARD_X, self.BOARD_Y), 3)

    def show_numbers(self, sudoku_grid):
            for row, sudoku_row in enumerate(sudoku_grid):
                for col, num in enumerate(sudoku_row):
                    if num[0]:
                        text_surface = self.text_font.render(str(num[0]), True, 'red' if num[1] == 'red' else (0, 0, 0))
                        text_rect = text_surface.get_rect(center=(self.BOARD_LEN + (col + 0.5) * self.BOX_X, self.BOARD_TOP + (row + 0.5) * self.BOX_Y))
                        self.window.blit(text_surface, text_rect)

    def show_solution(self, unsolved, solution):
        for row, unsolved_row in enumerate(unsolved):
            for col, num in enumerate(unsolved_row):
                    if num[1] == True:
                        text_surface = self.text_font.render(str(num[0]), True, (0, 0, 0))
                    else:
                        text_surface = self.text_font.render(str(solution[row][col]), True, 'red')
                    text_rect = text_surface.get_rect(center=(self.BOARD_LEN + (col + 0.5) * self.BOX_X, self.BOARD_TOP + (row + 0.5) * self.BOX_Y))
                    self.window.blit(text_surface, text_rect)