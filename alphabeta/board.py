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
    
    def get_safe_positions(self):
        """
        Get all safe positions on the board for placing a queen.
        
        Returns:
            list: List of tuples (row, col) for all safe positions
        """
        safe_positions = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i, j] == 0 and self.is_safe(i, j):
                    safe_positions.append((i, j))
        return safe_positions
        
    def evaluate(self):
        """
        Evaluate the current board state for the alpha-beta algorithm.
        
        Returns:
            int: A heuristic value representing the board state quality
        """
        n = self.size
        queens_placed = n - self.queens_left
        
        # If all queens are placed successfully, this is the best outcome
        if queens_placed == n:
            return 1000
            
        # Count the number of safe positions remaining
        safe_positions = len(self.get_safe_positions())
        
        # If we have no safe positions left but haven't placed all queens, bad position
        if safe_positions == 0 and queens_placed < n:
            return -1000
            
        # Otherwise, the score is based on queens placed and safe positions available
        return queens_placed * 10 + safe_positions
        
    def is_game_over(self):
        """
        Check if the game is over (all queens placed).
        
        Returns:
            bool: True if game is over, False otherwise
        """
        return self.queens_left == 0
        
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