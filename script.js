let game = new Chess();
let board = null;
let playerColor = 'white';
let stockfish = new Worker('https://unpkg.com/stockfish.js@10.0.2/stockfish.js');

stockfish.postMessage('uci');
stockfish.postMessage('isready');

function onDragStart(source, piece, position, orientation) {
    if (game.game_over()) return false;
    if ((game.turn() === 'w' && playerColor !== 'white') || (game.turn() === 'b' && playerColor !== 'black')) return false;
    if ((game.turn() === 'w' && piece.search(/^b/) !== -1) || (game.turn() === 'b' && piece.search(/^w/) !== -1)) return false;
}

function onDrop(source, target) {
    let move = game.move({
        from: source,
        to: target,
        promotion: 'q'
    });
    if (move === null) return 'snapback';
    updateStatus();
    if (!game.game_over()) {
        setTimeout(makeAIMove, 500);
    }
}

function onSnapEnd() {
    board.position(game.fen());
}

function updateStatus() {
    let status = '';
    let moveColor = 'Putih';
    if (game.turn() === 'b') {
        moveColor = 'Hitam';
    }
    if (game.in_checkmate()) {
        status = 'Game over, ' + moveColor + ' is in checkmate.';
    } else if (game.in_draw()) {
        status = 'Game over, drawn position';
    } else {
        status = 'Giliran ' + moveColor;
        if (game.in_check()) {
            status += ', ' + moveColor + ' is in check';
        }
    }
    document.getElementById('turn-info').textContent = status;
}

function makeAIMove() {
    if (game.game_over()) return;
    getBestMove(function(bestMove) {
        game.move(bestMove);
        board.position(game.fen());
        updateStatus();
        if (!game.game_over()) {
            getSuggestion();
        }
    });
}

function getBestMove(callback) {
    stockfish.postMessage('position fen ' + game.fen());
    stockfish.postMessage('go movetime 1000');
    stockfish.onmessage = function(event) {
        let line = event.data;
        if (line.startsWith('bestmove')) {
            let bestMove = line.split(' ')[1];
            callback(bestMove);
        }
    };
}

function getSuggestion() {
    stockfish.postMessage('position fen ' + game.fen());
    stockfish.postMessage('go movetime 1000');
    stockfish.onmessage = function(event) {
        let line = event.data;
        if (line.startsWith('bestmove')) {
            let bestMove = line.split(' ')[1];
            document.getElementById('suggestion').textContent = 'Saran langkah: ' + bestMove;
        }
    };
}

function startGame() {
    playerColor = document.getElementById('color-select').value;
    game = new Chess();
    board = Chessboard('board', {
        draggable: true,
        position: 'start',
        onDragStart: onDragStart,
        onDrop: onDrop,
        onSnapEnd: onSnapEnd
    });
    updateStatus();
    if (playerColor === 'black') {
        setTimeout(makeAIMove, 500);
    } else {
        getSuggestion();
    }
}

function resetGame() {
    game = new Chess();
    if (board) {
        board.position('start');
    }
    document.getElementById('turn-info').textContent = 'Pilih warna dan klik Mulai';
    document.getElementById('suggestion').textContent = 'Saran langkah: -';
}

document.getElementById('start-btn').addEventListener('click', startGame);
document.getElementById('reset-btn').addEventListener('click', resetGame);