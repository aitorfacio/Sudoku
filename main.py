from PyQt6.QtWidgets import QMainWindow, QGridLayout, QLineEdit, QApplication, QWidget, QPushButton
from PyQt6.QtCore import QObject, pyqtSlot,pyqtSignal
from math import sqrt
import sys


def string_to_sudoku(sudoku):
    size = int(sqrt(len(sudoku)+1))
    result = [[int(x) if int(x) != 0 else None for x in sudoku[s*size: s*size+size]] for s in range(size)]
    return result


class SudokuSolver(object):
    def __init__(self, board):
        self.size = len(board)
        self.square_size = int(sqrt(self.size))
        self.board = board
        self.empty_cells = [(i,j) for i in range(self.size) for j in range(self.size) if not self.board[i][j]]
        self.visited = []

    def __str__(self):
        return "\n".join([" ".join(str(x) for x in y) for y in self.board])

    def __repr__(self):
        return str(self)

    def _square(self, row, col):
        x = col * self.square_size
        y = row * self.square_size
        square = []
        for i in range(y, y + self.square_size):
            row = []
            for j in range(x, x + self.square_size):
                row.append(self.board[i][j])
            square.append(row)
        return square

    def _next_cell(self):
        for cell in self.empty_cells:
            if cell not in self.visited:
                yield cell
        yield None

    def _square_containing(self,i,j):
        center_row = (i//self.square_size) * self.square_size + 1
        center_col = (j//self.square_size) * self.square_size + 1
        return center_row, center_col

    def _backtracking_solve(self):
        if len(self.visited) == len(self.empty_cells):
            #no cell left to visit
            return True

        for next_cell in self._next_cell():
            i, j = next_cell
            for value in range(1, self.size+1):
                if self.feasible(i, j, value):
                    self.board[i][j] = value
                    self.visited.append((i,j))
                    if self._backtracking_solve():
                        return True
                    else:
                        self.board[i][j] = None
                        self.visited.remove((i,j))
            return False

    def solve(self):
        return self._backtracking_solve()

    def feasible(self, i, j, value):
        row_feasible = value not in self.board[i]
        col_feasible = value not in [self.board[y][j] for y in range(self.size)]
        x, y = self._square_containing(i, j)
        square_feasible = [self.board[x-1][y-1:y+2], self.board[x][y-1:y+2], self.board[x+1][y-1:y+2]]
        square_feasible = value not in [y for x in square_feasible for y in x]
        return row_feasible and col_feasible and square_feasible

    def is_solution(self):
        '''assumes dimensions are correct'''
        must_match = list(range(1,self.size+1))

        #check rows
        for r in range(self.size):
            if not sorted(self.board[r].copy()) == must_match:
                print(f"Row {r}: {self.board[r]} No solution")
                return False

        #check cols
        for c in range(self.size):
            col = []
            for r in range(self.size):
                col.append(self.board[r][c])

            if not sorted(col) == must_match:
                print(f"Col {c}: {col} No solution")
                return False

        #check squares
        #there are square_size X square_size squares
        for r in range(self.square_size):
            for c in range(self.square_size):
                flattened_square = [y for x in self._square(r, c) for y in x]
                if not(sorted(flattened_square)) == must_match:
                    return False
        return True


class SudokuBoard(QObject):
    board_incorrect = pyqtSignal()
    board_ok = pyqtSignal()

    def __init__(self, parent=None, size=9):
        self.board = [[0 for x in range(size)] for m in range(size)]

    @pyqtSlot(int, int, int)
    def set_cell(self, row, col, value):
        self.board[row][col] = value


class SudokuWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid_size = 9
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.widget = []
        self.draw_grid()

    def draw_grid(self):
        for i in range(self.grid_size):
            self.widget.append([])
            for j in range(self.grid_size):
                self.widget[i].append(QLineEdit(self))
                self.widget[i][j].setText(str(j+1))
                self.grid.addWidget(self.widget[i][j], i, j)


if __name__ == '__main__':
    #app = QApplication(sys.argv)
    #window = SudokuWindow()
    #window.show()

    #sys.exit(app.exec())
    #app = QApplication(sys.argv)
    #widget = QWidget()
    #layout = QGridLayout()

    #buttons = {}

    #for i in range(10):
    #    for j in range(10):
    #        # keep a reference to the buttons
    #        buttons[(i, j)] = QPushButton('row %d, col %d' % (i, j))
    #        buttons[(i,j)] = QLineEdit()
    #        # add to the layout
    #        layout.addWidget(buttons[(i, j)], i, j)

    #widget.setLayout(layout)
    #widget.show()
    #sys.exit(app.exec())

    sudoku_1 = [
        [7,5,9,4,6,2,8,1,3],
        [4,6,3,5,1,8,2,9,7],
        [1,2,8,9,7,3,6,4,5],
        [6,9,7,1,8,4,5,3,2],
        [5,8,4,2,3,6,9,7,1],
        [2,3,1,7,9,5,4,8,6],
        [3,4,5,8,2,1,7,6,9],
        [9,1,2,6,4,7,3,5,8],
        [8,7,6,3,5,9,1,2,4]
    ]
    sudoku_2 = [
        [4,3,5,2,6,9,7,8,1],
        [6,8,2,5,7,1,4,9,3],
        [1,9,7,8,3,4,5,6,2],
        [8,2,6,1,9,5,3,4,7],
        [3,7,4,6,8,2,9,1,5],
        [9,5,1,7,4,3,6,2,8],
        [5,1,9,3,2,6,8,7,4],
        [2,4,8,9,5,7,1,3,6],
        [7,6,3,4,1,8,2,5,9],
    ]
    solver1 = SudokuSolver(sudoku_1)
    solver2 = SudokuSolver(sudoku_2)

    sudoku_exercise_1 = [
        [None, None, None, 2, 6, None, 7, None, 1],
        [6, 8, None, None, 7, None, None, 9, None],
        [1, 9, None, None, None, 4, 5, None, None],
        [8, 2, None, 1, None, None, None, 4, None],
        [None, None, 4, 6, None, 2, 9, None, None],
        [None, 5, None, None, None, 3, None, 2, 8],
        [None, None, 9, 3, None, None, None, 7, 4],
        [None, 4, None, None, 5, None, None, 3, 6],
        [7, None, 3, None, 1, 8, None, None, None],
    ]
    sudoku_solution_1 = [
        [4, 3, 5, 2, 6, 9, 7, 8, 1],
        [6, 8, 2, 5, 7, 1, 4, 9, 3],
        [1, 9, 7, 8, 3, 4, 5, 6, 2],
        [8, 2, 6, 1, 9, 5, 3, 4, 7],
        [3, 7, 4, 6, 8, 2, 9, 1, 5],
        [9, 5, 1, 7, 4, 3, 6, 2, 8],
        [5, 1, 9, 3, 2, 6, 8, 7, 4],
        [2, 4, 8, 9, 5, 7, 1, 3, 6],
        [7, 6, 3, 4, 1, 8, 2, 5, 9],
    ]

    sudoku_exercise_2 = [
        [1, None, None, 4, 8, 9, None, None, 6],
        [7, 3, None, None, None, None, None, 4, None],
        [None, None, None, None, None, 1, 2, 9, 5],
        [None, None, 7, 1, 2, None, 6, None, None],
        [5, None, None, 7, None, 3, None, None, 8],
        [None, None, 6, None, 9, 5, 7, None, None],
        [9, 1, 4, 6, None, None, None, None, None],
        [None, 2, None, None, None, None, None,3, 7 ],
        [8, None, None, 5, 1, 2, None, None, 4],
    ]

    sudoku_solution_2 = [
        [1, 5, 2, 4, 8, 9, 3, 7, 6],
        [7, 3, 9, 2, 5, 6, 8, 4, 1],
        [4, 6, 8, 3, 7, 1, 2, 9, 5],
        [3, 8, 7, 1, 2, 4, 6, 5, 9],
        [5, 9, 1, 7, 6, 3, 4, 2, 8],
        [2, 4, 6, 8, 9, 5, 7, 1, 3],
        [9, 1, 4, 6, 3, 7, 5, 8, 2],
        [6, 2, 5, 9, 4, 8, 1, 3, 7],
        [8, 7, 3, 5, 1, 2, 9, 6, 4],
    ]
    sudoku_exercise_3 = "400701003005000200060003040078600900000050000004002180010800020002000300800205004"
    sudoku_exercise_3 = string_to_sudoku(sudoku_exercise_3)

    solver3 = SudokuSolver(sudoku_exercise_1)
    solver3.solve()
    solver4 = SudokuSolver(sudoku_exercise_2)
    solver4.solve()
    solver5 = SudokuSolver(sudoku_exercise_3)
    solved = solver5.solve()
    assert (solver1.is_solution())
    assert (solver2.is_solution())
    assert (solver3.is_solution())
    assert (solver3.board == sudoku_solution_1)
    assert (solver4.is_solution())
    assert (solver4.board == sudoku_solution_2)
    assert (solver5.is_solution())
