# 🎱 Billiard Master Simulation — Week 3: Physics Engine Baseline

**Billiard Master** adalah simulasi permainan biliar **8-ball** berbasis desktop yang dikembangkan menggunakan **Python** dan **Pygame**.

---

## 📑 Progres Week 3: Physics Engine Baseline
Pada minggu ketiga, fokus pengembangan dialihkan ke pembuatan engine simulasi fisika 2D realistis untuk benturan dan gesekan bola.

### Fitur & Batasan pada Milestone ini:
- **Physics Engine 2D**:
  - Implementasi deteksi tumbukan lingkaran-lingkaran (ball-to-ball) dan lingkaran-garis (ball-to-cushion).
  - Penyelesaian transfer momentum elastis dan koreksi *positional overlap* untuk mencegah bola bertumpuk.
- **Friction & Friction Deceleration**:
  - Simulasi perlambatan kecepatan bola akibat gesekan dengan kain meja laken.
- **Interactive Shoot Testing**:
  - Klik mouse akan menembakkan bola putih (Cue Ball) secara langsung ke arah kursor mouse dengan kecepatan konstan untuk mempermudah pengujian benturan bola di meja.

### 📂 Struktur Proyek pada Week 3:
```
📦 BilliardMaster
┣ 📜 main.py              # GameManager (Game Loop & Input tembakan test)
┣ 📜 physics.py           # PhysicsEngine (Deteksi & resolusi tumbukan 2D)
┣ 📜 ball.py              # Class Ball, CueBall, ObjectBall (Fisika batas dinding)
┣ 📜 table.py             # Class Table (Visual meja & cushion)
┣ 📜 cue.py               # Class Cue (Visual pointer stub)
┣ 📜 config.py            # Konstanta Global & Polished UI Colors
┣ 📜 requirements.txt
┗ 📜 README.md
```

---

## 🛠️ Instalasi & Menjalankan Program
Jalankan perintah berikut untuk menguji engine fisika:
```bash
pip install -r requirements.txt
python main.py
```
**Kontrol Pengujian**: Klik kiri di mana saja pada layar untuk melontarkan bola putih ke arah kursor mouse.

---

## 👥 Tim Pengembang (Kelompok 7)
* **Fujiono Nur Ikhsan** (1313624008)
* **Muhammad Daffa Ramdhani** (1313624025)
* **Leonard Dwi Chrisdiasa** (1313624031)
