# PRD — Razza Smart Kalkulator

| Item | Detail |
|---|---|
| **Nama Produk** | Razza Smart Kalkulator |
| **Platform** | Windows 10/11 (64-bit), aplikasi desktop |
| **Bahasa Pemrograman** | Python 3.11+ |
| **Distribusi** | File `.exe` portabel (tanpa instalasi) |
| **Versi Dokumen** | 1.0 |
| **Status** | Draft |

---

## 1. Ringkasan Produk

**Razza Smart Kalkulator** adalah aplikasi kalkulator desktop untuk Windows dengan tampilan minimalis, modern, dan responsif. Selain operasi hitung biasa, aplikasi ini punya fitur "pintar": input ekspresi langsung dengan pratinjau hasil real-time, riwayat perhitungan yang bisa dipakai ulang, mode ilmiah, konverter satuan, dan kalkulator persen/diskon.

Aplikasi dikemas menjadi **satu file `.exe` portabel**. Pengguna cukup mengunduh dan menjalankannya, tanpa instalasi, tanpa Python terpasang, dan tanpa hak administrator.

### 1.1 Latar Belakang & Tujuan
- Kalkulator bawaan Windows terasa berat dan penuh fitur yang jarang dipakai.
- Pengguna ingin alat hitung yang cepat, bersih, dan bisa dibawa lewat flashdisk.
- Proyek ini juga berfungsi sebagai **proyek belajar** pengembangan aplikasi desktop Python end-to-end: desain UI, logika, penyimpanan data, hingga packaging.

### 1.2 Tujuan Utama
1. Kalkulator yang **cepat dibuka** (< 3 detik) dan ringan.
2. UI **minimalis namun menarik**, nyaman di mode terang dan gelap.
3. Tata letak **responsif** terhadap perubahan ukuran jendela.
4. **Portabel**: satu `.exe`, data pengaturan disimpan di samping file.
5. Hasil hitung **akurat** (tidak ada galat seperti `0.1 + 0.2 = 0.30000000000000004`).

### 1.3 Di Luar Cakupan (Non-Goals) v1.0
- Versi macOS/Linux, mobile, atau web.
- Grafik fungsi (graphing) dan CAS/aljabar simbolik.
- Sinkronisasi cloud dan akun pengguna.
- Kurs mata uang *real-time* (butuh internet; dipertimbangkan di v1.2).

---

## 2. Target Pengguna

| Persona | Kebutuhan |
|---|---|
| **Pelajar/Mahasiswa** | Hitung cepat, fungsi ilmiah (sin, cos, log), riwayat untuk memeriksa langkah |
| **Pekerja Kantoran/UMKM** | Persen, diskon, PPN, margin; salin hasil ke Excel/Word |
| **Pengguna Umum** | Kalkulator sederhana yang bersih dan tidak ribet |
| **Pengguna Portabel** | Bawa aplikasi lewat flashdisk, jalan di PC mana pun |

---

## 3. Fitur & Kebutuhan Fungsional

Prioritas: **P0** = wajib (MVP), **P1** = penting, **P2** = opsional.

### 3.1 Mode Standar (P0)
| ID | Kebutuhan |
|---|---|
| F-01 | Operasi `+ − × ÷`, persen `%`, tanda `±`, `C` (hapus semua), `CE` (hapus entri), `⌫` (backspace) |
| F-02 | Dukungan tanda kurung `( )` dan operasi berantai |
| F-03 | Aritmetika desimal presisi tinggi (modul `decimal`) |
| F-04 | Penanganan galat ramah: pembagian nol → pesan "Tidak bisa dibagi nol", bukan *crash* |
| F-05 | Pemisah ribuan otomatis (contoh `1.234.567,89` sesuai format Indonesia; bisa diganti) |
| F-06 | Memori: `MC`, `MR`, `M+`, `M−` |

