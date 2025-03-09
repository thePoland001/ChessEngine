import random

class Position:
    def __init__(self):
        self.pieces = {}

    def add_piece(self, piece_id, piece_type, color, square):
        self.pieces[piece_id] = (piece_type, color, square)

    def remove_piece(self, piece_id):
        if piece_id in self.pieces:
            del self.pieces[piece_id]

    def get_king_square(self, color):
        for _, (piece_type, piece_color, square) in self.pieces.items():
            if piece_type == 'K' and piece_color == color:
                return square
        return None

    def get_piece_at_square(self, square):
        for piece_id, (piece_type, color, piece_square) in self.pieces.items():
            if piece_square == square:
                return (piece_id, piece_type, color)
        return None

class Move:
    def __init__(self, piece_id, from_square, to_square):
        self.piece_id = piece_id
        self.from_square = from_square
        self.to_square = to_square

class ChessAI:
    def __init__(self):
        self.piece_values = {
            'K': 20000,
            'Q': 900,
            'R': 500,
            'B': 330,
            'N': 320,
            'p': 100
        }
        self.center_squares = ['e4', 'e5', 'd4', 'd5']
        self.CHECKMATE = 100000
        self.MAX_DEPTH = 3

    def square_to_coords(self, square):
        file, rank = square[0], int(square[1])
        file_idx = ord(file) - ord('a')
        rank_idx = rank - 1
        return rank_idx, file_idx

    def coords_to_square(self, coords):
        rank_idx, file_idx = coords
        if not (0 <= rank_idx < 8 and 0 <= file_idx < 8):
            return None
        file = chr(ord('a') + file_idx)
        rank = str(rank_idx + 1)
        return file + rank

    def is_square_attacked(self, position, target_square, attacking_color):
        target_coords = self.square_to_coords(target_square)

        for piece_id, (piece_type, color, square) in position.pieces.items():
            if color != attacking_color:
                continue

            attacker_coords = self.square_to_coords(square)

            if piece_type == 'p':  # Pawn attacks
                direction = 1 if color == 'white' else -1
                file_diff = abs(ord(target_square[0]) - ord(square[0]))
                rank_diff = int(target_square[1]) - int(square[1])
                if file_diff == 1 and rank_diff == direction:
                    return True

            elif piece_type == 'N':  # Knight attacks
                file_diff = abs(ord(target_square[0]) - ord(square[0]))
                rank_diff = abs(int(target_square[1]) - int(square[1]))
                if (file_diff == 2 and rank_diff == 1) or (file_diff == 1 and rank_diff == 2):
                    return True

            elif piece_type in ['Q', 'R', 'B']:
                # Check if move is valid for piece type
                file_diff = abs(ord(target_square[0]) - ord(square[0]))
                rank_diff = abs(int(target_square[1]) - int(square[1]))

                is_orthogonal = file_diff == 0 or rank_diff == 0
                is_diagonal = file_diff == rank_diff

                if piece_type == 'R' and not is_orthogonal:
                    continue
                if piece_type == 'B' and not is_diagonal:
                    continue
                if piece_type == 'Q' and not (is_orthogonal or is_diagonal):
                    continue

                # Check if path is clear
                if self.is_path_clear(position, square, target_square):
                    return True

            elif piece_type == 'K':  # King attacks
                file_diff = abs(ord(target_square[0]) - ord(square[0]))
                rank_diff = abs(int(target_square[1]) - int(square[1]))
                if file_diff <= 1 and rank_diff <= 1:
                    return True

        return False

    def is_path_clear(self, position, from_square, to_square):
        """Check if path between two squares is clear of pieces"""
        from_file, from_rank = ord(from_square[0]) - ord('a'), int(from_square[1])
        to_file, to_rank = ord(to_square[0]) - ord('a'), int(to_square[1])

        file_diff = to_file - from_file
        rank_diff = to_rank - from_rank

        # Determine direction of movement
        file_step = 0 if file_diff == 0 else file_diff // abs(file_diff)
        rank_step = 0 if rank_diff == 0 else rank_diff // abs(rank_diff)

        current_file = from_file + file_step
        current_rank = from_rank + rank_step

        while (chr(ord('a') + current_file) + str(current_rank)) != to_square:
            square = chr(ord('a') + current_file) + str(current_rank)
            if position.get_piece_at_square(square) is not None:
                return False
            current_file += file_step
            current_rank += rank_step

        return True

    def is_in_check(self, position, color):
        king_square = position.get_king_square(color)
        if not king_square:
            return False
        return self.is_square_attacked(position, king_square, 'black' if color == 'white' else 'white')

    def is_checkmate(self, position, color):
        # First check if king is in check
        if not self.is_in_check(position, color):
            return False

        # Try all possible moves to see if any get out of check
        moves = self.generate_legal_moves(position, color)
        return len(moves) == 0

    def generate_legal_moves(self, position, color):
        moves = []

        for piece_id, (piece_type, piece_color, square) in position.pieces.items():
            if piece_color != color:
                continue

            potential_moves = self.generate_piece_moves(position, piece_id)
            for move in potential_moves:
                # Test if move leaves king in check
                new_position = self.make_move(position, move)
                if not self.is_in_check(new_position, color):
                    moves.append(move)

        return moves

    def generate_piece_moves(self, position, piece_id):
        piece_type, color, square = position.pieces[piece_id]
        moves = []

        from_file = ord(square[0]) - ord('a')
        from_rank = int(square[1])

        if piece_type == 'p':
            direction = 1 if color == 'white' else -1
            new_rank = from_rank + direction
            if 1 <= new_rank <= 8:
                new_square = square[0] + str(new_rank)
                if not position.get_piece_at_square(new_square):
                    moves.append(Move(piece_id, square, new_square))

            # Pawn captures
            for file_offset in [-1, 1]:
                new_file = chr(ord(square[0]) + file_offset)
                if 'a' <= new_file <= 'h':
                    capture_square = new_file + str(new_rank)
                    piece_at_square = position.get_piece_at_square(capture_square)
                    if piece_at_square and piece_at_square[2] != color:
                        moves.append(Move(piece_id, square, capture_square))

        elif piece_type == 'N':  # Knight
            knight_moves = [
                (-2, -1), (-2, 1), (-1, -2), (-1, 2),
                (1, -2), (1, 2), (2, -1), (2, 1)
            ]
            for rank_offset, file_offset in knight_moves:
                new_rank = from_rank + rank_offset
                new_file = chr(ord(square[0]) + file_offset)
                if 1 <= new_rank <= 8 and 'a' <= new_file <= 'h':
                    new_square = new_file + str(new_rank)
                    piece_at_square = position.get_piece_at_square(new_square)
                    if not piece_at_square or piece_at_square[2] != color:
                        moves.append(Move(piece_id, square, new_square))

        elif piece_type in ['Q', 'R', 'B', 'K']:
            directions = []
            if piece_type in ['Q', 'R']:  # Orthogonal directions
                directions.extend([(0, 1), (0, -1), (1, 0), (-1, 0)])
            if piece_type in ['Q', 'B']:  # Diagonal directions
                directions.extend([(1, 1), (1, -1), (-1, 1), (-1, -1)])
            if piece_type == 'K':
                directions = [(dx, dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if dx != 0 or dy != 0]

            for rank_dir, file_dir in directions:
                for distance in range(1, 8 if piece_type != 'K' else 2):
                    new_rank = from_rank + rank_dir * distance
                    new_file = chr(ord(square[0]) + file_dir * distance)
                    if 1 <= new_rank <= 8 and 'a' <= new_file <= 'h':
                        new_square = new_file + str(new_rank)
                        piece_at_square = position.get_piece_at_square(new_square)
                        if not piece_at_square:
                            moves.append(Move(piece_id, square, new_square))
                            continue
                        if piece_at_square[2] != color:
                            moves.append(Move(piece_id, square, new_square))
                        break
                    break

        return moves

    def make_move(self, position, move):
        new_position = Position()
        # Copy all pieces except captured piece
        for piece_id, piece_data in position.pieces.items():
            if piece_data[2] != move.to_square:  # Don't copy captured piece
                new_position.pieces[piece_id] = piece_data

        # Move the piece
        piece_type, color, _ = position.pieces[move.piece_id]
        new_position.pieces[move.piece_id] = (piece_type, color, move.to_square)

        return new_position

    def evaluate_position(self, position):
        # Check for checkmate
        if self.is_checkmate(position, 'white'):
            return -self.CHECKMATE
        if self.is_checkmate(position, 'black'):
            return self.CHECKMATE

        score = 0
        for piece_id, (piece_type, color, square) in position.pieces.items():
            # Material value
            piece_value = self.piece_values[piece_type]
            if color == 'black':
                piece_value = -piece_value

            # Position value - bonus for controlling center
            if square in self.center_squares:
                if color == 'white':
                    piece_value += 50
                else:
                    piece_value -= 50

            score += piece_value

        return score

    def minimax(self, position, depth, alpha, beta, maximizing_player):
        if depth == 0:
            return self.evaluate_position(position)

        color = 'white' if maximizing_player else 'black'
        moves = self.generate_legal_moves(position, color)

        # If no legal moves and in check, it's checkmate
        if len(moves) == 0 and self.is_in_check(position, color):
            return -self.CHECKMATE if maximizing_player else self.CHECKMATE

        if maximizing_player:
            max_eval = float('-inf')
            for move in moves:
                new_position = self.make_move(position, move)
                eval = self.minimax(new_position, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in moves:
                new_position = self.make_move(position, move)
                eval = self.minimax(new_position, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def find_best_move(self, position, color):
        best_move = None
        best_value = float('-inf') if color == 'white' else float('inf')
        alpha = float('-inf')
        beta = float('inf')

        moves = self.generate_legal_moves(position, color)
        for move in moves:
            new_position = self.make_move(position, move)
            value = self.minimax(new_position, self.MAX_DEPTH - 1, alpha, beta, color != 'white')

            if color == 'white' and value > best_value:
                best_value = value
                best_move = move
            elif color == 'black' and value < best_value:
                best_value = value
                best_move = move

        return best_move

# Test positions
if __name__ == "__main__":
    # position where White can checkmate in one move
    # Black king on h8 with pawns on g7, h7
    # White queen on f6 can deliver checkmate by moving to h6
    pos = Position()

    # White pieces
    pos.add_piece(1, 'K', 'white', 'e1')
    pos.add_piece(2, 'Q', 'white', 'f6')

    # Black pieces
    pos.add_piece(3, 'K', 'black', 'h8')
    pos.add_piece(4, 'p', 'black', 'g7')
    pos.add_piece(5, 'p', 'black', 'h7')

    ai = ChessAI()

    # Find best move for White
    print("\nFinding best move for White:")
    best_move = ai.find_best_move(pos, 'white')
    if best_move:
        piece_type = pos.pieces[best_move.piece_id][0]
        print(f"Best move: {piece_type} {best_move.from_square} to {best_move.to_square}")
    # Find best move for Black
    print("\nFinding best move for Black:")
    best_move = ai.find_best_move(pos, 'black')
    if best_move:
        piece_type = pos.pieces[best_move.piece_id][0]
        print(f"Best move: {piece_type} {best_move.from_square} to {best_move.to_square}")

        new_pos = ai.make_move(pos, best_move)

