import numpy as np
from typing import Optional, Tuple

class SudokuGame:
    def __init__(self, difficulty: str = 'medium'):
        """
        Initialize a Sudoku game with specified difficulty.
        
        Args:
            difficulty: 'easy', 'medium', or 'hard'
        """
        self.board = np.zeros((9, 9), dtype=int)
        self.solution = np.zeros((9, 9), dtype=int)
        self.original = np.zeros((9, 9), dtype=bool)  # Which cells are fixed
        self.difficulty = difficulty
        self.generate_puzzle()
    
    def generate_puzzle(self):
        """Generate a new Sudoku puzzle based on difficulty"""
        from .generator import generate_sudoku
        self.board, self.solution = generate_sudoku(self.difficulty)
        self.original = self.board != 0
    
    def is_valid_move(self, row: int, col: int, num: int) -> bool:
        """Check if a number can be placed in the given cell"""
        if self.original[row, col]:
            return False
        
        # Check row
        if num in self.board[row, :]:
            return False
        
        # Check column
        if num in self.board[:, col]:
            return False
        
        # Check 3x3 box
        box_row, box_col = row // 3, col // 3
        if num in self.board[box_row*3:box_row*3+3, box_col*3:box_col*3+3]:
            return False
        
        return True
    
    def place_number(self, row: int, col: int, num: int) -> bool:
        """Place a number on the board if valid"""
        if 1 <= num <= 9 and self.is_valid_move(row, col, num):
            self.board[row, col] = num
            return True
        return False
    
    def clear_cell(self, row: int, col: int):
        """Clear a cell if it's not part of the original puzzle"""
        if not self.original[row, col]:
            self.board[row, col] = 0
    
    def is_complete(self) -> bool:
        """Check if the board is completely filled correctly"""
        return np.array_equal(self.board, self.solution)
    
    def get_hint(self) -> Optional[Tuple[int, int, int]]:
        """Get a hint (returns row, col, num)"""
        empty_cells = np.argwhere(self.board == 0)
        if len(empty_cells) > 0:
            row, col = empty_cells[0]
            return row, col, self.solution[row, col]
        return None
