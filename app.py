import streamlit as st
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

# Fungsi untuk render papan sebagai grid klik
def render_board(board, selected_square=None):
    st.subheader("Papan Catur - Klik untuk Pilih dan Jalan")
    cols = st.columns(8)
    squares = []
    for rank in range(7, -1, -1):  # Dari 8 ke 1
        for file in range(8):  # a ke h
            square = chess.square(file, rank)
            piece = board.piece_at(square)
            piece_symbol = piece.symbol() if piece else ""
            color = "light" if (rank + file) % 2 == 0 else "dark"
            if selected_square == square:
                color = "selected"
            button_label = f"{chr(97 + file)}{rank + 1}\n{piece_symbol}"
            if cols[file].button(button_label, key=f"{file}_{rank}", help=f"Square {chr(97 + file)}{rank + 1}"):
                return square
    return None

# UI Streamlit
st.title("♟️ Simulasi Papan Catur dengan Stockfish")
st.markdown("Pilih warna dan klik pada papan untuk jalan!")

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

# Status permainan
if board.is_checkmate():
    st.success("Checkmate! Game Over.")
    st.session_state.game_over = True
elif board.is_stalemate():
    st.info("Stalemate! Draw.")
    st.session_state.game_over = True
elif board.is_check():
    st.warning("Check!")

# Render papan dan handle klik
if not st.session_state.game_over:
    if (board.turn == chess.WHITE and player_color == 'white') or (board.turn == chess.BLACK and player_color == 'black'):
        clicked_square = render_board(board, st.session_state.selected_square)
        if clicked_square is not None:
            if st.session_state.selected_square is None:
                # Pilih piece
                piece = board.piece_at(clicked_square)
                if piece and piece.color == board.turn:
                    st.session_state.selected_square = clicked_square
                    st.rerun()
            else:
                # Coba jalan
                move = chess.Move(st.session_state.selected_square, clicked_square)
                if move in board.legal_moves:
                    board.push(move)
                    st.session_state.selected_square = None
                    st.rerun()
                else:
                    # Promotion atau invalid
                    st.session_state.selected_square = None
                    st.error("Langkah tidak valid!")
                    st.rerun()
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