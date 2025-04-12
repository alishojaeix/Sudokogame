import pygame
import sys
import numpy as np
from typing import Optional, Tuple

# Constants
WINDOW_SIZE = 600
GRID_SIZE = 540
CELL_SIZE = GRID_SIZE // 9
MARGIN = (WINDOW_SIZE - GRID_SIZE) // 2
BG_COLOR = (251, 247, 245)
GRID_COLOR = (0, 0, 0)
TEXT_COLOR = (0, 0, 0)
FIXED_TEXT_COLOR = (50, 50, 50)
HIGHLIGHT_COLOR = (173, 216, 230)
ERROR_COLOR = (255, 200, 200)

class SudokuGUI:
    def __init__(self, difficulty: str = 'medium'):
        pygame.init()
        pygame.display.set_caption("Sudoku")
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        self.font = pygame.font.SysFont('Arial', 40)
        self.small_font = pygame.font.SysFont('Arial', 24)
        self.game = None
        self.selected: Optional[Tuple[int, int]] = None
        self.difficulty = difficulty
        self.new_game()
    
    def new_game(self):
        """Start a new game with the current difficulty"""
        from .game import SudokuGame
        self.game = SudokuGame(self.difficulty)
        self.selected = None
    
    def draw(self):
        """Draw the game interface"""
        self.screen.fill(BG_COLOR)
        self.draw_grid()
        self.draw_numbers()
        self.draw_buttons()
        pygame.display.flip()
    
    def draw_grid(self):
        """Draw the Sudoku grid"""
        # Draw the selected cell highlight
        if self.selected:
            row, col = self.selected
            pygame.draw.rect(
                self.screen, 
                HIGHLIGHT_COLOR,
                (MARGIN + col * CELL_SIZE, 
                 MARGIN + row * CELL_SIZE, 
                 CELL_SIZE, CELL_SIZE)
            )
        
        # Draw the grid lines
        for i in range(10):
            # Thicker lines for 3x3 boxes
            line_width = 2 if i % 3 != 0 else 4
            
            # Horizontal lines
            pygame.draw.line(
                self.screen, GRID_COLOR,
                (MARGIN, MARGIN + i * CELL_SIZE),
                (MARGIN + GRID_SIZE, MARGIN + i * CELL_SIZE),
                line_width
            )
            
            # Vertical lines
            pygame.draw.line(
                self.screen, GRID_COLOR,
                (MARGIN + i * CELL_SIZE, MARGIN),
                (MARGIN + i * CELL_SIZE, MARGIN + GRID_SIZE),
                line_width
            )
    
    def draw_numbers(self):
        """Draw the numbers on the board"""
        for row in range(9):
            for col in range(9):
                num = self.game.board[row, col]
                if num != 0:
                    # Determine text color
                    if self.game.original[row, col]:
                        color = FIXED_TEXT_COLOR
                    else:
                        color = TEXT_COLOR
                    
                    # Check if the number is correct
                    if not self.game.original[row, col] and num != self.game.solution[row, col]:
                        pygame.draw.rect(
                            self.screen, ERROR_COLOR,
                            (MARGIN + col * CELL_SIZE, 
                             MARGIN + row * CELL_SIZE, 
                             CELL_SIZE, CELL_SIZE)
                        )
                    
                    text = self.font.render(str(num), True, color)
                    text_rect = text.get_rect(
                        center=(MARGIN + col * CELL_SIZE + CELL_SIZE // 2,
                                MARGIN + row * CELL_SIZE + CELL_SIZE // 2)
                    )
                    self.screen.blit(text, text_rect)
    
    def draw_buttons(self):
        """Draw the control buttons"""
        # New Game button
        new_game_text = self.small_font.render("New Game", True, (0, 0, 0))
        pygame.draw.rect(
            self.screen, (200, 200, 200),
            (20, WINDOW_SIZE - 50, 120, 30)
        )
        self.screen.blit(new_game_text, (30, WINDOW_SIZE - 45))
        
        # Difficulty selector
        diff_text = self.small_font.render(f"Difficulty: {self.difficulty}", True, (0, 0, 0))
        self.screen.blit(diff_text, (160, WINDOW_SIZE - 45))
        
        # Hint button
        hint_text = self.small_font.render("Hint", True, (0, 0, 0))
        pygame.draw.rect(
            self.screen, (200, 200, 200),
            (WINDOW_SIZE - 120, WINDOW_SIZE - 50, 80, 30)
        )
        self.screen.blit(hint_text, (WINDOW_SIZE - 110, WINDOW_SIZE - 45))
        
        # Game over message
        if self.game.is_complete():
            msg = self.font.render("Puzzle Complete!", True, (0, 128, 0))
            msg_rect = msg.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
            pygame.draw.rect(self.screen, (255, 255, 255), msg_rect.inflate(20, 20))
            self.screen.blit(msg, msg_rect)
    
    def handle_click(self, pos: Tuple[int, int]):
        """Handle mouse click events"""
        x, y = pos
        
        # Check if New Game button was clicked
        if 20 <= x <= 140 and WINDOW_SIZE - 50 <= y <= WINDOW_SIZE - 20:
            self.new_game()
            return
        
        # Check if Hint button was clicked
        if WINDOW_SIZE - 120 <= x <= WINDOW_SIZE - 40 and WINDOW_SIZE - 50 <= y <= WINDOW_SIZE - 20:
            hint = self.game.get_hint()
            if hint:
                row, col, num = hint
                self.game.place_number(row, col, num)
                self.selected = (row, col)
            return
        
        # Check if difficulty text was clicked
        if 160 <= x <= 300 and WINDOW_SIZE - 50 <= y <= WINDOW_SIZE - 20:
            difficulties = ['easy', 'medium', 'hard']
            current = difficulties.index(self.difficulty)
            self.difficulty = difficulties[(current + 1) % len(difficulties)]
            return
        
        # Check if a cell was clicked
        if (MARGIN <= x <= MARGIN + GRID_SIZE and 
            MARGIN <= y <= MARGIN + GRID_SIZE):
            col = (x - MARGIN) // CELL_SIZE
            row = (y - MARGIN) // CELL_SIZE
            if not self.game.original[row, col]:
                self.selected = (row, col)
    
    def handle_key(self, key: int):
        """Handle keyboard input"""
        if not self.selected:
            return
        
        row, col = self.selected
        
        if key == pygame.K_BACKSPACE or key == pygame.K_DELETE:
            self.game.clear_cell(row, col)
        elif pygame.K_1 <= key <= pygame.K_9:
            num = key - pygame.K_0
            self.game.place_number(row, col, num)
        elif pygame.K_LEFT <= key <= pygame.K_DOWN:
            # Move selection with arrow keys
            if key == pygame.K_LEFT and col > 0:
                col -= 1
            elif key == pygame.K_RIGHT and col < 8:
                col += 1
            elif key == pygame.K_UP and row > 0:
                row -= 1
            elif key == pygame.K_DOWN and row < 8:
                row += 1
            
            # Skip fixed cells when moving
            while self.game.original[row, col]:
                if key == pygame.K_LEFT and col > 0:
                    col -= 1
                elif key == pygame.K_RIGHT and col < 8:
                    col += 1
                elif key == pygame.K_UP and row > 0:
                    row -= 1
                elif key == pygame.K_DOWN and row < 8:
                    row += 1
                else:
                    break
            
            self.selected = (row, col)
    
    def run(self):
        """Main game loop"""
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    self.handle_key(event.key)
            
            self.draw()
            clock.tick(30)
