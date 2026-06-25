# 🎱 Billiard Master Simulation — Week 6: UI, Leaderboard, & Bot AI

**Billiard Master** adalah simulasi permainan biliar **8-ball** berbasis desktop yang dikembangkan menggunakan **Python** dan **Pygame**.

---

## 📑 Progres Week 6: UI, Leaderboard, & Bot AI
Pada minggu keenam, kami menambahkan mode Single Player melawan komputer (Bot AI), form input nama terintegrasi dengan database lokal, serta pencatatan skor leaderboard.

### Fitur Utama pada Milestone ini:
- **VS Computer AI Mode**:
  - Bermain melawan Bot AI dengan 4 tingkat kesulitan: **EASY**, **MEDIUM**, **HARD**, dan **MASTER**.
  - AI menggunakan model pencarian heuristik untuk menganalisis lintasan bola ke 6 lubang berbeda dan mensimulasikan sodokan stik secara alami (aiming rotation, power pull-back, delay).
- **Leaderboard local JSON**:
  - Menyimpan data kemenangan secara permanen pada file `leaderboard.json` dan menampilkan daftar TOP 5 pemenang di menu Leaderboard.
- **Nama Form Input & Autocomplete**:
  - Mengingat nama pemain yang pernah di-input sebelumnya lewat database lokal `player_history.json` dan memberikan dropdown autocomplete saat mengetik.
  - Memungkinkan penekanan tombol **Tab** untuk berpindah fokus kolom input Player 1 dan Player 2 secara cepat.
- **Polished UI Consistency**:
  - Mengaplikasikan styling UI polished konsisten (Segoe UI font matching, warna oranye ACCENT_COLOR, panel border radius 12px, background bar HUD 12px, dll).

### 📂 Struktur Proyek pada Week 6:
```
📦 BilliardMaster
┣ 📜 main.py              # GameManager (Game loop, form input autocomplete)
┣ 📜 computer.py          # BilliardAI (Strategi & heuristik bot AI)
┣ 📜 leaderboard.py       # Perekaman data TOP 5 lokal JSON
┣ 📜 cue.py               # Stik Biliar & Prediksi Aiming
┣ 📜 physics.py           # PhysicsEngine
┣ 📜 ball.py              # Class Ball, CueBall, ObjectBall
┣ 📜 table.py             # Class Table
┣ 📜 config.py            # Konstanta Global & Polished UI Colors
┣ 📜 requirements.txt
┗ 📜 README.md
```

---

## 🕹️ Kontrol Permainan
| Aksi | Input |
| ---------- | -------------------------- |
| Membidik | Gerakkan Mouse |
| Kunci Arah | Klik Kiri (1x) |
| Atur Power | Tarik Mouse ke Belakang |
| Tembak | Klik Kiri (2x) |
| Batal Tembakan | Klik Kanan |
| Pindah Input Nama | Tombol **Tab** |
| Pause Game | Tombol di Pojok Kanan Atas |

---

## 👥 Tim Pengembang (Kelompok 7)
* **Fujiono Nur Ikhsan** (1313624008)
* **Muhammad Daffa Ramdhani** (1313624025)
* **Leonard Dwi Chrisdiasa** (1313624031)