### 3.2 Fitur Pintar (P0/P1)
| ID | Prioritas | Kebutuhan |
|---|---|---|
| S-01 | P0 | **Input ekspresi langsung**: ketik `12+3*4` lalu Enter. Mendukung keyboard penuh |
| S-02 | P0 | **Pratinjau hasil real-time** di bawah input sebelum menekan `=` |
| S-03 | P0 | **Riwayat perhitungan**: klik entri untuk memakai ulang ekspresi/hasil; hapus satu/semua |
| S-04 | P1 | **Kalkulator persen pintar**: `200 + 10%` = 220, `50 − 20%` = 40, `15% dari 300` = 45 |
| S-05 | P1 | **Mode Diskon & PPN**: harga awal, diskon %, PPN % → harga akhir dan penghematan |
| S-06 | P1 | **Salin hasil** satu klik (tombol dan `Ctrl+C`); tempel ekspresi dengan `Ctrl+V` |
| S-07 | P2 | **Variabel `Ans`**: memakai hasil sebelumnya dalam ekspresi baru |
| S-08 | P2 | **Kalkulator tanggal**: selisih dua tanggal, tambah/kurang hari |

### 3.3 Mode Ilmiah (P1)
| ID | Kebutuhan |
|---|---|
| I-01 | `sin cos tan`, `asin acos atan`, dengan pilihan **DEG / RAD** |
| I-02 | `log`, `ln`, `√`, `x²`, `xʸ`, `n!`, `1/x`, `|x|` |
| I-03 | Konstanta `π` dan `e` |
| I-04 | Panel ilmiah dapat **dilipat/dibuka** agar tampilan tetap bersih |

### 3.4 Konverter Satuan (P1)
| ID | Kebutuhan |
|---|---|
| K-01 | Kategori: Panjang, Berat, Suhu, Volume, Luas, Waktu, Kecepatan, Data (B/KB/MB/GB) |
| K-02 | Dua kolom (dari ↔ ke) dengan konversi langsung saat mengetik, tombol tukar |
| K-03 | Semua data konversi tersimpan lokal (offline) |

### 3.5 Pengaturan (P1)
| ID | Kebutuhan |
|---|---|
| P-01 | Tema: **Terang / Gelap / Ikuti sistem** |
| P-02 | Format angka: Indonesia (`1.234,56`) atau Internasional (`1,234.56`) |
| P-03 | Jumlah angka desimal maksimum (2–12 atau otomatis) |
| P-04 | Opsi **Selalu di atas** (*always on top*) |
| P-05 | Ukuran & posisi jendela terakhir diingat |
| P-06 | Tombol "Hapus semua data" (riwayat + pengaturan) |

---

## 4. Kebutuhan Non-Fungsional

| Aspek | Target |
|---|---|
| **Performa** | Startup < 3 dtk (pertama kali boleh lebih lama karena ekstraksi `onefile`); respons input < 50 ms |
| **Ukuran file** | Target `.exe` < 40 MB |
| **Akurasi** | Aritmetika desimal; hasil ditampilkan tanpa galat floating-point |
| **Keamanan** | Ekspresi **tidak boleh** dievaluasi dengan `eval()`; gunakan parser aman (`ast` dengan *whitelist* operator/fungsi) |
| **Privasi** | Tanpa telemetri, tanpa koneksi internet, semua data lokal |
| **Portabilitas** | Tidak menulis ke registry; tidak butuh admin; data di folder `data/` di samping `.exe` |
| **Stabilitas** | Tidak ada *crash* akibat input tidak valid; semua galat ditangkap dan ditampilkan ramah |
| **Kompatibilitas** | Windows 10 (1809+) dan Windows 11, 64-bit; mendukung DPI scaling 100–200% |
| **Aksesibilitas** | Kontras warna WCAG AA, dukungan penuh keyboard, urutan *Tab* logis |

---

## 5. Desain UI/UX

### 5.1 Prinsip Desain
1. **Minimalis**: hanya tampilkan yang dibutuhkan; fitur lanjutan disembunyikan rapi.
2. **Fokus pada angka**: layar hasil besar, kontras tinggi, tombol tidak mengganggu.
3. **Konsisten**: satu sistem warna, radius, dan jarak di seluruh aplikasi.
4. **Responsif & lembut**: transisi singkat (120–180 ms) pada hover, klik, dan pergantian tema.

