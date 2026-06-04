# 🎱 Billiard Master Simulation

**Billiard Master** adalah simulasi permainan biliar **8-ball** berbasis desktop yang dikembangkan menggunakan **Python** dan **Pygame**. Proyek ini dirancang sebagai **Final Project** untuk mata kuliah **Desain dan Pemrograman Berorientasi Objek** serta **Rekayasa Perangkat Lunak**, dengan fokus pada penerapan **OOP**, **fisika 2D realistis**, serta **manajemen data lokal**.

---

## 📑 Table of Contents
- [Pendahuluan](#-pendahuluan)
- [Fitur Utama](#-fitur-utama)
- [Teknologi yang Digunakan](#-teknologi-yang-digunakan)
- [Struktur Proyek](#-struktur-proyek)
- [Instalasi & Menjalankan Program](#-instalasi--menjalankan-program)
- [Membuat File Executable (.exe)](#-membuat-file-executable-exe)
- [Kontrol Permainan](#-kontrol-permainan)
- [Tim Pengembang](#-tim-pengembang)
- [Lisensi](#-lisensi)

---

## 📘 Pendahuluan

Billiard Master mensimulasikan permainan biliar 8-ball dengan aturan resmi dan mekanisme permainan yang realistis. Game ini menerapkan:
- **Object-Oriented Programming (OOP)**
- **Physics Engine 2D**
- **Collision Detection & Resolution**
- **Local Leaderboard berbasis file JSON**

---

## ✨ Fitur Utama

### 🎮 Gameplay & Fisika
- **Realistic Physics Engine**  
  Simulasi tumbukan elastis, gesekan (friction), dan transfer momentum antar bola.
  
- **Precision Aiming System**  
  Dilengkapi *guide line* dan *ghost ball* untuk memprediksi arah bola.

- **Mekanisme Stik 2-Tahap**  
  - Klik pertama: mengunci arah  
  - Tarik mouse: mengatur kekuatan  
  - Klik kedua: menembak
  
- **Peraturan 8-Ball Resmi**
  - Foul jika bola putih masuk lubang  
  - Penentuan otomatis bola **Solid / Stripes**  
  - Kondisi menang/kalah berdasarkan bola 8  

- **VS Computer AI Mode** (New!)
  - Bermain single player melawan bot AI dengan 4 tingkat kesulitan: **EASY**, **MEDIUM**, **HARD**, dan **MASTER**.
  - AI menganalisis lintasan bola ke 6 lubang berbeda menggunakan model heuristik untuk menemukan tembakan terbaik.
  - Alur bermain AI didukung animasi natural (aiming rotation, power pull-back, short pause) yang menyerupai perilaku manusia.
  - Akurasi tembakan dan strategi pemilihan bola disesuaikan secara dinamis berdasarkan tingkat kesulitan (pada level **MASTER**, tembakan AI menjadi 100% akurat secara matematis).

### 🏆 Fitur Final Update & Pengaturan
- **Autocomplete & Dropdown Saran Nama** (New!)
  - Mengingat nama pemain yang pernah di-input sebelumnya lewat database lokal `player_history.json`.
  - Memberikan saran nama otomatis saat mengetik di input box.
  
- **Tab Focus Navigation** (New!)
  - Memudahkan navigasi form input nama dengan menekan tombol **Tab** untuk berpindah focus field (Player 1 <=> Player 2).

- **Realistis Procedural Audio Engine** (New!)
  - Menghasilkan audio billiard beneran secara matematis (tanpa file eksternal):
    - *Ball Hit*: clack nyaring khas bola akrilik.
    - *Cue Hit*: suara kayu stik menyodok bola putih.
    - *Wall Cushion*: thud teredam saat memantul di karet meja.
    - *Pocket Pot*: gabungan suara rattle stik pembatas dan drop lubang.
  - Volume efek suara disesuaikan secara dinamis berdasarkan kekuatan benturan/kecepatan bola.

- **Menu Pengaturan & Pause Fleksibel** (New!)
  - Tombol **SETTINGS** terintegrasi di pause menu dalam game, sehingga pengaturan suara/sensitivitas bisa diubah tanpa perlu keluar dari match.
  - Pengaturan sensitivitas stik kini memiliki 5 tingkat presisi dan bisa diubah menggunakan mouse atau digeser dengan tombol panah kiri-kanan saat di-hover.
  
- **Local Leaderboard**  
  Menyimpan nama pemenang dan jumlah kemenangan secara permanen menggunakan file JSON.

---

## 🛠️ Teknologi yang Digunakan

| Komponen | Teknologi |
|--------|----------|
| Bahasa | Python 3.x |
| Library | Pygame |
| Audio | Procedural Synthesized Sound (Stereo/Mono, Volume Dynamic) |
| Data Storage | JSON (Leaderboard & Player History) |

---

## 📂 Struktur Proyek

Proyek ini dirancang secara modular dengan prinsip **OOP**:

```
📦 BilliardMaster
┣ 📜 main.py              # GameManager (Game Loop, State Machine, Input form)
┣ 📜 computer.py          # BilliardAI (AI Decision-making Heuristics & Difficulty levels)
┣ 📜 physics.py           # PhysicsEngine (Collision & Vector Math)
┣ 📜 ball.py              # Ball, CueBall, ObjectBall (Inheritance & Collision)
┣ 📜 cue.py               # Cue Stick & Aiming Logic
┣ 📜 table.py             # Meja, Cushion, Area Lubang Permainan
┣ 📜 leaderboard.py       # I/O JSON Leaderboard
┣ 📜 config.py            # Konstanta Global (Warna, FPS, Sensitivity Levels)
┣ 📜 requirements.txt
┣ 📜 leaderboard.json
┗ 📜 player_history.json  # Database riwayat input nama user
```

---

## 🚀 Instalasi & Menjalankan Program

### 1️⃣ Prasyarat
- Python **3.8 atau lebih baru**

### 2️⃣ Instalasi Dependency
Jalankan perintah berikut di terminal:

```bash
pip install -r requirements.txt
```

### 3️⃣ Menjalankan Game

```bash
python main.py
```

---

## 📦 Membuat File Executable (.exe)

Agar game dapat dijalankan tanpa Python:

### 1️⃣ Instal PyInstaller

```bash
pip install pyinstaller
```

### 2️⃣ Build Executable

```bash
pyinstaller --noconfirm --onefile --windowed --name "BilliardMaster" main.py
```

### 3️⃣ Hasil Build

* File `.exe` akan tersedia di folder:

```
dist/BilliardMaster.exe
```

Executable ini dapat dibagikan dan dijalankan di komputer lain tanpa instalasi Python.

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
| Ubah Sensitivitas | Hover + **Panah Kanan / Panah Kiri** (Di Menu Settings) |
| Pause Game | Tombol di Pojok Kanan Atas |

---

## 👥 Tim Pengembang (Kelompok 7)

* **Fujiono Nur Ikhsan** (1313624008)
* **Muhammad Daffa Ramdhani** (1313624025)
* **Leonard Dwi Chrisdiasa** (1313624031)

---

## 📄 Lisensi

Proyek ini dibuat **khusus untuk keperluan akademik** sebagai Tugas Akhir Mata Kuliah
**Desain dan Pemrograman Berorientasi Objek** serta **Rekayasa Perangkat Lunak**.

---

🎱 *Selamat bermain dan selamat belajar OOP!*
