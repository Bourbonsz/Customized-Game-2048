import copy
import random

# Game logic class
class Matrix2048():
    def __init__(self, column: int = 4):
        self.column = column
        self.matrix = [[0 for i in range(column)] for li in range(column)]
        self.history = []
        self.score = 0
        self.init()

    # Generate a new number
    def generate_number(self):
        matrix = self.matrix
        column = self.column
        # Find all positions with 0
        zero = [(x, y) for x in range(column)
                for y in range(column) if matrix[x][y] == 0]
        # Randomly choose a position with 0 and fill it with a random number
        if zero != []:
            x, y = random.choice(zero)
            matrix[x][y] = random.choice([2, 2])

    # Check if the game is over, return True if over, otherwise return False
    def gameover(self) -> bool:
        matrix = self.matrix
        column = self.column
        # 1. If there is a 0 in the matrix (self.matrix), the game is not over
        if 0 in [i for li in matrix for i in li]:
            return False

        # 2. If there are the same numbers in a horizontal direction, the game is not over
        for row in range(column):
            for col in range(column-1):
                if matrix[row][col] == matrix[row][col+1]:
                    return False

        # 3. If there are the same numbers in a vertical direction, the game is not over
        for row in range(column-1):
            for col in range(column):
                if matrix[row][col] == matrix[row+1][col]:
                    return False
        return True

    # Initialize the game
    def init(self):
        self.matrix = [[0 for x in range(self.column)]
                       for y in range(self.column)]
        self.generate_number()
        self.generate_number()

        self.history = []
        self.score = 0

    # Move and merge cells, and record the historical data
    def matrix_move(self, direction):
        if direction in ['L', 'R', 'D', 'U']:

            # Record history
            prev_step = {
                'score': copy.deepcopy(self.score),
                'matrix': copy.deepcopy(self.matrix)
            }
            self.history.append(prev_step)
            # Keep only the latest 10 steps
            if len(self.history) > 10:
                self.history = self.history[-10:]
            if direction == 'U':
                self.move_up()
            if direction == 'D':
                self.move_down()
            if direction == 'L':
                self.move_left()
            if direction == 'R':
                self.move_right()

    # Move and merge cells to the left
    def move_left(self):
        column = self.column
        matrix = self.matrix

        # Move numbers to the left
        def move_left_(matrix):
            for row in range(column):
                while 0 in matrix[row]:
                    matrix[row].remove(0)
                while len(matrix[row]) != column:
                    matrix[row].append(0)
            return matrix

        # Merge numbers to the left
        def merge_left(matrix):
            for row in range(column):
                for col in range(column-1):
                    if matrix[row][col] == matrix[row][col+1] and matrix[row][col] != 0:
                        matrix[row][col] = 2 * matrix[row][col]
                        matrix[row][col+1] = 0
                        self.score = self.score + matrix[row][col]
            return matrix

        matrix = move_left_(matrix)
        matrix = merge_left(matrix)
        self.matrix = move_left_(matrix)

    # Move and merge cells to the right
    def move_right(self):
        self.matrix = [li[::-1] for li in self.matrix]
        self.move_left()
        self.matrix = [li[::-1] for li in self.matrix]

    # Move and merge cells upward
    def move_up(self):
        column = self.column

        self.matrix = [[self.matrix[x][y]
                        for x in range(column)] for y in range(column)]
        self.move_left()
        self.matrix = [[self.matrix[x][y]
                        for x in range(column)] for y in range(column)]

    # Move and merge cells downward
    def move_down(self):
        self.matrix = self.matrix[::-1]
        self.move_up()
        self.matrix = self.matrix[::-1]

    # Go back to the previous step
    def prev_step(self):
        if self.history:
            prev_data = self.history[-1]
            self.score = prev_data['score']
            self.matrix = prev_data['matrix']
            self.history = self.history[0:-1]