### 5.2 Palet Warna

**Tema Gelap (default)**
| Token | Warna | Penggunaan |
|---|---|---|
| `bg` | `#0F1115` | Latar jendela |
| `surface` | `#181B22` | Panel tampilan & riwayat |
| `key` | `#222631` | Tombol angka |
| `key-op` | `#2E3445` | Tombol operator |
| `accent` | `#7C5CFF` | Tombol `=`, fokus, aksen |
| `text` | `#F2F4F8` | Teks utama |
| `text-muted` | `#8A93A6` | Ekspresi, label, pratinjau |
| `danger` | `#FF5C6C` | Pesan galat, tombol `C` |

**Tema Terang**
| Token | Warna |
|---|---|
| `bg` | `#F5F6FA` |
| `surface` | `#FFFFFF` |
| `key` | `#ECEEF4` |
| `key-op` | `#DDE1EC` |
| `accent` | `#6A48F5` |
| `text` | `#12141A` |
| `text-muted` | `#6B7385` |
| `danger` | `#E5384C` |

### 5.3 Tipografi
- Font utama: **Segoe UI Variable** (bawaan Windows), cadangan `Segoe UI`.
- Hasil: 40 pt (menyusut otomatis jika angka panjang, minimum 20 pt).
- Ekspresi/pratinjau: 14–16 pt, warna `text-muted`.
- Tombol: 16 pt (angka), 14 pt (fungsi ilmiah).

### 5.4 Tata Letak Dasar
```
┌─────────────────────────────────────────────┐
│ ☰  Razza Smart Kalkulator        ◐  ⚙   ─ ▢ ✕│  ← bilah judul
├─────────────────────────────────────────────┤
│ Standar | Ilmiah | Konverter | Diskon       │  ← tab mode
├─────────────────────────────────────────────┤
│                          12 + 3 × 4         │  ← ekspresi (muted)
│                                        24   │  ← hasil (besar)
│                              ≈ pratinjau    │
├─────────────────────────────────────────────┤
│  MC   MR   M+   M−                          │
│  C    ( )   %    ÷                          │
│  7     8    9    ×                          │
│  4     5    6    −                          │
│  1     2    3    +                          │
│  ±     0    ,    =                          │
└─────────────────────────────────────────────┘
```

### 5.5 Perilaku Responsif (Breakpoint)

| Lebar Jendela | Layout |
|---|---|
| **Compact** < 380 px | Satu kolom; keypad penuh; riwayat lewat tombol/laci geser |
| **Normal** 380–720 px | Satu kolom; panel ilmiah dapat dilipat di atas keypad |
| **Wide** > 720 px | Dua kolom: keypad di kiri, **panel riwayat permanen** di kanan; ilmiah tampil berdampingan |

Aturan tambahan:
- Ukuran minimum jendela: **320 × 480 px**.
- Tombol memakai grid yang melebar proporsional (`grid` dengan bobot sama), ukuran font ikut menyesuaikan.
- Mendukung DPI scaling Windows tanpa tampilan buram.

### 5.6 Interaksi & Mikro-Animasi
- **Hover**: tombol sedikit terang; **klik**: efek tekan (skala ~0.97).
- Hasil muncul dengan *fade* singkat; pesan galat bergetar halus.
- Pergantian tema: transisi warna halus, bukan berkedip.
- Salin hasil menampilkan *toast* kecil "Tersalin ✓" selama 1,5 detik.

### 5.7 Pintasan Keyboard
| Pintasan | Aksi |
|---|---|
| `0–9`, `+ − * /`, `( )`, `,` `.` | Input |
| `Enter` / `=` | Hitung |
| `Backspace` | Hapus karakter terakhir |
| `Esc` | Hapus semua (`C`) |
| `Del` | Hapus entri (`CE`) |
| `Ctrl+C` / `Ctrl+V` | Salin hasil / tempel ekspresi |
| `Ctrl+H` | Tampil/sembunyikan riwayat |
| `Ctrl+T` | Ganti tema |
| `Ctrl+1…4` | Pindah mode |
| `Ctrl+Shift+T` | Selalu di atas |

