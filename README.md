# Simulasi Catur dengan Stockfish (Python + Streamlit)

Aplikasi web sederhana untuk simulasi permainan catur dengan AI Stockfish menggunakan Python dan Streamlit.

## Cara Menjalankan

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Jalankan aplikasi:
   ```
   streamlit run app.py
   ```

3. Buka browser di URL yang diberikan (biasanya http://localhost:8501).

## Fitur

- Pilih warna (Putih atau Hitam).
- Input langkah manual dengan format UCI (contoh: e2e4).
- AI (Stockfish) jalan otomatis untuk lawan.
- Saran langkah terbaik dari Stockfish.
- Reset permainan.

## Teknologi

- Python
- Streamlit (UI web)
- Chess (logika catur)
- Stockfish (engine AI)
- CairoSVG & Pillow (rendering papan)# Simulasi Papan Catur dengan Stockfish

Aplikasi web sederhana untuk simulasi permainan catur di mana Stockfish memberikan saran langkah.

## Cara Menjalankan

1. Jalankan server HTTP lokal:
   ```
   python3 -m http.server 8000
   ```

2. Buka browser dan akses `http://localhost:8000`

3. Pilih warna (Putih atau Hitam), klik "Mulai Permainan"

4. Jika Putih: Anda jalan duluan, lalu musuh (AI) jalan, lalu Stockfish memberikan saran langkah berikutnya.

5. Jika Hitam: Musuh jalan duluan, lalu Anda jalan, lalu saran dari Stockfish.

## Fitur

- Papan catur interaktif
- Integrasi dengan Stockfish untuk saran langkah
- AI lawan menggunakan Stockfish
- UI sederhana dan responsif

## Teknologi

- HTML, CSS, JavaScript
- Chess.js untuk logika catur
- Chessboard.js untuk tampilan papan
- Stockfish.js untuk engine catur