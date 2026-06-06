# Tic-Tac-Toe with AI Player 🎮

**Artificial Intelligence – Internship Project 2**

This repository contains a Python implementation of a Tic-Tac-Toe game featuring an unbeatable AI opponent powered by the **Minimax algorithm**. 

## 🧠 Concepts Demonstrated
- Game Theory & Adversarial Search
- Recursive Algorithms (Minimax)
- AI Move Prediction & Decision Making
- Graphical User Interface (GUI) design in Python

## 📂 Project Files
This project includes three different variations of the game to demonstrate progression from basic logic to advanced UI:

1. **`tic_tac_toe.py` (CLI Version)**
   - A fully functional text-based version playable in the terminal.
2. **`tic_tac_toe_gui.py` (Basic GUI)**
   - A standard windowed graphical interface built using Python's built-in `tkinter`.
3. **`tic_tac_toe_pro.py` (Premium Custom GUI)**
   - A highly polished interface featuring a custom canvas rendering engine, hover animations, persistent score tracking, and difficulty selectors (Easy vs Unbeatable Minimax).

## 🚀 How to Run

### Prerequisites
You only need Python installed on your system. No external libraries are required.

### Running the Game
1. Clone the repository:
   ```bash
   git clone https://github.com/PrajaKaran/Tic-Tac-Toe-Game-with-AI-Player.git
   cd Tic-Tac-Toe-Game-with-AI-Player
   ```

2. Run your preferred version using Python:

   **For the Advanced Premium GUI (Recommended):**
   ```bash
   python tic_tac_toe_pro.py
   ```

   **For the standard GUI:**
   ```bash
   python tic_tac_toe_gui.py
   ```

   **For the Terminal CLI version:**
   ```bash
   python tic_tac_toe.py
   ```

## 🤖 How the Minimax AI Works
The AI uses the **Minimax Algorithm**, a backtracking algorithm used in decision making and game theory. It explores all possible future moves on the board until it reaches a terminal state (Win, Lose, or Draw). 
- It assigns a positive score (+10) if the AI wins.
- It assigns a negative score (-10) if the human wins.
- It assigns 0 for a draw.

By maximizing its own score and assuming the human is playing optimally to minimize it, the AI maps out a decision tree that ensures it will **always** either win or force a draw. It is mathematically unbeatable!
