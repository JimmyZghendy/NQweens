"""
N-Queens Game - Minimax Module
This module contains the AI logic using the minimax algorithm.
"""
import numpy as np

class MinimaxAI:
    def __init__(self, board):
        """
        Initialize the Minimax AI with a board.
        
        Args:
            board: The Board object
        """
        self.board = board
    
    def minimax(self, depth, alpha, beta, is_maximizing_player):
        """
        Minimax algorithm with alpha-beta pruning.
        
        Args:
            depth (int): Current depth in the game tree
            alpha (float): Alpha value for pruning
            beta (float): Beta value for pruning
            is_maximizing_player (bool): True if current player is maximizing
            
        Returns:
            float: The evaluation score
        """
        if depth == 0 or np.sum(self.board.board) == self.board.size:
            return self.board.evaluate()

        if is_maximizing_player:
            max_eval = float('-inf')
            for i in range(self.board.size):
                for j in range(self.board.size):
                    if self.board.board[i, j] == 0 and self.board.is_safe(i, j):
                        self.board.board[i, j] = 1
                        eval = self.minimax(depth - 1, alpha, beta, False)
                        self.board.board[i, j] = 0
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
            return max_eval

        else:
            min_eval = float('inf')
            for i in range(self.board.size):
                for j in range(self.board.size):
                    if self.board.board[i, j] == 0 and self.board.is_safe(i, j):
                        self.board.board[i, j] = 1
                        eval = self.minimax(depth - 1, alpha, beta, True)
                        self.board.board[i, j] = 0
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
            return min_eval
    
    def get_best_move(self):
        """
        Find the best move for the AI.
        
        Returns:
            tuple: (row, col) or None if no valid moves
        """
        best_score = float('-inf')
        best_move = None
        valid_moves = []
        
        # First collect all valid moves
        for i in range(self.board.size):
            for j in range(self.board.size):
                if self.board.board[i, j] == 0 and self.board.is_safe(i, j):
                    valid_moves.append((i, j))
        
        # If no valid moves, return None
        if not valid_moves:
            return None
        
        # Evaluate each valid move
        for i, j in valid_moves:
            self.board.board[i, j] = 1
            score = self.minimax(3, float('-inf'), float('inf'), False)
            self.board.board[i, j] = 0
            if score > best_score:
                best_score = score
                best_move = (i, j)
        
        return best_move