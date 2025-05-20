"""
N-Queens Game - Main Module
This is the entry point for the N-Queens game application with Alpha-Beta pruning AI.
"""
import tkinter as tk
from gui import NQueensGUI

def main():
    """
    Main function to start the N-Queens game.
    """
    # Create the main window
    root = tk.Tk()
    root.title("N-Queens Game with Alpha-Beta AI")
    
    # Initialize the game GUI
    app = NQueensGUI(root)
    
    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    main()