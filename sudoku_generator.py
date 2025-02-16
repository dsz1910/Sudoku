from random import choice, sample, randint
from time import perf_counter
import sys


sys.setrecursionlimit(1500)
class SudokuGridMaker:

    def __init__(self, level) -> None:
        self.level = level
        self.solution = self.fill_grid()
        self.grid = self.sudoku_puzzle()

    @property
    def level(self):
        return self._level
    
    @level.setter
    def level(self, val):
        if val in ('hard', 'easy', 'medium'):
            self._level = val

    @property
    def solution(self):
        return self._solution
    
    @solution.setter
    def solution(self, val):
        if isinstance(val, list) and all(isinstance(x, list) for x in val) and len(val) == 9 and all(len(x) == 9 for x in val) \
            and all([isinstance(x, int) and 0 < x < 10 for x in y] for y in val):
            self._solution = val

    @property
    def grid(self):
        return self._grid
    
    @grid.setter
    def grid(self, val):
        if isinstance(val, list) and all(isinstance(x, list) for x in val) and len(val) == 9 and all(len(x) == 9 for x in val) \
            and all([isinstance(x, int) and 0 <= x < 10 for x in y] for y in val):
            self._grid = val

    @staticmethod
    def deep_copy(grid):   # makes and returns deepcopy of grid
        return [[el for el in row] for row in grid]

    @staticmethod
    def get_next(row, col):         # returns next position
        if col < 8:
            return row, col + 1
        return row + 1, 0

    @staticmethod
    def get_previous(row, col):     # returns previous position
        if col > 0:
            return row, col - 1
        return row - 1, 8

    @classmethod
    def empty_cells_count(cls, level):
        if level == 'hard': return randint(50, 54)
        if level =='medium': return randint(41, 49)
        return randint(32, 40)

    def check_nums(self, grid, row, col):
        not_used = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        for r in range(3 * (row // 3), 3 * (row // 3) + 3):           # checking which numbers have been used in 3x3 square yet
            for c in range(3 * (col // 3), 3 * (col // 3) + 3):
                if grid[r][c] in not_used and grid[r][c] != 0:
                    not_used.remove(grid[r][c])

        for i in range(9):                       # checking which numbers have been used in row and column
            if grid[i][col] in not_used:
                not_used.remove(grid[i][col])
            if grid[row][i] in not_used:
                not_used.remove(grid[row][i])
        
        return not_used

    def choose_num(self, grid, row, col):      # chooses number to add into the grid
        not_used = self.check_nums(grid, row, col)
        if not not_used:
            return 0
        return choice(not_used)

    def fill_grid(self):  # returns filled sudoku grid which is our solution
        grid = [sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 9)] + [[0] * 9 for _ in range(8)]
        row = 1
        col = 0
        arr = [(0, 5), (0, 6), (0, 7), (0, 8)]

        while row < 9:
            num = self.choose_num(grid, row, col)
            if num:
                grid[row][col] = num
                row, col = self.get_next(row, col)
            else:
                row, col = self.get_previous(row, col)

            arr.append((row, col))
            if arr[-1] == arr[-5]:
                return self.fill_grid()
                
        return grid

    def sudoku_solutions_counter(self, grid, row=0, col=0, solutions=0): # checks grids uniqueness
        if row == 9:    # if row == 9 it means we found solution so we increment and return solutions
            return solutions + 1
        
        if grid[row][col] != 0:
            next_row, next_col = self.get_next(row, col) 
            return self.sudoku_solutions_counter(grid, next_row, next_col, solutions)    # if number is 0 we move to the next position
                
        not_used = self.check_nums(grid, row, col)    # if there is no fitting numbers there is no solution
        if not not_used:
            return solutions
            
        for num in not_used:  # we check all numbers which can be adden into this position
            grid[row][col] = num
            next_row, next_col = self.get_next(row, col)
            solutions = self.sudoku_solutions_counter(grid, next_row, next_col, solutions)
            grid[row][col] = 0

            if solutions > 1:   #if there is more than one solution then grid is not unique
                return solutions
                
        if solutions > 0:
            return solutions
        return 0

    def sudoku_puzzle(self):   #creates puzzle
        grid = self.deep_copy(self.solution)
        to_remove = self.empty_cells_count(self.level)

        while to_remove > 0:
            row, col = (randint(0, 8), randint(0, 8))
            if grid[row][col] == 0:
                continue

            removed = grid[row][col]
            grid[row][col] = 0
            #grid_copy = self.deep_copy(grid)

            if self.sudoku_solutions_counter(grid) == 1:
                to_remove -= 1
            else:
                grid[row][col] = removed
                
        return grid

def main():
    start = perf_counter()
    sudoku = SudokuGridMaker('hard')
    end = perf_counter()

    for row in sudoku.grid:
        print(row)
    print('\n')
    for row in sudoku.solution:
        print(row)
    print(end - start)

if __name__ == '__main__':
    main()