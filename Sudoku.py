import pygame
from sudoku_generator import SudokuGridMaker
from sudoku_board import SudokuBoard
import buttons
import time


class SudokuGame:

    def __init__(self):
        pygame.init()
        self.running = True
        self.level = self.solved = self.loss = False
        self.row = self.col = self.final_time = self.sudoku_grid = None

        self.window = pygame.display.set_mode((SudokuBoard.WIDTH, SudokuBoard.HEIGHT))
        pygame.display.set_caption('Sudoku')
        self.window.fill((240, 240, 240))
        self.font = pygame.font.Font(pygame.font.match_font('verdana'), 25)
        self.board = SudokuBoard(self.window)
        self.board.draw_board()

        self.easy_button = buttons.LevelButton('easy', (55, 650), 200, 50)
        self.medium_button = buttons.LevelButton('medium', (325, 650), 200, 50)
        self.hard_button = buttons.LevelButton('hard', (590, 650), 200, 50)
        self.solve_button = buttons.SolveButton((590, 650), 200, 50)
        self.new_game_button = buttons.NewGameButton((SudokuBoard.WIDTH / 2 - 100, SudokuBoard.HEIGHT * 0.85), 200, 50)
    
    def draw_text(self, text, position, center=True, color=(0, 0, 0), background=None):
        text_surface = self.font.render(text, True, color, background)
        text_rect = text_surface.get_rect(center=position) if center else text_surface.get_rect(topleft=position)
        if background:
            self.window.fill(background, text_rect)
        self.window.blit(text_surface, text_rect)
    
    def get_new_sudoku(self):
        self.window.fill((240, 240, 240))
        sudoku = SudokuGridMaker(self.level)
        self.sudoku_grid, self.solution = sudoku.grid, sudoku.solution
        self.sudoku_grid = self.nums_not_to_change(self.sudoku_grid)
        self.board.draw_board()
        self.board.show_numbers(self.sudoku_grid)
        self.mistakes = 0
        self.solved = self.loss = False
        self.final_time = self.row = None
        self.start = time.time()

    def draw_level_buttons(self):
        self.easy_button.draw(self.window)
        self.medium_button.draw(self.window)
        self.hard_button.draw(self.window)

    def is_level_button_clicked(self, pos):
        for button in (self.easy_button, self.medium_button, self.hard_button):
            if button.is_clicked(pos):
                self.level = button.level
                return True
        
    def draw_new_game_button(self):
        self.new_game_button.draw(self.window)

    def is_new_game_button_clicked(self, pos):
        if self.new_game_button.is_clicked(pos):
            return True
        
    def draw_solve_button(self):
        self.solve_button.draw(self.window)

    def is_solve_button_clicked(self, pos):
        if self.solve_button.is_clicked(pos):
            return True

    def count_time(self):
        current_time = time.time() - self.start
        min, sec = divmod(current_time, 60)
        return f'{int(min):02}:{int(sec):02}'

    def draw_time(self):
        formatted_time = self.count_time()
        self.draw_text(f'Time: {formatted_time}', (SudokuBoard.WIDTH * 0.2, SudokuBoard.HEIGHT * 0.89), color=(0, 0, 0), background=(240, 240, 240))

    def nums_not_to_change(self, grid):
        for r, row in enumerate(grid):
            for c, col in enumerate(row):
                if col != 0:
                    grid[r][c] = (col, True)
                else:
                    grid[r][c] = (col, False)
        return grid

    def is_mistake(self, num, row, col):
        return num != self.solution[row][col]
    
    def manage_mistakes(self):
        self.mistakes += 1
        if self.mistakes == 3:
            self.loss = True

    def is_solved(self):
        for r, row in enumerate(self.sudoku_grid):
            for c, value in enumerate(row):
                if value[0] != self.solution[r][c]:
                    return False
        self.solved = True
        self.final_time = self.count_time()
        return True
    
    def draw_mistakes(self):
        self.draw_text(f'Mistakes: {self.mistakes} / {3}', (SudokuBoard.WIDTH * 0.5, SudokuBoard.HEIGHT * 0.89), color=(0, 0, 0))

    def draw_result(self):
        if self.solved:
            self.draw_text(f'Great Job!!! Your time is {self.final_time}', (SudokuBoard.WIDTH * 0.5, SudokuBoard.HEIGHT * 0.8), color=(0, 0, 0))
        else:
            self.draw_text(f'You failed', (SudokuBoard.WIDTH * 0.5, SudokuBoard.HEIGHT * 0.8), color=(0, 0, 0))

    def board_before_game(self):
        self.window.fill((240, 240, 240))
        self.board.draw_board()
        self.draw_level_buttons()

    def board_during_game(self):
        self.window.fill((240, 240, 240))
        if isinstance(self.row, int) :
            pygame.draw.rect(self.window, 'light blue', (self.col * self.board.BOX_X + self.board.BOARD_LEN + 1, self.row * self.board.BOX_Y + self.board.BOARD_TOP + 0.5, SudokuBoard.BOX_X, SudokuBoard.BOX_Y))
        self.board.draw_board()
        self.board.show_numbers(self.sudoku_grid)
        self.draw_mistakes()
        self.draw_time()
        self.draw_solve_button()

    def board_after_game(self):
        self.window.fill((240, 240, 240))
        self.board.draw_board()
        self.board.show_solution(self.sudoku_grid, self.solution)
        self.draw_result()
        self.draw_new_game_button()

    def run(self):
        while self.running:

            if self.solved or self.loss:
                self.board_after_game()
            elif self.level:
               self.board_during_game()
            elif not self.level:
                self.board_before_game()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    
                    if self.level == False:
                        if self.is_level_button_clicked((x, y)):
                            self.get_new_sudoku()

                    elif self.loss or self.solved:
                        if self.is_new_game_button_clicked((x, y)):
                            self.loss = self.solved = self.level = False
                        
                    else:
                        if self.is_solve_button_clicked((x, y)):
                            self.loss = True
                            
                        elif self.board.BOARD_LEN < x < self.board.BOARD_LEN + self.board.BOARD_X and self.board.BOARD_TOP < y < self.board.BOARD_TOP + self.board.BOARD_Y:
                            self.row = int(((y - self.board.BOARD_TOP) // self.board.BOX_Y))
                            self.col = int((x - self.board.BOARD_LEN) // self.board.BOX_X)

                if event.type == pygame.KEYDOWN:
                    if event.unicode.isdigit() and 1 <= int(event.unicode) <= 9 and self.loss == False and self.level:
                        
                        if self.sudoku_grid[self.row][self.col][1] in (False, 'red'):
                            num = int(event.unicode)
                            
                            if not self.is_mistake(num, self.row, self.col):
                                self.sudoku_grid[self.row][self.col] = (num, True)    
                            else:
                                self.sudoku_grid[self.row][self.col] = (num, 'red')
                                self.manage_mistakes()
                
                        self.is_solved()
            pygame.display.update()
        pygame.quit()

if __name__ == '__main__':
    game = SudokuGame()
    game.run()