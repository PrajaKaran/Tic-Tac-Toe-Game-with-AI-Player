import tkinter as tk
import math

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe AI (Minimax)")
        self.root.geometry("450x650")
        self.root.configure(bg="#1e1e1e") # Dark theme background
        self.root.resizable(False, False)
        
        self.board = [' ' for _ in range(9)]
        self.buttons = []
        
        # Header Label
        self.title_label = tk.Label(
            self.root, 
            text="Tic-Tac-Toe", 
            font=("Segoe UI", 32, "bold"), 
            bg="#1e1e1e", 
            fg="#ffffff"
        )
        self.title_label.pack(pady=(25, 5))
        
        # Status Label (replaces the annoying popups)
        self.status_label = tk.Label(
            self.root, 
            text="Your Turn (X)", 
            font=("Segoe UI", 16), 
            bg="#1e1e1e", 
            fg="#aaaaaa"
        )
        self.status_label.pack(pady=(0, 25))
        
        # Frame for the board (creates the grid lines)
        self.board_frame = tk.Frame(self.root, bg="#555555")
        self.board_frame.pack()
        
        # Create buttons
        for i in range(9):
            btn = tk.Button(
                self.board_frame, 
                text=' ', 
                font=('Segoe UI', 40, 'bold'), 
                width=4, 
                height=1,
                bg='#2d2d2d',
                fg='#ffffff',
                activebackground='#3d3d3d',
                activeforeground='#ffffff',
                relief=tk.FLAT,
                borderwidth=0,
                cursor="hand2",
                command=lambda i=i: self.human_move(i)
            )
            # Add subtle grid lines by padding the frame
            row = i // 3
            col = i % 3
            btn.grid(row=row, column=col, padx=2, pady=2)
            self.buttons.append(btn)
            
        # Reset Button
        self.reset_btn = tk.Button(
            self.root,
            text="Restart Game",
            font=("Segoe UI", 14, "bold"),
            bg="#007acc",
            fg="#ffffff",
            activebackground="#005999",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            borderwidth=0,
            cursor="hand2",
            command=self.reset_game
        )
        self.reset_btn.pack(pady=40)
        self.reset_btn.config(width=16, height=1)

    def check_win(self, player):
        """Checks if the specified player has won."""
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8], # cols
            [0, 4, 8], [2, 4, 6]             # diagonals
        ]
        for condition in win_conditions:
            if self.board[condition[0]] == self.board[condition[1]] == self.board[condition[2]] == player:
                return condition # Return winning spots to highlight them
        return None

    def check_draw(self):
        """Checks if the game is a draw."""
        return ' ' not in self.board

    def get_available_moves(self):
        """Returns all empty spots on the board."""
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def minimax(self, is_maximizing, depth):
        """Minimax algorithm for AI to choose the best move."""
        if self.check_win('O'):
            return 10 - depth
        if self.check_win('X'):
            return depth - 10
        if self.check_draw():
            return 0

        if is_maximizing:
            best_score = -math.inf
            for move in self.get_available_moves():
                self.board[move] = 'O'
                score = self.minimax(False, depth + 1)
                self.board[move] = ' '
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for move in self.get_available_moves():
                self.board[move] = 'X'
                score = self.minimax(True, depth + 1)
                self.board[move] = ' '
                best_score = min(score, best_score)
            return best_score

    def ai_move(self):
        """Handles the AI's turn."""
        best_score = -math.inf
        best_move = None
        
        # Calculate the best move
        for move in self.get_available_moves():
            self.board[move] = 'O'
            score = self.minimax(False, 0)
            self.board[move] = ' '
            if score > best_score:
                best_score = score
                best_move = move
                
        # Make the move on the board and UI
        if best_move is not None:
            self.board[best_move] = 'O'
            self.buttons[best_move].config(text='O', fg='#ff4a4a', disabledforeground='#ff4a4a', state=tk.DISABLED)
            
        # Check game state after AI move
        win_condition = self.check_win('O')
        if win_condition:
            self.highlight_win(win_condition)
            self.status_label.config(text="AI Wins! Unbeatable.", fg="#ff4a4a")
            self.disable_all_buttons()
        elif self.check_draw():
            self.status_label.config(text="It's a draw!", fg="#aaaaaa")
            self.disable_all_buttons()
        else:
            self.status_label.config(text="Your Turn (X)", fg="#55ff55")

    def human_move(self, i):
        """Handles the human player's click on a grid cell."""
        if self.board[i] == ' ':
            # Update board and UI for Human
            self.board[i] = 'X'
            self.buttons[i].config(text='X', fg='#55ff55', disabledforeground='#55ff55', state=tk.DISABLED)
            
            # Check game state after Human move
            win_condition = self.check_win('X')
            if win_condition:
                self.highlight_win(win_condition)
                self.status_label.config(text="You Win!", fg="#55ff55")
                self.disable_all_buttons()
            elif self.check_draw():
                self.status_label.config(text="It's a draw!", fg="#aaaaaa")
                self.disable_all_buttons()
            else:
                self.status_label.config(text="AI is thinking...", fg="#ffaa00")
                self.root.update()
                # Trigger AI's response with a slight delay
                self.root.after(250, self.ai_move) 

    def highlight_win(self, condition):
        """Highlights the winning row/column/diagonal."""
        for i in condition:
            self.buttons[i].config(bg="#444444")

    def disable_all_buttons(self):
        """Disables buttons when the game is over."""
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)

    def reset_game(self):
        """Resets the board for a new game."""
        self.board = [' ' for _ in range(9)]
        self.status_label.config(text="Your Turn (X)", fg="#aaaaaa")
        for btn in self.buttons:
            btn.config(text=' ', state=tk.NORMAL, bg='#2d2d2d')

if __name__ == "__main__":
    # Initialize the Tkinter application
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()
