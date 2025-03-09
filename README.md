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
1. Position Class
- Manages the current state of the board.
- Tracks pieces and their locations.
- Provides helper functions to retrieve piece positions and check for occupied squares.
2. Move Class
- Represents a move from one square to another.
- Stores the piece involved and the start/end locations.
3. ChessAI Class
- Uses the Minimax algorithm with Alpha-Beta pruning.
- Evaluates the board based on:
- Material value of pieces.
- Positioning advantage (central squares).
- Check and checkmate scenarios.
- Generates legal moves for all piece types.
- Ensures the king is not left in check after a move.

# How to Use 
```bash
git clone https://github.com/your-username/ChessEngine.git
cd chess_engine

python chess_engine.py
```

# Example Usage

```python
pos = Position()

# White pieces
pos.add_piece(1, 'K', 'white', 'e1')
pos.add_piece(2, 'Q', 'white', 'f6')

# Black pieces
pos.add_piece(3, 'K', 'black', 'h8')
pos.add_piece(4, 'p', 'black', 'g7')
pos.add_piece(5, 'p', 'black', 'h7')

ai = ChessAI()

# Find the best move for White
best_move = ai.find_best_move(pos, 'white')
if best_move:
    piece_type = pos.pieces[best_move.piece_id][0]
    print(f"Best move: {piece_type} {best_move.from_square} to {best_move.to_square}")
```

Output: 
```python
Best move: Q f6 to h6
```
