"""
N-Queens Game - GUI Module
This module contains the graphical user interface for the N-Queens game.
"""
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from PIL import ImageTk, Image
import numpy as np
import time

from board import Board
from alpabeta import AlphaBetaAI

class NQueensGUI:
    def __init__(self, root):
        """
        Initialize the N-Queens GUI.
        
        Args:
            root: The tkinter root window
        """
        self.root = root
        self.cell_size = 50
        
        # Ask for board size
        self.n = simpledialog.askinteger("N-Queens Game", "Enter the size of the board:", 
                                         minvalue=4, maxvalue=12)
        if self.n is None:
            self.n = 8  # Default size if dialog is cancelled
            
        # Initialize board and AI
        self.board = Board(self.n)
        self.ai = AlphaBetaAI(self.board)
        
        # Set up the main frame
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left frame for board
        self.left_frame = tk.Frame(self.main_frame)
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Set up the canvas
        self.canvas = tk.Canvas(self.left_frame, width=self.n * self.cell_size, 
                               height=self.n * self.cell_size)
        self.canvas.pack()
        
        # Right frame for info and controls
        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.Y)
        
        # AI settings frame
        self.ai_frame = tk.LabelFrame(self.right_frame, text="AI Settings", padx=5, pady=5)
        self.ai_frame.pack(fill=tk.X, pady=5)
        
        # AI depth setting
        self.depth_frame = tk.Frame(self.ai_frame)
        self.depth_frame.pack(fill=tk.X, pady=2)
        
        tk.Label(self.depth_frame, text="Search Depth:").pack(side=tk.LEFT)
        self.depth_var = tk.IntVar(value=4)
        self.depth_scale = tk.Scale(self.depth_frame, from_=1, to=6, orient=tk.HORIZONTAL,
                                   variable=self.depth_var, command=self.update_ai_depth)
        self.depth_scale.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        # AI stats frame
        self.stats_frame = tk.LabelFrame(self.right_frame, text="AI Statistics", padx=5, pady=5)
        self.stats_frame.pack(fill=tk.X, pady=5)
        
        self.nodes_var = tk.StringVar(value="Nodes evaluated: 0")
        self.time_var = tk.StringVar(value="Search time: 0.00 s")
        self.nps_var = tk.StringVar(value="Nodes/second: 0")
        
        tk.Label(self.stats_frame, textvariable=self.nodes_var).pack(anchor=tk.W)
        tk.Label(self.stats_frame, textvariable=self.time_var).pack(anchor=tk.W)
        tk.Label(self.stats_frame, textvariable=self.nps_var).pack(anchor=tk.W)
        
        # Game info frame
        self.info_frame = tk.LabelFrame(self.right_frame, text="Game Info", padx=5, pady=5)
        self.info_frame.pack(fill=tk.X, pady=5)
        
        self.queens_var = tk.StringVar(value=f"Queens left: {self.board.queens_left}")
        tk.Label(self.info_frame, textvariable=self.queens_var).pack(anchor=tk.W)
        
        # Add control buttons
        self.controls_frame = tk.Frame(self.right_frame)
        self.controls_frame.pack(fill=tk.X, pady=10)
        
        self.reset_button = tk.Button(self.controls_frame, text="Reset Game", 
                                     command=self.reset_game)
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        self.hint_button = tk.Button(self.controls_frame, text="Get Hint", 
                                    command=self.show_hint)
        self.hint_button.pack(side=tk.LEFT, padx=5)
        
        self.quit_button = tk.Button(self.controls_frame, text="Quit", 
                                    command=root.destroy)
        self.quit_button.pack(side=tk.RIGHT, padx=5)
        
        # Status label
        self.status_var = tk.StringVar()
        self.status_var.set("Place queens on the board. Click to make your move.")
        self.status_label = tk.Label(root, textvariable=self.status_var, 
                                    bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
        
        # Load the queen image
        self.load_queen_image()
        
        # Draw the initial board
        self.draw_board()
        
        # Highlight hint (if any)
        self.hint_highlight = None
        
        # Bind click event
        self.canvas.bind("<Button-1>", self.on_board_click)
        
    def load_queen_image(self):
        """
        Load the queen image for the board.
        """
        # Check if images directory exists
        if not os.path.exists("images"):
            os.makedirs("images")
            
        # Check if Queen.jpg exists, if not create a placeholder
        if not os.path.exists("images/Queen.jpg"):
            # Create a placeholder image with a simple queen symbol
            img = Image.new('RGB', (self.cell_size, self.cell_size), color = (255, 255, 255))
            self.queen_photo = ImageTk.PhotoImage(img)
            print("Warning: Queen.jpg not found. Using placeholder image.")
        else:
            # Load the actual queen image
            queen_image = Image.open("images/Queen.jpg")
            queen_image = queen_image.resize((self.cell_size, self.cell_size), Image.LANCZOS)
            self.queen_photo = ImageTk.PhotoImage(queen_image)
    
    def draw_board(self):
        """
        Draw the chess board and queens.
        """
        self.canvas.delete("all")
        
        # Draw the chess board
        for row in range(self.n):
            for col in range(self.n):
                color = 'white' if (row + col) % 2 == 0 else 'gray'
                self.canvas.create_rectangle(
                    col * self.cell_size, row * self.cell_size, 
                    (col + 1) * self.cell_size, (row + 1) * self.cell_size,
                    fill=color, tags=f"cell_{row}_{col}"
                )
        
        # Place the queens on the board
        for i in range(self.n):
            for j in range(self.n):
                if self.board.board[i, j] == 1:
                    self.canvas.create_image(
                        j * self.cell_size, i * self.cell_size, 
                        anchor='nw', image=self.queen_photo
                    )
        
        # Update the game info
        self.queens_var.set(f"Queens left: {self.board.queens_left}")
        
    def on_board_click(self, event):
        """
        Handle board click event.
        
        Args:
            event: The mouse click event
        """
        # Clear any hint highlight
        if self.hint_highlight:
            self.draw_board()
            self.hint_highlight = None
        
        if self.board.is_game_over():  # Game already over
            messagebox.showinfo("Game Over", "Game is already finished! Reset to play again.")
            return
        
        # Calculate the clicked cell
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        
        if self.board.queens_left > 0:
            if self.board.board[row, col] == 0:
                if self.board.is_safe(row, col):
                    # Place the queen
                    self.board.place_queen(row, col)
                    self.draw_board()
                    self.status_var.set(f"Queen placed at position ({row}, {col}).")
                    
                    # Check if game is over
                    if self.board.is_game_over():
                        messagebox.showinfo("Game Over", "You placed all the queens!")
                    else:
                        # AI's turn
                        self.make_ai_move()
                else:
                    self.status_var.set("Invalid move! Position is under attack.")
        else:
            messagebox.showinfo("Game Over", "No more queens left to place!")
    
    def make_ai_move(self):
        """
        Make the AI's move.
        """
        self.status_var.set("AI is thinking...")
        self.root.update_idletasks()
        
        # Get the best move from the AI
        move, stats = self.ai.get_best_move()
        
        # Update AI stats
        self.nodes_var.set(f"Nodes evaluated: {stats['nodes_evaluated']}")
        self.time_var.set(f"Search time: {stats['search_time']:.2f} s")
        self.nps_var.set(f"Nodes/second: {int(stats['nodes_per_second'])}")
        
        if move is None:  # No valid moves left
            if self.board.is_game_over():
                messagebox.showinfo("Game Over", "All queens placed successfully!")
            else:
                messagebox.showinfo("Game Over", "No safe positions left!")
            return
        
        row, col = move
        self.board.place_queen(row, col)
        self.draw_board()
        self.status_var.set(f"AI placed a queen at position ({row}, {col}).")
        
        if self.board.is_game_over():
            messagebox.showinfo("Game Over", "All queens placed successfully!")
    
    def show_hint(self):
        """
        Show a hint for the player by highlighting the best move.
        """
        if self.board.is_game_over():
            messagebox.showinfo("Game Over", "Game is already finished!")
            return
            
        move, stats = self.ai.get_best_move()
        
        # Update AI stats
        self.nodes_var.set(f"Nodes evaluated: {stats['nodes_evaluated']}")
        self.time_var.set(f"Search time: {stats['search_time']:.2f} s")
        self.nps_var.set(f"Nodes/second: {int(stats['nodes_per_second'])}")
        
        if move is None:
            messagebox.showinfo("Hint", "No safe moves available!")
            return
            
        row, col = move
        
        # Highlight the suggested move
        self.hint_highlight = (row, col)
        cell_id = f"cell_{row}_{col}"
        self.canvas.itemconfig(cell_id, fill="light green")
        self.status_var.set(f"Hint: Try placing a queen at position ({row}, {col}).")
    
    def update_ai_depth(self, *args):
        """
        Update the AI search depth.
        """
        new_depth = self.depth_var.get()
        self.ai.max_depth = new_depth
        self.status_var.set(f"AI search depth set to {new_depth}")
    
    def reset_game(self):
        """
        Reset the game with a new board size.
        """
        new_size = simpledialog.askinteger("N-Queens Game", "Enter the size of the board:", 
                                         minvalue=4, maxvalue=12, initialvalue=self.n)
        if new_size is not None:
            self.n = new_size
            self.board.reset(new_size)
            self.ai = AlphaBetaAI(self.board)
            
            # Resize the canvas
            self.canvas.config(width=self.n * self.cell_size, height=self.n * self.cell_size)
            
            # Reset AI stats
            self.nodes_var.set("Nodes evaluated: 0")
            self.time_var.set("Search time: 0.00 s")
            self.nps_var.set("Nodes/second: 0")
            
            # Clear any hint highlight
            self.hint_highlight = None
            
            # Redraw the board
            self.draw_board()
            self.status_var.set("Game reset. Place queens on the board.")