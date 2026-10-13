# Razza Smart Kalkulator

Aplikasi kalkulator desktop Windows offline dengan antarmuka berbahasa Indonesia. Implementasi memakai Tkinter dari standard library agar ringan dan dapat dijalankan tanpa dependensi tambahan. Mesin hitung memakai `Decimal` dan parser AST dengan whitelist; ekspresi pengguna tidak dijalankan dengan `eval()`.

## Menjalankan dari source

- Python 3.11+ direkomendasikan (kode saat ini juga kompatibel dengan Python 3.8).
- Tidak ada dependensi runtime tambahan.

```powershell
python main.py
```

Data lokal dibuat di folder `data/` di samping source atau executable. Jika lokasi portable tidak bisa ditulis, aplikasi menggunakan `%APPDATA%\RazzaSmartKalkulator`.

## Fitur

- Ekspresi langsung, pratinjau, prioritas operasi, kurung, persen pintar, memori, dan riwayat lokal.
- Kalkulator ilmiah (DEG/RAD), konverter delapan kategori, serta kalkulator diskon dan PPN.
- Tema gelap/terang, format angka Indonesia/internasional, presisi hasil, always-on-top, dan geometri jendela tersimpan.
- Pintasan: Enter hitung, Esc hapus, Delete hapus entri, Ctrl+C salin, Ctrl+V tempel, Ctrl+H riwayat, Ctrl+T tema, Ctrl+1–4 pindah tab, Ctrl+Shift+T always-on-top.

## Tes

```powershell
python -m unittest discover -s tests -v
```

## Membuat executable portable Windows

Build pada Windows 64-bit dengan Python 3.11+:

```powershell
python -m pip install pyinstaller==6.14.2
pyinstaller --noconfirm --onefile --windowed --name RazzaSmartKalkulator main.py
```

Executable ada di `dist\RazzaSmartKalkulator.exe`. Build diuji pada Windows 10 64-bit. Jalankan di PC Windows untuk pemeriksaan akhir.
