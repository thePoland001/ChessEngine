# ♔ Chess Engine
A Python-based chess engine that uses the Minimax algorithm with Alpha-Beta pruning to calculate the best moves. The engine evaluates board positions based on piece values, positional advantages, and checkmate scenarios. This project includes move generation, check/checkmate detection, and an evaluation function.

# 🚀 Features 
- ✅ Minimax algorithm with Alpha-Beta pruning for efficient search. 
- ✅ Move generation for all piece types.
- ✅ Check and checkmate detection.
- ✅ Positional evaluation considering material and control of center squares.
- ✅ Pathfinding to ensure legal moves.
- ✅ Basic AI that can play as White or Black.

# 🧠 How It Works
- Position Class
Manages the current state of the board.
Tracks pieces and their locations.
Provides helper functions to retrieve piece positions and check for occupied squares.
- Move Class
Represents a move from one square to another.
Stores the piece involved and the start/end locations.
  - ChessAI Class
Uses the Minimax algorithm with Alpha-Beta pruning.
Evaluates the board based on:
Material value of pieces.
Positioning advantage (central squares).
Check and checkmate scenarios.
Generates legal moves for all piece types.
Ensures the king is not left in check after a move.
