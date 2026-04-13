import streamlit as st
import chess
import chess.svg
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

# UI Streamlit
st.title("♟️ Simulasi Papan Catur dengan Stockfish")
st.markdown("Pilih warna dan mainkan catur dengan arahan AI!")

# Pilih warna
color = st.selectbox("Pilih Warna Anda:", ["Putih (Jalan Duluan)", "Hitam (Musuh Jalan Duluan)"])
player_color = 'white' if color == "Putih (Jalan Duluan)" else 'black'

# Inisialisasi board
if 'board' not in st.session_state:
    st.session_state.board = chess.Board()
    st.session_state.game_over = False
    st.session_state.suggestion = None

board = st.session_state.board

# Tampilkan papan catur
st.subheader("Papan Catur")
board_svg = chess.svg.board(board=board, size=400)
st.image(board_svg, use_column_width=True)

# Status permainan
if board.is_checkmate():
    st.success("Checkmate! Game Over.")
    st.session_state.game_over = True
elif board.is_stalemate():
    st.info("Stalemate! Draw.")
    st.session_state.game_over = True
elif board.is_check():
    st.warning("Check!")

# Input langkah pemain
if not st.session_state.game_over:
    if (board.turn == chess.WHITE and player_color == 'white') or (board.turn == chess.BLACK and player_color == 'black'):
        move_input = st.text_input("Masukkan langkah Anda (contoh: e2e4):", key="move")
        if st.button("Jalan!"):
            try:
                move = chess.Move.from_uci(move_input)
                if move in board.legal_moves:
                    board.push(move)
                    st.rerun()
                else:
                    st.error("Langkah tidak valid!")
            except:
                st.error("Format langkah salah! Gunakan UCI, contoh: e2e4")
    else:
        st.info("Menunggu langkah AI...")
        time.sleep(1)  # Simulasi delay
        ai_move = make_ai_move(board)
        if ai_move:
            st.success(f"AI jalan: {ai_move}")
            st.session_state.suggestion = get_best_move(board)  # Saran untuk pemain berikutnya
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
    st.rerun()