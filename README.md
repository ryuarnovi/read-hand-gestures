# Hand Gesture Recognition — Dokumentasi singkat

Ini adalah dokumentasi singkat yang menjelaskan fungsi aplikasi, cara instalasi, dan cara menjalankan demo pengenalan gestur tangan.

Fungsi aplikasi
---------------
- Mendeteksi tangan pada video stream (webcam) menggunakan MediaPipe.
- Menyajikan koordinat dan landmark tangan, menggambar koneksi jari, dan menampilkan nama gestur sederhana (Peace, Hi Five, Thumbs Up, OK, Mengepal).
- Menampilkan panel informasi (jumlah tangan, gestur terdeteksi) di atas video.

Persyaratan singkat
-------------------
- macOS dengan webcam
- Python 3.11 (direkomendasikan)

Instalasi (singkat)
-------------------
1. Masuk ke folder `gesture`:

```bash
cd '/Users/macbookpro/Documents/Tugas Kuliah/gesture'
```

2. Buat virtual environment (Python 3.11):

```bash
python3.11 -m venv hand_gesture_env
```

3. Aktifkan venv dan instal dependensi:

```bash
source hand_gesture_env/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

Menjalankan aplikasi
--------------------
- Dari root proyek (memanggil launcher):

```bash
cd '/Users/macbookpro/Documents/Tugas Kuliah'
./start_gesture.sh
```

- Atau langsung dari folder `gesture`:

```bash
cd '/Users/macbookpro/Documents/Tugas Kuliah/gesture'
./run_gesture.sh
```

- Manual (aktifkan venv lalu jalankan):

```bash
source hand_gesture_env/bin/activate
python index.py
```

Troubleshooting singkat
----------------------
- `ModuleNotFoundError: No module named 'cv2'` — pastikan menjalankan Python dari `hand_gesture_env` (aktifkan venv atau jalankan venv Python langsung).
- `OpenCV: not authorized to capture video` atau "Gagal membaca dari kamera" — beri izin kamera:
  - System Settings → Privacy & Security → Camera → aktifkan Terminal / iTerm / VS Code.
  - Tutup dan buka kembali aplikasi terminal setelah mengubah izin.

Menghapus venv dari git (jika ter-track)
--------------------------------------
Jika `gesture/hand_gesture_env` sudah ter-track di repo, hapus dari index tanpa menghapus file lokal:

```bash
git rm -r --cached gesture/hand_gesture_env
echo "gesture/hand_gesture_env/" >> .gitignore
git add .gitignore
git commit -m "Remove hand_gesture_env from repo and add to .gitignore"
```

Jika butuh saya commit file README ini ke repo, konfirmasi saja dan saya akan men-stage & commit.

---
Ini README ringkas sesuai permintaan: hanya fungsi aplikasi, instalasi, dan cara menjalankan.
