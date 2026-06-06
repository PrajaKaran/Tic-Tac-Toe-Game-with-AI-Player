import tkinter as tk
import math
import random

class PremiumTicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe: Advanced AI Edition")
        self.root.geometry("550x700")
        self.root.configure(bg="#0f172a") # Slate 900
        self.root.resizable(False, False)
        
        self.board = [' ' for _ in range(9)]
        self.game_over = False
        self.hovered_cell = None
        
        # Stats tracking
        self.stats = {'X': 0, 'O': 0, 'Draws': 0}
        
        self.setup_ui()
        
    def setup_ui(self):
        # Header Frame
        header_frame = tk.Frame(self.root, bg="#0f172a")
        header_frame.pack(fill=tk.X, pady=(20, 10))
        
        title = tk.Label(header_frame, text="TIC-TAC-TOE", font=("Helvetica", 32, "bold"), bg="#0f172a", fg="#38bdf8")
        title.pack()
        
        subtitle = tk.Label(header_frame, text="Minimax AI Engine", font=("Helvetica", 12), bg="#0f172a", fg="#94a3b8")
        subtitle.pack()

        # Score Board Frame
        score_frame = tk.Frame(self.root, bg="#1e293b")
        score_frame.pack(pady=10, padx=40, fill=tk.X)
        
        self.score_x_lbl = tk.Label(score_frame, text="YOU: 0", font=("Helvetica", 14, "bold"), bg="#1e293b", fg="#4ade80")
        self.score_x_lbl.pack(side=tk.LEFT, padx=30, pady=10)
        
        self.score_draw_lbl = tk.Label(score_frame, text="DRAWS: 0", font=("Helvetica", 14, "bold"), bg="#1e293b", fg="#94a3b8")
        self.score_draw_lbl.pack(side=tk.LEFT, expand=True)
        
        self.score_o_lbl = tk.Label(score_frame, text="AI: 0", font=("Helvetica", 14, "bold"), bg="#1e293b", fg="#f87171")
        self.score_o_lbl.pack(side=tk.RIGHT, padx=30, pady=10)
        
        # Status Label
        self.status_var = tk.StringVar(value="Your Turn (X)")
        self.status_label = tk.Label(self.root, textvariable=self.status_var, font=("Helvetica", 16), bg="#0f172a", fg="#f1f5f9")
        self.status_label.pack(pady=(10, 20))
        
        # Canvas Board for Custom Drawing
        self.canvas = tk.Canvas(self.root, width=390, height=390, bg="#0f172a", highlightthickness=0)
        self.canvas.pack()
        
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Motion>", self.on_hover)
        self.canvas.bind("<Leave>", self.on_leave)
        
        self.draw_board()
        
        # Controls Frame (Difficulty & Reset)
        control_frame = tk.Frame(self.root, bg="#0f172a")
        control_frame.pack(pady=20)
        
        diff_lbl = tk.Label(control_frame, text="AI Level:", font=("Helvetica", 12), bg="#0f172a", fg="#94a3b8")
        diff_lbl.pack(side=tk.LEFT, padx=(0, 10))
        
        self.difficulty = tk.StringVar(value="Unbeatable")
        diff_menu = tk.OptionMenu(control_frame, self.difficulty, "Easy", "Unbeatable")
        diff_menu.config(bg="#1e293b", fg="#f1f5f9", font=("Helvetica", 12), bd=0, highlightthickness=1, indicatoron=0, width=10)
        diff_menu.pack(side=tk.LEFT, padx=10)
        
        reset_btn = tk.Button(control_frame, text="New Game", font=("Helvetica", 12, "bold"), bg="#38bdf8", fg="#0f172a", 
                              activebackground="#0ea5e9", relief=tk.FLAT, padx=20, pady=5, cursor="hand2", command=self.reset_game)
        reset_btn.pack(side=tk.LEFT, padx=20)

    def draw_board(self):
        self.canvas.delete("all")
        # Draw the Grid Lines
        for i in range(1, 3):
            # Vertical
            self.canvas.create_line(i * 130, 10, i * 130, 380, fill="#334155", width=4, capstyle=tk.ROUND)
            # Horizontal
            self.canvas.create_line(10, i * 130, 380, i * 130, fill="#334155", width=4, capstyle=tk.ROUND)
            
        # Draw Symbols
        for i, spot in enumerate(self.board):
            if spot != ' ':
                self.draw_symbol(i, spot)
                
        # Draw Hover Shadow
        if self.hovered_cell is not None and self.board[self.hovered_cell] == ' ' and not self.game_over:
            self.draw_symbol(self.hovered_cell, 'X', ghost=True)

    def draw_symbol(self, index, symbol, ghost=False):
        row = index // 3
        col = index % 3
        x_center = col * 130 + 65
        y_center = row * 130 + 65
        offset = 35
        
        if symbol == 'X':
            color = "#166534" if ghost else "#4ade80" # Ghost is darker
            self.canvas.create_line(x_center - offset, y_center - offset, x_center + offset, y_center + offset, fill=color, width=8, capstyle=tk.ROUND)
            self.canvas.create_line(x_center + offset, y_center - offset, x_center - offset, y_center + offset, fill=color, width=8, capstyle=tk.ROUND)
        elif symbol == 'O':
            color = "#991b1b" if ghost else "#f87171"
            self.canvas.create_oval(x_center - offset, y_center - offset, x_center + offset, y_center + offset, outline=color, width=8)

    def on_hover(self, event):
        if self.game_over: return
        col = event.x // 130
        row = event.y // 130
        if 0 <= col <= 2 and 0 <= row <= 2:
            cell = row * 3 + col
            if cell != self.hovered_cell:
                self.hovered_cell = cell
                self.draw_board()

    def on_leave(self, event):
        self.hovered_cell = None
        self.draw_board()

    def on_click(self, event):
        if self.game_over: return
        col = event.x // 130
        row = event.y // 130
        if 0 <= col <= 2 and 0 <= row <= 2:
            cell = row * 3 + col
            if self.board[cell] == ' ':
                self.board[cell] = 'X'
                self.hovered_cell = None
                self.draw_board()
                self.check_game_state('X')
                
                if not self.game_over:
                    self.status_var.set("AI is thinking...")
                    self.root.update()
                    self.root.after(400, self.ai_move) # Delay for realism

    def check_win(self, player):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8], # cols
            [0, 4, 8], [2, 4, 6]             # diagonals
        ]
        for condition in win_conditions:
            if self.board[condition[0]] == self.board[condition[1]] == self.board[condition[2]] == player:
                return condition
        return None

    def check_draw(self):
        return ' ' not in self.board

    def get_available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def minimax(self, is_maximizing, depth):
        if self.check_win('O'): return 10 - depth
        if self.check_win('X'): return depth - 10
        if self.check_draw(): return 0

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
        if self.game_over: return
        
        available = self.get_available_moves()
        if not available: return

        if self.difficulty.get() == "Easy":
            # Random move for easy difficulty
            best_move = random.choice(available)
        else:
            # Unbeatable Minimax
            best_score = -math.inf
            best_move = None
            for move in available:
                self.board[move] = 'O'
                score = self.minimax(False, 0)
                self.board[move] = ' '
                if score > best_score:
                    best_score = score
                    best_move = move
                    
        if best_move is not None:
            self.board[best_move] = 'O'
            self.draw_board()
            self.check_game_state('O')

    def check_game_state(self, player):
        win_condition = self.check_win(player)
        if win_condition:
            self.game_over = True
            self.draw_winning_line(win_condition)
            if player == 'X':
                self.status_var.set("You Win! Impossible!")
                self.stats['X'] += 1
            else:
                self.status_var.set("AI Wins! Better luck next time.")
                self.stats['O'] += 1
            self.update_score_labels()
        elif self.check_draw():
            self.game_over = True
            self.status_var.set("It's a Draw!")
            self.stats['Draws'] += 1
            self.update_score_labels()
        else:
            if player == 'X':
                self.status_var.set("AI is thinking...")
            else:
                self.status_var.set("Your Turn (X)")

    def draw_winning_line(self, condition):
        # Calculate coordinates for the winning line
        p1 = condition[0]
        p2 = condition[2]
        
        r1, c1 = p1 // 3, p1 % 3
        r2, c2 = p2 // 3, p2 % 3
        
        x1 = c1 * 130 + 65
        y1 = r1 * 130 + 65
        x2 = c2 * 130 + 65
        y2 = r2 * 130 + 65
        
        # Extend line slightly past the center of the edge squares
        if r1 == r2: # Horizontal
            x1 -= 40; x2 += 40
        elif c1 == c2: # Vertical
            y1 -= 40; y2 += 40
        else: # Diagonal
            if x1 < x2:
                x1 -= 30; y1 -= 30; x2 += 30; y2 += 30
            else:
                x1 += 30; y1 -= 30; x2 -= 30; y2 += 30

        self.canvas.create_line(x1, y1, x2, y2, fill="#fbbf24", width=12, capstyle=tk.ROUND)

    def update_score_labels(self):
        self.score_x_lbl.config(text=f"YOU: {self.stats['X']}")
        self.score_o_lbl.config(text=f"AI: {self.stats['O']}")
        self.score_draw_lbl.config(text=f"DRAWS: {self.stats['Draws']}")

    def reset_game(self):
        self.board = [' ' for _ in range(9)]
        self.game_over = False
        self.hovered_cell = None
        self.status_var.set("Your Turn (X)")
        self.draw_board()

if __name__ == "__main__":
    root = tk.Tk()
    app = PremiumTicTacToe(root)
    root.mainloop()
