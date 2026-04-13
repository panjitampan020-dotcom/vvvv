import streamlit as st
import streamlit.components.v1 as components
import chess
from stockfish import Stockfish
import time

# Inisialisasi Stockfish
stockfish = Stockfish(path="./stockfish/stockfish-ubuntu-x86-64-avx2")

# Fungsi untuk mendapatkan langkah terbaik dari Stockfish
def get_best_move(board):
    stockfish.set_fen_position(board.fen())
    return stockfish.get_best_move()

# Fungsi untuk membuat langkah AI
def make_ai_move(board):
    move = get_best_move(board)
    if move:
        board.push_uci(move)
    return move

# Fungsi untuk generate HTML papan catur dengan onclick
def generate_board_html(board, selected_square=None):
    html = """
    <style>
        .chessboard { display: grid; grid-template-columns: repeat(8, 50px); grid-template-rows: repeat(8, 50px); border: 2px solid #333; width: 400px; margin: 0 auto; }
        .square { display: flex; align-items: center; justify-content: center; font-size: 30px; cursor: pointer; font-weight: bold; }
        .light { background-color: #f0d9b5; }
        .dark { background-color: #b58863; }
        .selected { background-color: #ffff00; }
    </style>
    <div class="chessboard">
    """
    for rank in range(7, -1, -1):
        for file in range(8):
            square = chess.square(file, rank)
            piece = board.piece_at(square)
            piece_symbol = piece.symbol() if piece else ""
            color_class = "light" if (rank + file) % 2 == 0 else "dark"
            if selected_square == square:
                color_class = "selected"
            square_name = chr(97 + file) + str(rank + 1)
            html += f'<div class="square {color_class}" onclick="selectSquare(\'{square_name}\')">{piece_symbol}</div>'
    html += """
    </div>
    <script>
        function selectSquare(square) {
            window.parent.postMessage({type: 'select_square', square: square}, '*');
        }
    </script>
    """
    return html

# UI Streamlit
st.title("♟️ Simulasi Papan Catur dengan Stockfish")
st.markdown("Pilih warna dan klik di papan untuk main!")

# Pilih warna
color = st.selectbox("Pilih Warna Anda:", ["Putih (Jalan Duluan)", "Hitam (Musuh Jalan Duluan)"])
player_color = 'white' if color == "Putih (Jalan Duluan)" else 'black'

# Inisialisasi board
if 'board' not in st.session_state:
    st.session_state.board = chess.Board()
    st.session_state.game_over = False
    st.session_state.suggestion = None
    st.session_state.selected_square = None

board = st.session_state.board

# Tampilkan papan catur
components.html(generate_board_html(board, st.session_state.selected_square), height=420)

# Untuk handle klik, gunakan input text sementara (karena postMessage sulit di Streamlit)
if not st.session_state.game_over:
    if (board.turn == chess.WHITE and player_color == 'white') or (board.turn == chess.BLACK and player_color == 'black'):
        move_input = st.text_input("Klik square di papan, atau input manual (e2e4):", key="move")
        if st.button("Jalan!"):
            try:
                move = chess.Move.from_uci(move_input)
                if move in board.legal_moves:
                    board.push(move)
                    st.rerun()
                else:
                    st.error("Langkah tidak valid!")
            except:
                st.error("Format salah!")
    else:
        st.info("Menunggu langkah AI...")
        time.sleep(1)
        ai_move = make_ai_move(board)
        if ai_move:
            st.success(f"AI jalan: {ai_move}")
            st.session_state.suggestion = get_best_move(board)
            st.rerun()
        else:
            st.error("AI tidak bisa jalan!")

# Status permainan
if board.is_checkmate():
    st.success("Checkmate! Game Over.")
    st.session_state.game_over = True
elif board.is_stalemate():
    st.info("Stalemate! Draw.")
    st.session_state.game_over = True
elif board.is_check():
    st.warning("Check!")

# Saran langkah
if st.session_state.suggestion and not st.session_state.game_over:
    st.info(f"Saran langkah berikutnya: {st.session_state.suggestion}")

# Tombol reset
if st.button("Reset Permainan"):
    st.session_state.board = chess.Board()
    st.session_state.game_over = False
    st.session_state.suggestion = None
    st.session_state.selected_square = None
    st.rerun()