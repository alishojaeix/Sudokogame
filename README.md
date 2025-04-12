# 🧩 Python Sudoku Game

![Game Screenshot](assets/screenshot.png) *(add screenshot later)*

A complete Sudoku game with puzzle generation, solving, and a graphical interface built with Python and Pygame.

## 🎯 Features

- 🧩 Random puzzle generation with three difficulty levels
- ✅ Automatic solving and validation
- 💡 Hint system
- 🖱️ Intuitive graphical interface
- 🎨 Clean, responsive design
- 🔄 Multiple game support

## 📋 Table of Contents
- [Game Rules](#-game-rules)
- [Installation](#-installation)
- [How to Play](#-how-to-play)
- [Controls](#-controls)
- [Customization](#-customization)
- [Roadmap](#-roadmap)
- [License](#-license)

## 🧠 Game Rules

1. Fill the 9×9 grid with digits from 1 to 9
2. Each row must contain all digits from 1 to 9 without repetition
3. Each column must contain all digits from 1 to 9 without repetition
4. Each 3×3 box must contain all digits from 1 to 9 without repetition

## 💻 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/alishojaeix/sudoku-game.git
   cd sudoku-game

   2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the game:
   ```bash
   python main.py
   ```

## 🎮 How to Play

1. Click on an empty cell to select it
2. Press a number key (1-9) to fill the cell
3. Use backspace/delete to clear a cell
4. Click "Hint" to get help with the next move
5. Click "New Game" to start a new puzzle

## 🕹️ Controls

| Control | Action |
|---------|--------|
| Mouse Click | Select cell |
| 1-9 Keys | Enter number |
| Delete/Backspace | Clear cell |
| Arrow Keys | Move selection |
| Hint Button | Get a hint |
| New Game Button | Start new game |

## 🛠️ Customization

Modify `main.py` to change default settings:
```python
# Change difficulty: 'easy', 'medium', or 'hard'
game = SudokuGUI(difficulty='medium')
```

Modify `gui.py` to change appearance:
```python
# Change colors, sizes, etc.
WINDOW_SIZE = 600  # Window width/height
BG_COLOR = (251, 247, 245)  # Background color
```

## 🚀 Roadmap

- [ ] Add puzzle timer
- [ ] Implement puzzle difficulty scoring
- [ ] Add save/load functionality
- [ ] Create an AI solver visualization
- [ ] Add sound effects
