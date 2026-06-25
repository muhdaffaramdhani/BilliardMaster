# 🎱 Billiard Master Simulation — Week 5: Game Rules & State Management

**Billiard Master** adalah simulasi permainan biliar **8-ball** berbasis desktop yang dikembangkan menggunakan **Python** dan **Pygame**.

---

## 📑 Progres Week 5: Game Rules & State Management
Pada minggu kelima, aturan permainan biliar 8-ball resmi dan sistem penanganan keadaan game (state machine) telah diimplementasikan sepenuhnya untuk permainan lokal 2-player.

### Fitur Utama pada Milestone ini:
- **Game Rules Integration**:
  - Aturan penentuan jenis bola otomatis (**Solid** atau **Stripes**) setelah bola pertama masuk lubang.
  - Penanganan kondisi **Foul** (bola putih masuk lubang / scratch).
  - Kondisi menang/kalah berdasarkan bola 8 hitam (termasuk kalah langsung jika memasukkan bola 8 sebelum bola kelompok habis).
- **Sistem Turn / Pergantian Pemain**:
  - Menghitung hak tembakan pemain secara bergantian jika tidak ada bola sendiri yang berhasil dimasukkan (*pot*).
- **State Machine & Menu Screens**:
  - Transisi state: Main Menu, Game Match, Game Paused, Settings Menu, Tutorial Menu, Team Menu.
  - Menu Settings dapat mengatur sensitivitas stik biliar dalam game.
- **Polished UI Elements**:
  - Tampilan tombol yang memiliki efek shadow, hover border, dan background transparan halus.
  - Dialog pop-up menu pause dan panel pengaturan dengan border tipis oranye dan border radius rounded 12px.
  - HUD bar atas berwarna gelap minimalis `(12, 14, 18)` dan teks label POWER dengan latar belakang semi-transparan.

### 📂 Struktur Proyek pada Week 5:
```
📦 BilliardMaster
┣ 📜 main.py              # GameManager (State Machine, Rule Engine, Polished UI screens)
┣ 📜 cue.py               # Cue Stick & Prediksi Aiming
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
| Pause Game | Tombol di Pojok Kanan Atas |

---

## 👥 Tim Pengembang (Kelompok 7)
* **Fujiono Nur Ikhsan** (1313624008)
* **Muhammad Daffa Ramdhani** (1313624025)
* **Leonard Dwi Chrisdiasa** (1313624031)
