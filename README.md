# 🎲 Ludo Game

**Ludo Game** is a Python implementation of the classic Ludo board game using Pygame. It features player management, database integration for tracking scores, and a graphical interface with smooth gameplay mechanics.

---

## ✨ Features

- Classic Ludo gameplay for 2-4 players
- Player management system with win/loss tracking
- SQLite database integration for persistent score storage
- Interactive player selection screen
- Colored dice matching player colors
- Token movement with special rules (jumps, safe zones, home paths)
- Winner detection and ranking system
- Player statistics tracking

---

## 🛠️ Requirements

- **Python 3.7+**
- **Pygame** library
- **SQLite3** (included with Python)

---

## 🚀 Installation & Setup

### 1. Clone or Download the Repository

### 2. Install Dependencies

```bash
pip install pygame
```

### 3. Run the Game

```bash
python ludo.py
```

---

## 🎮 How to Play

1. **Select Players**: Choose 2-4 players at the start of the game
2. **Roll Dice**: Click on the dice to roll (must roll a 6 to move tokens out of home)
3. **Move Tokens**: Click on your token after rolling to move it
4. **Special Moves**:
   - Jump to other paths when landing on special squares
   - Send opponents back to home by landing on their tokens
   - Safe zones (star squares) protect from being sent home
5. **Win the Game**: Be the first to get all four tokens to the center winner area

---

## 🗄️ Database Features

The game includes a SQLite database (`ludo.db`) that:
- Stores player names and statistics
- Tracks wins and losses
- Allows player management through the in-game interface

### Player Management

Click the "Manage Players" button to:
- View all players and their statistics
- Add new players
- Edit existing player names and stats
- Delete players

---

## 🎨 Game Elements

- **Colored Tokens**: Red, Green, Yellow, Blue
- **Special Squares**: Star icons indicate safe zones
- **Colored Dice**: Matches current player's color
- **Player Panel**: Shows current player and winner rankings

---

## 📁 Project Structure

```
ludo.py  # Main game file
db.py         # Database handling module
asset/        # Game assets directory
  Board.jpg   # Game board
  star.png    # Safe zone marker
  1.png-6.png # Dice faces
  red.png     # Red token
  green.png   # Green token
  yellow.png  # Yellow token
  blue.png    # Blue token
```

---

## 👨‍💻 Author

Hafifa Hussein

---

## 📄 License

MIT License