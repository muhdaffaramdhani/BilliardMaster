# 🎱 Billiard Master Simulation — Week 4: Cue Stick Mechanics

**Billiard Master** adalah simulasi permainan biliar **8-ball** berbasis desktop yang dikembangkan menggunakan **Python** dan **Pygame**.

---

## 📑 Progres Week 4: Cue Stick Mechanics
Pada minggu keempat, stik billiard diubah menjadi interaktif sepenuhnya dengan kontrol dua tahap dan alat bantu prediksi bidikan.

### Fitur & Batasan pada Milestone ini:
- **Precision Aiming & Prediction**:
  - Menampilkan *aiming guideline* (garis bidik) dan *ghost ball* untuk memproyeksikan posisi tumbukan pertama bola target serta lintasan pantul bola putih.
- **Two-Stage Shooting Mechanics**:
  - Klik ke-1: Mengunci arah bidikan stik.
  - Tarik mouse ke belakang: Mengatur kekuatan pukulan (*cue power*).
  - Klik ke-2: Menembak bola putih dengan impuls kecepatan yang sesuai tarikan mouse.
  - Klik kanan: Membatalkan tarikan stik (reset state ke bidik arah).
- **Power Bar Overlay**:
  - Menggambar progress bar kekuatan tembakan secara dinamis di atas layar game.

### 📂 Struktur Proyek pada Week 4:
```
📦 BilliardMaster
┣ 📜 main.py              # GameManager (Mengintegrasikan input mouse ke stik & HUD power)
┣ 📜 cue.py               # Stik Biliar, Rotasi, Tarikan Power, & Prediksi Bidikan
┣ 📜 physics.py           # PhysicsEngine (Deteksi lintasan prediksi ghost ball)
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

---

## 👥 Tim Pengembang (Kelompok 7)
* **Fujiono Nur Ikhsan** (1313624008)
* **Muhammad Daffa Ramdhani** (1313624025)
* **Leonard Dwi Chrisdiasa** (1313624031)