### 5.8 Status & Penanganan Galat
| Situasi | Perilaku |
|---|---|
| Ekspresi belum lengkap (`12+`) | Pratinjau kosong, tidak ada galat |
| Bagi nol | "Tidak bisa dibagi nol" warna `danger` |
| Input tak valid | "Ekspresi tidak valid", kursor ke posisi masalah |
| Angka terlalu besar | Otomatis ke notasi ilmiah (`1,2e+45`) |

---

## 6. Arsitektur Teknis

### 6.1 Stack yang Direkomendasikan
| Komponen | Pilihan | Alasan |
|---|---|---|
| Bahasa | Python 3.11+ | Sesuai kebutuhan, mudah dipelajari |
| GUI | **CustomTkinter** | Tampilan modern, tema terang/gelap bawaan, ringan, mudah untuk pemula |
| Aritmetika | `decimal` + `math` | Presisi desimal |
| Parser ekspresi | `ast` (whitelist) atau tokenizer + *shunting-yard* buatan sendiri | Aman, tanpa `eval()` |
| Penyimpanan | JSON (`settings.json`, `history.json`) | Sederhana, mudah dibaca |
| Packaging | **PyInstaller** (`--onefile --windowed`) | Menghasilkan satu `.exe` portabel |
| Pengujian | `pytest` | Uji mesin kalkulasi |

> **Alternatif:** PySide6 (Qt) menghasilkan UI lebih kaya dan animasi lebih halus, tetapi ukuran `.exe` jauh lebih besar (80 MB+) dan kurva belajar lebih curam. Untuk proyek belajar, CustomTkinter lebih tepat.

### 6.2 Struktur Proyek
```
razza-smart-kalkulator/
├── main.py                  # titik masuk aplikasi
├── requirements.txt
├── razza.spec               # konfigurasi PyInstaller (opsional)
├── assets/
│   ├── icon.ico
│   └── fonts/               # jika memakai font tambahan
├── app/
│   ├── __init__.py
│   ├── core/
│   │   ├── engine.py        # evaluasi ekspresi aman
│   │   ├── parser.py        # tokenizer & validasi
│   │   ├── formatter.py     # format angka (ID/Intl)
│   │   ├── units.py         # data & logika konversi
│   │   └── finance.py       # diskon, PPN, persen
│   ├── data/
│   │   ├── storage.py       # baca/tulis JSON, deteksi folder portabel
│   │   └── history.py
│   ├── ui/
│   │   ├── theme.py         # token warna & font
│   │   ├── main_window.py
│   │   ├── keypad.py
│   │   ├── display.py
│   │   ├── history_panel.py
│   │   ├── scientific_panel.py
│   │   ├── converter_view.py
│   │   ├── discount_view.py
│   │   └── settings_view.py
│   └── utils/
│       └── paths.py         # resolusi path (dev vs. .exe)
└── tests/
    ├── test_engine.py
    ├── test_formatter.py
    └── test_units.py
```

### 6.3 Prinsip Arsitektur
- **Pisahkan logika dari UI**: `core/` tidak boleh meng-*import* apa pun dari `ui/`, agar mudah diuji.
- **Satu sumber kebenaran tema** di `theme.py`; semua widget mengambil warna dari sana.
- **Resolusi path** aman untuk mode `.exe`: gunakan `sys.frozen` / `sys._MEIPASS` untuk aset, dan folder di samping `.exe` untuk data pengguna.

### 6.4 Penyimpanan Data Portabel
```
RazzaSmartKalkulator.exe
data/
├── settings.json
└── history.json
```
- Saat pertama dijalankan, folder `data/` dibuat otomatis di samping `.exe`.
- Jika folder tidak bisa ditulis (mis. disk baca-saja), fallback ke `%APPDATA%/RazzaSmartKalkulator/` dan beri tahu pengguna.
- Riwayat dibatasi **500 entri** terbaru.

