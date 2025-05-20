"""
N-Queens Game - Board Module
This module contains the logic for the game board and queen placement rules.
"""
import numpy as np

class Board:
    def __init__(self, size):
        """
        Initialize the N-Queens board.
        
        Args:
            size (int): The size of the board (n x n)
        """
        self.size = size
        self.board = np.zeros((size, size))
        self.queens_left = size
    
    def reset(self, size=None):
        """
        Reset the board to the initial state.
        
        Args:
            size (int, optional): New size for the board, if None the current size is used.
        """
        if size is not None:
            self.size = size
        self.board = np.zeros((self.size, self.size))
        self.queens_left = self.size
    
    def place_queen(self, row, col):
        """
        Place a queen at the specified position.
        
        Args:
            row (int): Row index
            col (int): Column index
            
        Returns:
            bool: True if queen was successfully placed, False otherwise
        """
        if self.is_safe(row, col):
            self.board[row, col] = 1
            self.queens_left -= 1
            return True
        return False
    
    def is_safe(self, row, col):
        """
        Check if it's safe to place a queen at the specified position.
        
        Args:
            row (int): Row index
            col (int): Column index
            
        Returns:
            bool: True if position is safe, False otherwise
        """
        n = self.size

        # Check if the position is already occupied
        if self.board[row, col] == 1:
            return False

        # Check row and column
        for i in range(n):
            if self.board[row, i] == 1 or self.board[i, col] == 1:
                return False

        # Check diagonals
        for i in range(n):
            for j in range(n):
                if (i + j == row + col) or (i - j == row - col):
                    if self.board[i, j] == 1:
                        return False

        return True
    
    def evaluate(self):
        """
        Evaluate the current board state for the minimax algorithm.
        
        Returns:
            int: Score representing how many conflicts exist
        """
        n = self.size
        score = 0

        # Count the number of queens in each row
        row_counts = np.sum(self.board, axis=1)
        score += np.sum(row_counts > 1)

        # Count the number of queens in each column
        col_counts = np.sum(self.board, axis=0)
        score += np.sum(col_counts > 1)

        # Count the number of queens in each diagonal
        diagonal_counts = []
        for i in range(2 * n - 1):
            diagonal_counts.append(np.sum(np.diagonal(self.board, i - n + 1)))
            diagonal_counts.append(np.sum(np.diagonal(np.fliplr(self.board), i - n + 1)))
        score += np.sum(np.array(diagonal_counts) > 1)

        return score
    
    def is_game_over(self):
        """
        Check if the game is over (all queens placed).
        
        Returns:
            bool: True if game is over, False otherwise
        """
        return np.sum(self.board) == self.size
    
    def print_board(self):
        """
        Print the current board state to the console.
        """
        n = self.size
        for i in range(n):
            for j in range(n):
                if self.board[i, j] == 1:
                    print('Q', end=' ')
                else:
                    print('.', end=' ')
            print()