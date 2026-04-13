# Simulasi Papan Catur dengan Stockfish

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