Contoh `settings.json`:
```json
{
  "theme": "dark",
  "number_format": "id",
  "max_decimals": 10,
  "angle_unit": "deg",
  "always_on_top": false,
  "window": { "width": 420, "height": 640, "x": 200, "y": 120 }
}
```

### 6.5 Mesin Kalkulasi (Alur)
1. **Tokenisasi** → ubah teks menjadi token (angka, operator, fungsi, kurung).
2. **Normalisasi** → `×`→`*`, `÷`→`/`, koma desimal→titik, aturan persen pintar.
3. **Parsing** → pohon `ast` / *shunting-yard* dengan *whitelist*.
4. **Evaluasi** → `Decimal` untuk aritmetika dasar; `math` untuk fungsi ilmiah (dikonversi ke `Decimal` dengan presisi terkontrol).
5. **Pemformatan** → bulatkan, beri pemisah ribuan, notasi ilmiah jika perlu.

---

## 7. Packaging & Distribusi Portabel

### 7.1 Perintah Build
```bash
pip install customtkinter pyinstaller

pyinstaller --noconfirm --onefile --windowed ^
  --name "RazzaSmartKalkulator" ^
  --icon "assets/icon.ico" ^
  --add-data "assets;assets" ^
  --collect-all customtkinter ^
  main.py
```
Hasil: `dist/RazzaSmartKalkulator.exe`.

### 7.2 Catatan Penting
- `--onefile` mengekstrak ke folder sementara saat dijalankan, jadi **jangan menyimpan data pengguna di sana**; selalu gunakan folder `data/` di samping `.exe`.
- `--collect-all customtkinter` diperlukan agar tema dan aset CustomTkinter ikut terbawa.
- Build di Windows 64-bit, dalam *virtual environment* bersih agar ukuran file kecil.
- Antivirus kadang memberi **false positive** pada `.exe` buatan PyInstaller. Mitigasi: gunakan *virtual environment* bersih, hindari UPX, dan (opsional) tanda tangani digital file.
- Alternatif jika startup `--onefile` terasa lambat: `--onedir` lalu kompres folder menjadi `.zip` portabel.

---

## 8. Kriteria Penerimaan (MVP v1.0)

| # | Kriteria | Cara Uji |
|---|---|---|
| 1 | `0,1 + 0,2` menghasilkan `0,3` | Uji unit |
| 2 | `12+3*4` → `24`; pratinjau muncul saat mengetik | Uji manual |
| 3 | `200 + 10%` → `220`; `50 − 20%` → `40` | Uji unit |
| 4 | `5 ÷ 0` menampilkan pesan galat, aplikasi tidak *crash* | Uji manual |
| 5 | Riwayat tersimpan setelah aplikasi ditutup dan dibuka lagi | Uji manual |
| 6 | Tema, ukuran, dan posisi jendela tersimpan | Uji manual |
| 7 | UI beradaptasi pada 3 breakpoint tanpa elemen terpotong | Uji manual |
| 8 | `.exe` berjalan di Windows 10/11 tanpa Python terpasang | Uji di PC bersih/VM |
| 9 | Semua pintasan keyboard di §5.7 berfungsi | Uji manual |
| 10 | Ekspresi berbahaya (`__import__('os')`) ditolak | Uji unit |
| 11 | Seluruh `tests/` lolos dengan `pytest` | CI/lokal |

---

## 9. Rencana Rilis (Roadmap)

| Fase | Cakupan | Estimasi* |
|---|---|---|
| **M0 — Fondasi** | Struktur proyek, tema, jendela utama, mesin kalkulasi + unit test | 1 minggu |
| **M1 — MVP (v1.0)** | Mode standar, input ekspresi, pratinjau, riwayat, memori, pengaturan dasar, packaging `.exe` | 2–3 minggu |
| **M2 — v1.1** | Mode ilmiah, konverter satuan, persen pintar, diskon & PPN | 2 minggu |
| **M3 — v1.2** | Kalkulator tanggal, variabel `Ans`, ekspor riwayat (CSV), kurs mata uang (opsional, online) | 2 minggu |
| **M4 — Polesan** | Animasi, aksesibilitas, optimasi ukuran/kecepatan, ikon & splash | 1 minggu |

