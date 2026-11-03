# 🎮 TicTacToe++ | Intelligent Tic-Tac-Toe Game (Python)

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![GUI](https://img.shields.io/badge/GUI-Tkinter-orange)
![AI](https://img.shields.io/badge/AI-Minimax%20Algorithm-purple)
![Algorithm](https://img.shields.io/badge/Algorithm-Alpha--Beta%20Pruning-red)
![Difficulty](https://img.shields.io/badge/Difficulty-Easy%20%7C%20Medium%20%7C%20Hard-green)
![Game](https://img.shields.io/badge/Game-Two%20Player%20%7C%20AI-informational)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)

**TicTacToe++** is an interactive, feature-rich Tic-Tac-Toe game developed using Python and Tkinter. It combines the simplicity of the classic Tic-Tac-Toe game with intelligent computer opponents, multiple difficulty levels, custom graphical interfaces, and real-time game statistics.

The project implements fundamental **Data Structures and Algorithms (DSA)** concepts, including game-state management, move generation, recursion, the Minimax algorithm, and Alpha-Beta Pruning to create an intelligent computer opponent.

Whether you want to challenge a friend or test your strategic thinking against an AI, TicTacToe++ provides an engaging gaming experience.

> 🎯 Think Ahead. Play Smart.

---

## 📌 Table of Contents

* 🚀 Features
* 🎮 Game Modes
* 🧠 AI Intelligence & Difficulty Levels
* ⚡ Algorithms & Game Logic
* 🗺️ Game Flow
* 🎨 User Interface & Design
* 🔊 Sound Effects
* ⌨️ Keyboard Shortcuts
* 📊 Score Tracking
* 🛠️ Tech Stack
* 📂 Project Structure
* ▶️ Installation & Setup
* 🎯 How to Play
* 📸 Gameplay Preview
* 🧪 Technical Implementation
* 📚 Learning Outcomes
* 🔮 Future Improvements
* 🤝 Contributing
* 📜 License
* 👨‍💻 Author
* ⭐ Support

---

# 🚀 Features

TicTacToe++ combines classic gameplay with intelligent decision-making and a modern desktop interface.

| Feature                  | Description                                                             |
| ------------------------ | ----------------------------------------------------------------------- |
| 🎮 Two Game Modes        | Play against another person or challenge the computer.                  |
| 🤖 Intelligent AI        | Computer opponent with three difficulty levels.                         |
| 🟢 Easy Mode             | Computer selects moves randomly.                                        |
| 🟡 Medium Mode           | Computer uses winning and blocking strategies.                          |
| 🔴 Hard Mode             | Uses Minimax with Alpha-Beta Pruning for optimal decision-making.       |
| 🎨 Custom GUI            | Modern dark-themed graphical interface built with Tkinter.              |
| 📊 Scoreboard            | Tracks Player X wins, Player O wins, and draws.                         |
| ↩️ Undo System           | Undo previous moves and reconsider your strategy.                       |
| 🔄 Restart Game          | Restart the current match without returning to the main menu.           |
| 🔊 Sound Effects         | Audio feedback for moves, wins, losses, draws, and button interactions. |
| 📜 Move History          | Displays the sequence of moves played during a match.                   |
| 🏆 Winning Animation     | Highlights the winning combination on the game board.                   |
| ⌨️ Keyboard Controls     | Perform important game actions using keyboard shortcuts.                |
| ⚡ Responsive Interaction | Smooth mouse-based gameplay with visual hover feedback.                 |

---

# 🎮 Game Modes

The game provides two different ways to play.

## 1️⃣ Two Player Mode

Challenge your friends in a local two-player match.

* Player X makes the first move.
* Player O plays the next move.
* Players take turns selecting empty cells.
* The first player to complete three consecutive symbols wins.
* If all nine cells are occupied without a winner, the match ends in a draw.

**Winning combinations include:**

* Three horizontal combinations.
* Three vertical combinations.
* Two diagonal combinations.

## 2️⃣ Player vs Computer Mode

Play against an intelligent computer opponent.

* You play as X.
* The computer plays as O.
* Select your preferred difficulty before starting.
* The computer automatically calculates and executes its moves.
* Hard Mode uses an optimal decision-making algorithm.

The computer opponent provides three different difficulty levels.

---

# 🧠 AI Intelligence & Difficulty Levels

One of the main highlights of TicTacToe++ is its AI implementation.

Instead of using the same strategy for every difficulty, the computer follows different decision-making approaches.

| Difficulty | AI Technique                 | Behaviour                                                     |
| ---------- | ---------------------------- | ------------------------------------------------------------- |
| 🟢 Easy    | Random Selection             | Selects any available cell randomly.                          |
| 🟡 Medium  | Heuristic-Based Strategy     | Prioritizes winning, blocking, the center, and corners.       |
| 🔴 Hard    | Minimax + Alpha-Beta Pruning | Evaluates possible game outcomes and selects an optimal move. |

### 🟢 Easy Mode — Random AI

Easy Mode is designed for beginners.

The computer:

* Identifies all available positions.
* Randomly selects one available position.
* Places its symbol on the selected cell.

This mode does not evaluate the strategic consequences of a move.

### 🟡 Medium Mode — Strategic AI

Medium Mode introduces basic strategic decision-making.

The computer follows this priority:

1. **Win:** Check whether it can complete a winning combination.
2. **Block:** Check whether the opponent can win on their next move.
3. **Center:** Prioritize the center position if available.
4. **Corners:** Select an available corner.
5. **Fallback:** Randomly select another available position.

This makes the computer more challenging than Easy Mode.

### 🔴 Hard Mode — Intelligent AI

Hard Mode uses the **Minimax Algorithm with Alpha-Beta Pruning**.

Instead of randomly selecting a position, the computer evaluates possible future game states and chooses the move with the best outcome.

The algorithm considers:

* Possible winning combinations.
* Potential opponent moves.
* Future game states.
* Winning and losing outcomes.
* The number of moves required to reach a result.

The computer aims to maximize its chances of winning while minimizing the opponent's chances.

**Result:** Hard Mode plays optimally in standard Tic-Tac-Toe and cannot be beaten by a correctly implemented opponent strategy.

A match can still end in a draw.

---

# ⚡ Algorithms & Game Logic

This project incorporates several important programming and DSA concepts.

## 1. Minimax Algorithm

Minimax is a recursive decision-making algorithm commonly used in two-player, turn-based games.

It assumes that both players make optimal decisions.

In TicTacToe++:

* The computer (O) acts as the maximizing player.
* The human player (X) acts as the minimizing player.

The algorithm evaluates possible game outcomes using the following scoring system:

| Game Outcome      | Score |
| ----------------- | ----: |
| Computer Wins (O) |   +10 |
| Human Wins (X)    |   -10 |
| Draw              |     0 |

The score is adjusted according to the search depth.

This encourages the computer to:

* Win as quickly as possible.
* Delay an unavoidable loss.
* Avoid moves that lead to losing positions.

### Simplified Minimax Logic

```python
def minimax(board, maximizing):

    winner, _ = Game.get_result(board)

    if winner == "O":
        return 10

    if winner == "X":
        return -10

    if "" not in board:
        return 0

    if maximizing:
        best = float("-inf")

        # Evaluate possible computer moves

    else:
        best = float("inf")

        # Evaluate possible human moves

    return best
```

*The above is a simplified illustration of the algorithm. The actual implementation also considers search depth and Alpha-Beta Pruning.*

## 2. Alpha-Beta Pruning

Alpha-Beta Pruning is an optimization technique used with Minimax.

It reduces the number of unnecessary game states that need to be evaluated.

It maintains two values:

| Parameter | Description                                               |
| --------- | --------------------------------------------------------- |
| Alpha (α) | Best value currently guaranteed to the maximizing player. |
| Beta (β)  | Best value currently guaranteed to the minimizing player. |

When the algorithm determines that exploring a particular branch cannot improve the final decision, it stops evaluating that branch.

This process is called **pruning**.

The implementation uses the condition:

```python
if beta <= alpha:
    break
```

### Why Alpha-Beta Pruning?

* Reduces unnecessary recursive calculations.
* Improves search efficiency.
* Allows deeper game-tree exploration.
* Produces the same optimal decision as Minimax when implemented correctly.

## 3. Game State Management

The game uses a list containing nine positions to represent the board.

```python
board = [""] * 9
```

Each position represents one cell.

Example:

```text
 X | O | X
-----------
 O | X | O
-----------
 X |   |
```

The board is represented internally as:

```python
[
    "X", "O", "X",
    "O", "X", "O",
    "X", "", ""
]
```

The game checks all eight possible winning combinations to determine whether a player has won.

---


---

# 🎨 User Interface & Design

TicTacToe++ uses Python's Tkinter library to provide a graphical gaming experience.

Instead of relying on a traditional command-line interface, the application provides a custom-designed desktop interface.

### Design Highlights

| UI Component         | Description                                                  |
| -------------------- | ------------------------------------------------------------ |
| 🌑 Dark Theme        | Dark background with carefully selected contrasting colors.  |
| 💠 Cyan Accents      | Used for Player X and important interface elements.          |
| 🟣 Violet Accents    | Used for Player O and AI-related elements.                   |
| 🟢 Green Highlights  | Used to indicate winning combinations.                       |
| 🎯 Interactive Board | Clickable 3×3 game board.                                    |
| ✨ Hover Effects      | Empty cells visually respond when the mouse moves over them. |
| 📊 Score Cards       | Display match statistics in a structured layout.             |
| 📜 Move History      | Shows previous moves and their positions.                    |

### Color Palette

| Color           | Hex Code  | Purpose                     |
| --------------- | --------- | --------------------------- |
| Dark Background | `#0B1020` | Main application background |
| Surface         | `#121A2B` | Cards and panels            |
| Cyan            | `#4DE1F0` | Player X                    |
| Violet          | `#A78BFA` | Player O                    |
| Green           | `#48D6A0` | Winning indicators          |
| Red             | `#FF7185` | Error and alert accents     |

---

# 🔊 Sound Effects

The game includes built-in sound effects to improve the overall gaming experience.

Sound effects are generated programmatically rather than using external audio files.

| Event              | Sound                    |
| ------------------ | ------------------------ |
| Player Move        | Short beep               |
| Undo Move          | Low-frequency beep       |
| Winning            | Multiple ascending tones |
| Losing             | Descending tones         |
| Draw               | Repeated tones           |
| Button Interaction | Short click sound        |

### Cross-Platform Handling

The application uses Python's `winsound` module when available.

On systems where `winsound` is unavailable, it falls back to Tkinter's built-in bell functionality.

Sound effects can also be enabled or disabled directly from the game interface.

---

# ⌨️ Keyboard Shortcuts

TicTacToe++ supports keyboard shortcuts for frequently used actions.

| Shortcut | Action                              |
| -------- | ----------------------------------- |
| `1 – 9`  | Select corresponding board position |
| `U`      | Undo previous move(s)               |
| `R`      | Restart current match               |

### Board Position Mapping

```text
  1 | 2 | 3
-------------
  4 | 5 | 6
-------------
  7 | 8 | 9
```

You can use either the mouse or keyboard to play.

---

# 📊 Score Tracking

The application maintains a scoreboard throughout the current session.

Three statistics are tracked:

| Statistic | Description                    |
| --------- | ------------------------------ |
| Player X  | Total matches won by Player X  |
| Draws     | Total matches ending in a draw |
| Player O  | Total matches won by Player O  |

The scoreboard automatically updates when a match finishes.

Additional controls include:

* Restart the current match.
* Undo previous moves.
* Reset all match scores.
* Return to the main menu.

**Note:** Scores are maintained during the running application session and are not permanently stored after closing the game.

---

# 🛠️ Tech Stack

The project uses Python and its built-in libraries to implement the game logic, AI, and graphical interface.

| Technology           | Purpose                                             |
| -------------------- | --------------------------------------------------- |
| 🐍 Python 3          | Primary programming language                        |
| 🎨 Tkinter           | Graphical User Interface                            |
| 🧠 Minimax           | AI decision-making algorithm                        |
| ⚡ Alpha-Beta Pruning | Optimization of Minimax search                      |
| 🎲 Random Module     | Random move selection in Easy Mode                  |
| 🔊 Winsound          | Programmatically generated sound effects on Windows |
| 📦 Typing            | Type annotations and optional type handling         |

### External Dependencies

No third-party Python packages are required.

The application primarily relies on Python's standard library.

---

# 📂 Project Structure

The project follows a simple and organized structure.

```text
TicTacToe-Plus-Plus/
│
├── main.py
│
├── README.md
│
├── LICENSE
│
└── screenshots/
    └── gameplay.png
```

| File / Directory | Description                                |
| ---------------- | ------------------------------------------ |
| `main.py`        | Contains the complete game implementation. |
| `README.md`      | Project documentation.                     |
| `LICENSE`        | Project license, if included.              |
| `screenshots/`   | Stores screenshots of the application.     |

*The structure above is a suggested repository organization.*

---


# 🎯 How to Play

Getting started is simple.

### Step 1: Launch the Application

Run the Python file to open the main menu.

### Step 2: Select Your Game Mode

Choose between:

* Two Players — Play against a friend.
* Vs Computer — Challenge the AI.

### Step 3: Select Difficulty

If you choose Computer Mode, select:

* Easy
* Medium
* Hard

### Step 4: Start Playing

Select any empty cell on the 3×3 board.

Player X always makes the first move.

### Step 5: Win the Match

Complete three consecutive symbols horizontally, vertically, or diagonally.

### Step 6: Manage Your Game

Use the available controls to:

* Undo moves.
* Restart the match.
* Reset scores.
* Toggle sound effects.
* Return to the main menu.

---

# 📸 Gameplay Preview

A visual preview of the TicTacToe++ desktop application.

### Main Menu

<!-- Add your main menu screenshot here -->

![TicTacToe++ Main Menu](screenshots/main-menu.png)

### Game Interface

<!-- Add your gameplay screenshot here -->

![TicTacToe++ Gameplay](screenshots/gameplay.png)

### Computer AI — Hard Mode

<!-- Add your Hard Mode screenshot here -->

![TicTacToe++ AI Mode](screenshots/hard-mode.png)

*Replace the screenshot paths with your actual image files.*

---

# 🧪 Technical Implementation

The project separates important responsibilities into different Python classes.

| Class            | Responsibility                                                                      |
| ---------------- | ----------------------------------------------------------------------------------- |
| `SoundFX`        | Handles sound generation and sound settings.                                        |
| `Game`           | Manages the board, turns, moves, winning conditions, and game state.                |
| `ComputerPlayer` | Implements AI decision-making for all three difficulty levels.                      |
| `TicTacToeApp`   | Manages the graphical interface, user interactions, controls, and application flow. |

### Important Methods

| Method              | Purpose                                                                |
| ------------------- | ---------------------------------------------------------------------- |
| `reset()`           | Initializes a new game state.                                          |
| `get_result()`      | Checks whether a player has won.                                       |
| `available_moves()` | Returns all available board positions.                                 |
| `play()`            | Executes a valid move.                                                 |
| `undo()`            | Removes previous moves from the game history.                          |
| `choose_move()`     | Determines the computer's next move.                                   |
| `_minimax()`        | Evaluates possible game outcomes recursively using Alpha-Beta Pruning. |
| `finish_round()`    | Handles match completion and score updates.                            |
| `draw_board()`      | Renders the game board and symbols.                                    |
| `restart()`         | Restarts the current match.                                            |

---

# 🎯 Learning Outcomes

Developing TicTacToe++ provides practical experience with several fundamental and intermediate programming concepts.

| Concept                        | What You Learn                                                          |
| ------------------------------ | ----------------------------------------------------------------------- |
| 🔀 Conditional Statements      | Implement game rules and decision-making logic.                         |
| 🔁 Loops                       | Process available moves and game conditions.                            |
| 🧩 Object-Oriented Programming | Organize application functionality using classes and methods.           |
| 📦 Lists & Data Structures     | Represent and manage the Tic-Tac-Toe board.                             |
| 🔄 Recursion                   | Explore future game states using recursive function calls.              |
| 🧠 Minimax Algorithm           | Implement intelligent decision-making for competitive games.            |
| ⚡ Alpha-Beta Pruning           | Optimize recursive search by eliminating unnecessary branches.          |
| 🎲 Randomization               | Generate unpredictable computer moves.                                  |
| 🖥️ GUI Development            | Build interactive desktop applications using Tkinter.                   |
| 🎧 Event Handling              | Handle mouse clicks, keyboard inputs, and interface events.             |
| 📚 Game State Management       | Maintain turns, move history, scores, and winning conditions.           |
| 🏗️ Code Architecture          | Separate game logic, AI functionality, sound, and GUI responsibilities. |

**Overall, this project demonstrates how fundamental programming concepts and algorithms can be combined to build an interactive application with intelligent decision-making.**

---

# 🔮 Future Improvements

Although the current version includes the core gameplay and AI functionality, there are several opportunities to expand the project.

Potential improvements include:

* 🌐 Online Multiplayer — Allow players to compete over the internet.
* 🏆 Persistent Leaderboard — Save player statistics between sessions.
* 🎨 Theme Customization — Introduce additional interface themes.
* 🤖 Advanced AI — Experiment with additional game-search strategies.
* ⏱️ Timed Challenges — Introduce time-based gameplay.
* 👤 Player Profiles — Maintain individual player statistics.
* 🎵 Custom Audio — Add background music and additional sound effects.
* 📱 Mobile Version — Explore adapting the game for mobile platforms.

These improvements can help transform the current desktop application into a more comprehensive gaming platform.

---

# 🤝 Contributing

Contributions are always welcome!

I'm genuinely open to collaborating with anyone interested in improving this project.

Whether you're a beginner exploring Python or an experienced developer interested in algorithms, GUI development, or AI, you're welcome to contribute.

You can contribute by:

* Improving the AI decision-making system.
* Optimizing existing algorithms.
* Enhancing the graphical interface.
* Adding new gameplay features.
* Fixing bugs.
* Improving code readability.
* Suggesting new ideas.

### Steps to Contribute

**1. Fork the repository**

**2. Clone your fork**

```bash
git clone https://github.com/your-username/TicTacToe-Plus-Plus.git
```

**3. Create a new branch**

```bash
git checkout -b feature-name
```

**4. Make your changes**

**5. Commit your changes**

```bash
git add .
git commit -m "Add new feature"
```

**6. Push your branch**

```bash
git push origin feature-name
```

**7. Open a Pull Request**

Your contributions and suggestions are appreciated!

Let's build, learn, and improve together. 🚀

---

# 📜 License

This project can be distributed under the **MIT License** if the repository includes an MIT `LICENSE` file.

The MIT License allows users to:

* Use the software.
* Modify the source code.
* Distribute copies.
* Use the software for personal or commercial purposes.

Please refer to the repository's `LICENSE` file for the applicable terms.

---

# 👨‍💻 Author

<div align="center">

## Prem Kumar

🎓 B.Tech Computer Science & Engineering Student

💻 Interested in Software Development, Algorithms, and Technology.

🚀 Building projects to learn, experiment, and solve real-world problems.

</div>

### 🤝 Let's Connect

I'm always interested in connecting with developers, exchanging ideas, exploring technologies, and collaborating on interesting projects.

**Keep Building. Keep Learning. Keep Improving.**

---

# ⭐ Support

<div align="center">

## 💙 Show Your Support

If you enjoyed playing TicTacToe++ or found the project interesting, consider supporting it!

</div>

### 🚀 Ways to Support

* ⭐ Star this repository.
* 🍴 Fork the project and experiment with your own ideas.
* 🛠️ Contribute new features and improvements.
* 📢 Share the project with other developers.
* 💬 Suggest improvements and report bugs.

> Every star, suggestion, and contribution motivates me to keep building and sharing more projects with the developer community.

---

<div align="center">

### 🎮 TICTACTOE++

**THINK AHEAD. PLAY SMART.**

*Built with Python, Algorithms, and a little intelligence.*

</div>
