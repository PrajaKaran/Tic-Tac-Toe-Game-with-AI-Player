const cells = document.querySelectorAll('.cell');
const statusText = document.getElementById('status-text');
const resetBtn = document.getElementById('reset-btn');
const difficultySelect = document.getElementById('difficulty');
const winningLine = document.getElementById('winning-line');

// Score elements
const scorePlayerEl = document.getElementById('score-player');
const scoreAiEl = document.getElementById('score-ai');
const scoreDrawsEl = document.getElementById('score-draws');

let board = ['', '', '', '', '', '', '', '', ''];
let currentPlayer = 'X';
let running = false;

let stats = { player: 0, ai: 0, draws: 0 };

const winConditions = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8], // rows
    [0, 3, 6], [1, 4, 7], [2, 5, 8], // cols
    [0, 4, 8], [2, 4, 6]             // diagonals
];

initializeGame();

function initializeGame() {
    cells.forEach(cell => cell.addEventListener('click', cellClicked));
    resetBtn.addEventListener('click', restartGame);
    running = true;
    statusText.textContent = "Your Turn (X)";
    statusText.style.color = "#4ade80";
    winningLine.style.strokeDashoffset = "500"; // Hide line
}

function cellClicked() {
    const cellIndex = this.getAttribute('data-index');

    if (board[cellIndex] !== '' || !running || currentPlayer !== 'X') {
        return;
    }

    updateCell(this, cellIndex, 'X');
    checkWinner();

    if (running) {
        currentPlayer = 'O';
        statusText.textContent = "AI is thinking...";
        statusText.style.color = "#fbbf24";
        setTimeout(aiMove, 300); // Small delay for realism
    }
}

function updateCell(cell, index, player) {
    board[index] = player;
    cell.textContent = player;
    cell.classList.add(player.toLowerCase());
}

function getAvailableMoves(currentBoard) {
    let moves = [];
    for (let i = 0; i < currentBoard.length; i++) {
        if (currentBoard[i] === '') moves.push(i);
    }
    return moves;
}

function checkWinCondition(currentBoard, player) {
    for (let condition of winConditions) {
        if (currentBoard[condition[0]] === player && 
            currentBoard[condition[1]] === player && 
            currentBoard[condition[2]] === player) {
            return condition;
        }
    }
    return null;
}

function checkDrawCondition(currentBoard) {
    return !currentBoard.includes('');
}

function minimax(newBoard, isMaximizing, depth) {
    if (checkWinCondition(newBoard, 'O')) return 10 - depth;
    if (checkWinCondition(newBoard, 'X')) return depth - 10;
    if (checkDrawCondition(newBoard)) return 0;

    let availableMoves = getAvailableMoves(newBoard);

    if (isMaximizing) {
        let bestScore = -Infinity;
        for (let move of availableMoves) {
            newBoard[move] = 'O';
            let score = minimax(newBoard, false, depth + 1);
            newBoard[move] = '';
            bestScore = Math.max(score, bestScore);
        }
        return bestScore;
    } else {
        let bestScore = Infinity;
        for (let move of availableMoves) {
            newBoard[move] = 'X';
            let score = minimax(newBoard, true, depth + 1);
            newBoard[move] = '';
            bestScore = Math.min(score, bestScore);
        }
        return bestScore;
    }
}

function aiMove() {
    let availableMoves = getAvailableMoves(board);
    if (availableMoves.length === 0 || !running) return;

    let bestMove;
    const difficulty = difficultySelect.value;

    if (difficulty === 'easy') {
        // Random move
        bestMove = availableMoves[Math.floor(Math.random() * availableMoves.length)];
    } else {
        // Unbeatable Minimax
        let bestScore = -Infinity;
        for (let move of availableMoves) {
            board[move] = 'O';
            let score = minimax(board, false, 0);
            board[move] = '';
            if (score > bestScore) {
                bestScore = score;
                bestMove = move;
            }
        }
    }

    const cell = document.querySelector(`.cell[data-index="${bestMove}"]`);
    updateCell(cell, bestMove, 'O');
    checkWinner();

    if (running) {
        currentPlayer = 'X';
        statusText.textContent = "Your Turn (X)";
        statusText.style.color = "#4ade80";
    }
}

function drawWinningLine(condition) {
    const startCell = document.querySelector(`.cell[data-index="${condition[0]}"]`);
    const endCell = document.querySelector(`.cell[data-index="${condition[2]}"]`);
    
    // We are overlaying SVG on top of the CSS Grid
    // Since CSS grid is responsive, we need to calculate exact positions relative to board
    const boardEl = document.getElementById('board');
    const boardRect = boardEl.getBoundingClientRect();
    const startRect = startCell.getBoundingClientRect();
    const endRect = endCell.getBoundingClientRect();

    let x1 = (startRect.left - boardRect.left) + (startRect.width / 2);
    let y1 = (startRect.top - boardRect.top) + (startRect.height / 2);
    let x2 = (endRect.left - boardRect.left) + (endRect.width / 2);
    let y2 = (endRect.top - boardRect.top) + (endRect.height / 2);

    // Extend line slightly
    const angle = Math.atan2(y2 - y1, x2 - x1);
    const padding = 20;
    
    winningLine.setAttribute('x1', x1 - Math.cos(angle) * padding);
    winningLine.setAttribute('y1', y1 - Math.sin(angle) * padding);
    winningLine.setAttribute('x2', x2 + Math.cos(angle) * padding);
    winningLine.setAttribute('y2', y2 + Math.sin(angle) * padding);
    
    // Trigger CSS animation
    setTimeout(() => {
        winningLine.style.strokeDashoffset = "0";
    }, 50);
}

function checkWinner() {
    let xWin = checkWinCondition(board, 'X');
    let oWin = checkWinCondition(board, 'O');

    if (xWin) {
        statusText.textContent = "You Win! (Impossible!)";
        statusText.style.color = "#4ade80";
        running = false;
        stats.player++;
        scorePlayerEl.textContent = stats.player;
        drawWinningLine(xWin);
    } else if (oWin) {
        statusText.textContent = "AI Wins! Unbeatable.";
        statusText.style.color = "#f87171";
        running = false;
        stats.ai++;
        scoreAiEl.textContent = stats.ai;
        drawWinningLine(oWin);
    } else if (checkDrawCondition(board)) {
        statusText.textContent = "It's a Draw!";
        statusText.style.color = "#94a3b8";
        running = false;
        stats.draws++;
        scoreDrawsEl.textContent = stats.draws;
    }
}

function restartGame() {
    board = ['', '', '', '', '', '', '', '', ''];
    currentPlayer = 'X';
    cells.forEach(cell => {
        cell.textContent = '';
        cell.classList.remove('x', 'o');
    });
    
    winningLine.style.strokeDashoffset = "500"; // Hide line immediately
    
    statusText.textContent = "Your Turn (X)";
    statusText.style.color = "#4ade80";
    running = true;
}