\*Estimasi untuk pengembang tunggal yang sambil belajar; sesuaikan dengan kecepatan Anda.

---

## 10. Risiko & Mitigasi

| Risiko | Dampak | Mitigasi |
|---|---|---|
| Ukuran/kecepatan startup `.exe` | Pengalaman pengguna buruk | Venv bersih, hindari library berat, pertimbangkan `--onedir` |
| *False positive* antivirus | Pengguna ragu menjalankan | Hindari UPX, tanda tangan digital, sediakan hash SHA-256 |
| Layout pecah di DPI tinggi | Tampilan tidak rapi | Uji di 100/125/150/200%, gunakan grid proporsional |
| Galat presisi desimal | Hasil salah | `Decimal` + uji unit ekstensif |
| Celah keamanan evaluasi ekspresi | Eksekusi kode berbahaya | Larang `eval()`, gunakan parser *whitelist* |
| Cakupan fitur melebar | Proyek tak selesai | Disiplin prioritas P0 → P1 → P2 |

---

## 11. Metrik Keberhasilan
- Startup ≤ 3 detik pada PC standar.
- Nol *crash* pada 200 skenario uji input acak.
- Cakupan unit test mesin kalkulasi ≥ 90%.
- Ukuran `.exe` < 40 MB.
- Pengguna uji dapat menyelesaikan 5 tugas inti (hitung, persen, riwayat, ganti tema, konversi satuan) tanpa panduan.

---

## 12. Pertanyaan Terbuka
1. Apakah ingin menambahkan mode **Programmer** (biner/heksa/oktal) di rilis berikutnya?
2. Apakah kurs mata uang online diperlukan, mengingat prinsip "100% offline"?
3. Apakah aplikasi akan didistribusikan publik (perlu tanda tangan digital & halaman unduhan)?
4. Apakah perlu dukungan bahasa antarmuka selain Indonesia (mis. Inggris)?

---

## 13. Lampiran: Titik Awal Kode (Kerangka)

`main.py`
```python
import customtkinter as ctk
from app.ui.main_window import MainWindow

def main():
    ctk.set_appearance_mode("dark")      # "light" | "dark" | "system"
    ctk.set_default_color_theme("dark-blue")
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    main()
```

`app/utils/paths.py`
```python
import sys
from pathlib import Path

def resource_path(rel: str) -> Path:
    """Path aset (ikon, font) — bekerja saat dev dan saat .exe."""
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[2]))
    return base / rel

def data_dir() -> Path:
    """Folder data pengguna di samping .exe (portabel)."""
    if getattr(sys, "frozen", False):
        base = Path(sys.executable).parent
    else:
        base = Path(__file__).resolve().parents[2]
    d = base / "data"
    d.mkdir(exist_ok=True)
    return d
```

`app/core/engine.py` (inti evaluator aman, ringkas)
```python
import ast
import operator as op
from decimal import Decimal, getcontext

getcontext().prec = 28

_BIN = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
        ast.Div: op.truediv, ast.Pow: op.pow, ast.Mod: op.mod}
_UNARY = {ast.UAdd: op.pos, ast.USub: op.neg}

def evaluate(expr: str) -> Decimal:
    expr = expr.replace("×", "*").replace("÷", "/").replace(",", ".")
    tree = ast.parse(expr, mode="eval")
    return _eval(tree.body)

def _eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return Decimal(str(node.value))
    if isinstance(node, ast.BinOp) and type(node.op) in _BIN:
        return _BIN[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY:
        return _UNARY[type(node.op)](_eval(node.operand))
    raise ValueError("Ekspresi tidak valid")
```

---

*Dokumen ini adalah titik awal. Perbarui seiring perkembangan proyek dan umpan balik pengguna.*
