"""
N-Queens Game - GUI Module
This module contains the graphical user interface for the N-Queens game.
"""
import os
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import ImageTk, Image
import numpy as np

from board import Board
from minimax import MinimaxAI

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
        self.ai = MinimaxAI(self.board)
        
        # Set up the canvas
        self.canvas = tk.Canvas(root, width=self.n * self.cell_size, 
                               height=self.n * self.cell_size)
        self.canvas.pack(padx=10, pady=10)
        
        # Add control buttons
        self.controls_frame = tk.Frame(root)
        self.controls_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.reset_button = tk.Button(self.controls_frame, text="Reset Game", 
                                     command=self.reset_game)
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        self.quit_button = tk.Button(self.controls_frame, text="Quit", 
                                    command=root.destroy)
        self.quit_button.pack(side=tk.RIGHT, padx=5)
        
        # Status label
        self.status_var = tk.StringVar()
        self.status_var.set(f"Queens left to place: {self.board.queens_left}")
        self.status_label = tk.Label(root, textvariable=self.status_var, 
                                    bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
        
        # Load the queen image
        self.load_queen_image()
        
        # Draw the initial board
        self.draw_board()
        
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
                    fill=color
                )
        
        # Place the queens on the board
        for i in range(self.n):
            for j in range(self.n):
                if self.board.board[i, j] == 1:
                    self.canvas.create_image(
                        j * self.cell_size, i * self.cell_size, 
                        anchor='nw', image=self.queen_photo
                    )
        
        # Update the status
        self.status_var.set(f"Queens left to place: {self.board.queens_left}")
        
    def on_board_click(self, event):
        """
        Handle board click event.
        
        Args:
            event: The mouse click event
        """
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
                    
                    # Check if game is over
                    if self.board.is_game_over():
                        messagebox.showinfo("Game Over", "You placed all the queens!")
                    else:
                        # AI's turn
                        self.make_ai_move()
                else:
                    messagebox.showwarning("Invalid Move", "The position is unsafe. Try again.")
        else:
            messagebox.showinfo("Game Over", "No more queens left to place!")
    
    def make_ai_move(self):
        """
        Make the AI's move.
        """
        move = self.ai.get_best_move()
        if move is None:  # No valid moves left
            if self.board.is_game_over():
                messagebox.showinfo("Game Over", "All queens placed successfully!")
            else:
                messagebox.showinfo("Game Over", "No safe positions left!")
            return
        
        row, col = move
        self.board.place_queen(row, col)
        self.draw_board()
        
        if self.board.is_game_over():
            messagebox.showinfo("Game Over", "All queens placed successfully!")
    
    def reset_game(self):
        """
        Reset the game with a new board size.
        """
        new_size = simpledialog.askinteger("N-Queens Game", "Enter the size of the board:", 
                                         minvalue=4, maxvalue=12, initialvalue=self.n)
        if new_size is not None:
            self.n = new_size
            self.board.reset(new_size)
            self.ai = MinimaxAI(self.board)
            
            # Resize the canvas
            self.canvas.config(width=self.n * self.cell_size, height=self.n * self.cell_size)
            
            # Redraw the board
            self.draw_board()