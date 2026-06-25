# 🎱 Billiard Master Simulation — Week 2: System Design Baseline

**Billiard Master** adalah simulasi permainan biliar **8-ball** berbasis desktop yang dikembangkan menggunakan **Python** dan **Pygame**.

---

## 📑 Progres Week 2: System Design Baseline
Pada minggu kedua, kami mengimplementasikan model dasar (class hierarchy) berorientasi objek untuk merender meja biliar dan bola secara dinamis.

### Fitur & Batasan pada Milestone ini:
- **Modular OOP Class Hierarchy**:
  - `Ball` (base class) untuk mendefinisikan posisi, radius, kecepatan, dan method menggambar dasar.
  - `CueBall` dan `ObjectBall` mewarisi `Ball`.
- **Render Table & Cushion Geometry**:
  - `Table` menangani visual batas meja, cushion, dan 6 lubang (pockets) permainan.
- **Visual Cue Stick Stub**:
  - `Cue` diimplementasikan sebagai visual pointer (hanya menggambar stik billiard yang mengarah ke pointer mouse).
- **GameLoop Baseline**:
  - `main.py` menginisialisasi pygame window, merender 15 object balls dalam susunan segitiga dan 1 cue ball, tanpa aturan permainan (rules), interaksi tumbukan bola, ataupun bot AI.

### 📂 Struktur Proyek pada Week 2:
```
📦 BilliardMaster
┣ 📜 main.py              # GameManager (Game Loop & render meja)
┣ 📜 ball.py              # Class Ball, CueBall, ObjectBall
┣ 📜 table.py             # Class Table (Visual meja & pocket)
┣ 📜 cue.py               # Class Cue (Visual stub stik billiard)
┣ 📜 config.py            # Konstanta Global & Polished UI Colors
┣ 📜 requirements.txt
┗ 📜 README.md
```

---

## 🛠️ Instalasi & Menjalankan Program
Jalankan perintah berikut untuk memulai simulasi visual baseline:
```bash
pip install -r requirements.txt
python main.py
```
*(Catatan: Pada tahap ini bola belum bisa memantul atau berinteraksi satu sama lain karena engine fisika belum diimplementasikan).*

---

## 👥 Tim Pengembang (Kelompok 7)
* **Fujiono Nur Ikhsan** (1313624008)
* **Muhammad Daffa Ramdhani** (1313624025)
* **Leonard Dwi Chrisdiasa** (1313624031)
