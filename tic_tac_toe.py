import math
import os

# Global board representation (1D list of 9 elements)
board = [' ' for _ in range(9)]

def print_board():
    """Prints the current state of the board in a user-friendly format."""
    print(f"\n {board[0]} | {board[1]} | {board[2]} ")
    print("---|---|---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---|---|---")
    print(f" {board[6]} | {board[7]} | {board[8]} \n")

def check_win(player):
    """Checks if the specified player has won the game."""
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8], # cols
        [0, 4, 8], [2, 4, 6]             # diagonals
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == player:
            return True
    return False

def check_draw():
    """Checks if the game is a draw (no empty spaces left)."""
    return ' ' not in board

def get_available_moves():
    """Returns a list of available indices on the board."""
    return [i for i, spot in enumerate(board) if spot == ' ']

def minimax(is_maximizing, depth):
    """
    Minimax algorithm to evaluate the best possible move.
    Returns a score indicating how good the current board state is.
    """
    # Base cases: Check if the game is over
    if check_win('O'): # AI wins
        return 10 - depth  # Subtract depth to prefer faster wins
    if check_win('X'): # Human wins
        return depth - 10  # Add depth to prolong the game if losing
    if check_draw():
        return 0

    if is_maximizing:
        best_score = -math.inf
        for move in get_available_moves():
            board[move] = 'O'
            score = minimax(False, depth + 1)
            board[move] = ' '
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for move in get_available_moves():
            board[move] = 'X'
            score = minimax(True, depth + 1)
            board[move] = ' '
            best_score = min(score, best_score)
        return best_score

def ai_move():
    """Determines and plays the best move for the AI using Minimax."""
    best_score = -math.inf
    best_move = None
    
    # Iterate through all possible moves and evaluate them using Minimax
    for move in get_available_moves():
        board[move] = 'O'
        score = minimax(False, 0)
        board[move] = ' '
        
        if score > best_score:
            best_score = score
            best_move = move
            
    if best_move is not None:
        board[best_move] = 'O'

def human_move():
    """Handles human input to make a move."""
    while True:
        try:
            move_input = input("Enter your move (1-9): ")
            move = int(move_input) - 1
            if 0 <= move <= 8 and move in get_available_moves():
                board[move] = 'X'
                break
            else:
                print("Invalid move. The spot is either taken or out of range. Try again.")
        except ValueError:
            print("Please enter a valid number between 1 and 9.")

def play_game():
    """Main game loop."""
    print("================================")
    print(" Welcome to Tic-Tac-Toe with AI!")
    print("================================")
    print("You are 'X' and the AI is 'O'.")
    print("The board positions are numbered 1-9, starting from top-left to bottom-right.")
    print("Example Board:")
    print(" 1 | 2 | 3 ")
    print("---|---|---")
    print(" 4 | 5 | 6 ")
    print("---|---|---")
    print(" 7 | 8 | 9 \n")
    print("Let the game begin!")
    
    print_board()

    while True:
        # Human turn
        human_move()
        print_board()
        if check_win('X'):
            print("Congratulations! You win! (Though this should be impossible against Minimax...)")
            break
        if check_draw():
            print("It's a draw! Well played.")
            break

        # AI turn
        print("AI is making a move...")
        ai_move()
        print_board()
        if check_win('O'):
            print("AI wins! Better luck next time.")
            break
        if check_draw():
            print("It's a draw! Well played.")
            break

if __name__ == "__main__":
    play_game()
