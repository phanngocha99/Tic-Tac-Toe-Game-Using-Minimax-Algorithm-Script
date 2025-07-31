# Tic-Tac-Toe AI using Minimax Algorithm
This project implements an AI for the classic Tic-Tac-Toe (caro) game using the Minimax algorithm. 
The AI plays optimally against a human player on a 3x3 board, with optional support for larger boards (e.g. 10x10, 20x20) and customizable win conditions.

🚀 Features
- 3x3 classic Tic-Tac-Toe board
- Human vs Computer gameplay
- Minimax algorithm with recursion and depth handling
- Input validation and game-over detection
- Support for custom initial states
- Option to scale to larger boards (10x10, 20x20)
- Configurable win condition (e.g., 5 in a row)

🧠 Core AI Logic: 
- Minimax Algorithm: The AI uses the minimax strategy to evaluate all possible game states.

🚀 Terminal conditions:
- Win/loss detected via wins() function
- No more valid moves
- Reached maximum search depth
- Evaluation Function
+1 if computer wins
-1 if human wins
0 for draw or ongoing

🕹️ Game Functions
- wins(state, player): Check if player wins
- evaluate(state): Evaluate current board score
- game_over(state): Detect game end
- empty_cells(state): List of empty positions
- valid_move(x, y): Validate move
- set_move(x, y, player): Apply move
- minimax(state, depth, player): Run AI search

🕹️ How to Play
- Run the game script.
- Choose your symbol: X or O
- Choose who goes first.
- Make your move by entering board coordinates.
- Let the AI respond and continue

🧪 Run the Python script
- python tictactoe.py
- Ensure you have Python 3.x installed
