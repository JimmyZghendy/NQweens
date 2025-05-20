"""
N-Queens Game - Alpha-Beta Search Module
This module contains the AI logic using the alpha-beta pruning algorithm.
"""
import numpy as np
import time

class AlphaBetaAI:
    def __init__(self, board, max_depth=4):
        """
        Initialize the Alpha-Beta AI with a board.
        
        Args:
            board: The Board object
            max_depth: Maximum search depth
        """
        self.board = board
        self.max_depth = max_depth
        self.nodes_evaluated = 0
        self.search_time = 0
        
    def alpha_beta_search(self, depth, alpha, beta, is_maximizing_player):
        """
        Alpha-Beta pruning algorithm.
        
        Args:
            depth (int): Current depth in the game tree
            alpha (float): Alpha value for pruning
            beta (float): Beta value for pruning
            is_maximizing_player (bool): True if current player is maximizing
            
        Returns:
            float: The evaluation score
        """
        self.nodes_evaluated += 1
        
        # Terminal conditions
        if depth == 0 or self.board.is_game_over():
            return self.board.evaluate()
        
        safe_positions = self.board.get_safe_positions()
        
        # If no valid moves, return evaluation
        if not safe_positions:
            return self.board.evaluate()
        
        if is_maximizing_player:
            max_eval = float('-inf')
            for i, j in safe_positions:
                # Make move
                self.board.board[i, j] = 1
                self.board.queens_left -= 1
                
                # Recursive evaluation
                eval_score = self.alpha_beta_search(depth - 1, alpha, beta, False)
                
                # Undo move
                self.board.board[i, j] = 0
                self.board.queens_left += 1
                
                # Update best score and alpha
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                
                # Alpha-Beta pruning
                if beta <= alpha:
                    break
                    
            return max_eval
        else:
            min_eval = float('inf')
            for i, j in safe_positions:
                # Make move
                self.board.board[i, j] = 1
                self.board.queens_left -= 1
                
                # Recursive evaluation
                eval_score = self.alpha_beta_search(depth - 1, alpha, beta, True)
                
                # Undo move
                self.board.board[i, j] = 0
                self.board.queens_left += 1
                
                # Update best score and beta
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                
                # Alpha-Beta pruning
                if beta <= alpha:
                    break
                    
            return min_eval
        
    def get_best_move(self):
        """
        Find the best move for the AI using alpha-beta pruning.
        
        Returns:
            tuple: (row, col) or None if no valid moves
            dict: Statistics about the search
        """
        start_time = time.time()
        self.nodes_evaluated = 0
        
        safe_positions = self.board.get_safe_positions()
        
        # If no valid moves, return None
        if not safe_positions:
            self.search_time = time.time() - start_time
            return None, self._get_stats()
        
        best_score = float('-inf')
        best_move = None
        
        # Try each valid move and choose the one with highest score
        for i, j in safe_positions:
            # Make move
            self.board.board[i, j] = 1
            self.board.queens_left -= 1
            
            # Evaluate with alpha-beta
            score = self.alpha_beta_search(
                self.max_depth, float('-inf'), float('inf'), False
            )
            
            # Undo move
            self.board.board[i, j] = 0
            self.board.queens_left += 1
            
            # Update best move
            if score > best_score:
                best_score = score
                best_move = (i, j)
        
        self.search_time = time.time() - start_time
        return best_move, self._get_stats()
    
    def _get_stats(self):
        """
        Get statistics about the last search.
        
        Returns:
            dict: Search statistics
        """
        return {
            'nodes_evaluated': self.nodes_evaluated,
            'search_time': self.search_time,
            'nodes_per_second': self.nodes_evaluated / max(0.001, self.search_time)
        }