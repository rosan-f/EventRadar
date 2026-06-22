# EventRadar

EventRadar adalah tools CLI berbasis Python untuk mengambil, menggabungkan, memfilter, dan mencari informasi event dari beberapa website.

Project ini dibuat sebagai penerapan **Design Pattern** pada aplikasi Python sederhana, khususnya:

* Strategy Pattern
* Factory Pattern

EventRadar berjalan langsung melalui terminal dan tidak menggunakan web interface maupun database.

---

## Fitur

* Mengambil data event dari beberapa sumber
* Menampilkan event melalui terminal
* Memilih sumber event
* Menggabungkan seluruh sumber
* Filter berdasarkan kategori
* Pencarian berdasarkan judul event
* Menampilkan judul, kategori, tanggal, sumber, dan URL
* Validasi argument CLI
* Penanganan error ketika website tidak dapat diakses

---

## Sumber Event

EventRadar saat ini mendukung:

| Source     | Keterangan                                                  |
| ---------- | ----------------------------------------------------------- |
| `pnl`      | Berita dan event dari website Politeknik Negeri Lhokseumawe |
| `dicoding` | Event teknologi dari Dicoding                               |
| `all`      | Mengambil event dari seluruh sumber                         |

---

## Kategori Event

Kategori yang tersedia:

* `seminar`
* `workshop`
* `lomba`
* `webinar`
* `all`

Kategori event ditentukan berdasarkan kata kunci yang ditemukan pada judul atau informasi event.

---

## Teknologi

* Python 3.12
* Conda
* Requests
* Beautiful Soup 4
* Argparse
* Dataclasses

---

## Design Pattern

### Strategy Pattern

Strategy Pattern digunakan untuk memisahkan proses scraping setiap website.

Setiap website memiliki struktur HTML yang berbeda, sehingga masing-masing sumber mempunyai class scraper sendiri.

Contoh:

```text
PNLScraper
DicodingScraper
```

Semua scraper mengikuti interface yang sama:

```python
class EventScraper:
    def scrape(self) -> list[Event]:
        ...
```

Dengan struktur ini, aplikasi dapat menjalankan scraper melalui method yang sama tanpa mengetahui detail implementasi setiap website.

### Factory Pattern

Factory Pattern digunakan untuk membuat object scraper berdasarkan sumber yang dipilih pengguna.

Contoh:

```python
scraper = ScraperFactory.create("pnl")
events = scraper.scrape()
```

Class utama tidak perlu membuat object seperti `PNLScraper` atau `DicodingScraper` secara langsung.

Factory juga dapat membuat seluruh scraper:

```python
scrapers = ScraperFactory.create_all()
```

---

## Struktur Project

```text
event-radar/
├── event_radar/
│   ├── __init__.py
│   ├── models.py
│   ├── formatter.py
│   │
│   └── scrapers/
│       ├── __init__.py
│       ├── base.py
│       ├── factory.py
│       ├── pnl_scraper.py
│       └── dicoding_scraper.py
│
├── .gitignore
├── environment.yml
├── main.py
└── README.md
```

### Penjelasan File

| File                  | Fungsi                                   |
| --------------------- | ---------------------------------------- |
| `main.py`             | Entry point dan konfigurasi argument CLI |
| `models.py`           | Model data event menggunakan dataclass   |
| `formatter.py`        | Menampilkan event ke terminal            |
| `base.py`             | Abstract class untuk Strategy Pattern    |
| `factory.py`          | Factory untuk membuat scraper            |
| `pnl_scraper.py`      | Scraper website PNL                      |
| `dicoding_scraper.py` | Scraper website Dicoding                 |
| `environment.yml`     | Daftar dependency Conda                  |

---

# Instalasi

## 1. Clone Repository

```powershell
git clone <URL_REPOSITORY_GITHUB>
cd event-radar
```

Ganti `<URL_REPOSITORY_GITHUB>` dengan URL repository EventRadar.

---

## 2. Buat Conda Environment Lokal

Environment dibuat di dalam folder project menggunakan prefix `.venv`.

```powershell
conda env create --prefix .\.venv -f environment.yml
```

Environment tidak dibuat pada daftar environment global dengan nama tertentu, tetapi langsung disimpan di:

```text
event-radar\.venv
```

---

## 3. Aktifkan Environment

```powershell
conda activate .\.venv
```

Setelah aktif, terminal akan menampilkan path environment:

```text
(X:\path\event-radar\.venv)
```

---

## 4. Verifikasi Dependency

```powershell
conda list
```

Pastikan package berikut tersedia:

```text
python
requests
beautifulsoup4
```

---

# Cara Penggunaan

## Menampilkan Bantuan

```powershell
python main.py --help
```

Contoh output:

```text
usage: event-radar [-h]
                   [--source {pnl,dicoding,all}]
                   [--category {seminar,workshop,lomba,webinar,all}]
                   [--search SEARCH]
                   [--version]
```

---

## Menampilkan Semua Event

```powershell
python main.py
```

Secara default, EventRadar menggunakan:

```text
source   : all
category : all
```

Command tersebut sama dengan:

```powershell
python main.py --source all --category all
```

---

## Memilih Sumber PNL

```powershell
python main.py --source pnl
```

---

## Memilih Sumber Dicoding

```powershell
python main.py --source dicoding
```

---

## Mengambil Semua Sumber

```powershell
python main.py --source all
```

---

## Filter Berdasarkan Kategori

### Seminar

```powershell
python main.py --category seminar
```

### Workshop

```powershell
python main.py --category workshop
```

### Lomba

```powershell
python main.py --category lomba
```

### Webinar

```powershell
python main.py --category webinar
```

---

## Menggabungkan Source dan Category

Contoh menampilkan seminar dari website PNL:

```powershell
python main.py --source pnl --category seminar
```

Contoh menampilkan workshop dari Dicoding:

```powershell
python main.py --source dicoding --category workshop
```

---

## Mencari Event

Pencarian dilakukan berdasarkan judul event.

```powershell
python main.py --search python
```

Pencarian tidak membedakan huruf besar dan kecil.

Command berikut tetap dianggap sama:

```powershell
python main.py --search Python
python main.py --search python
python main.py --search PYTHON
```

---

## Menggabungkan Source dan Search

```powershell
python main.py --source pnl --search cybersecurity
```

```powershell
python main.py --source dicoding --search cloud
```

---

## Menggabungkan Source, Category, dan Search

```powershell
python main.py --source all --category workshop --search python
```

Urutan prosesnya adalah:

```text
Ambil event
    ↓
Filter kategori
    ↓
Cari berdasarkan judul
    ↓
Tampilkan hasil
```

---

## Menampilkan Versi

```powershell
python main.py --version
```

Contoh output:

```text
event-radar 0.6.0
```

---

# Contoh Output

```text
=== EventRadar ===
Sumber   : all
Kategori : workshop
Pencarian: python

=== Daftar Event ===

[1] Workshop Python untuk Pemula
    Kategori : Workshop
    Tanggal  : 5 Juli 2026
    Sumber   : DICODING
    Link     : https://example.com/event

Total event: 1
```

Jika tidak ada event yang sesuai:

```text
Tidak ada event yang ditemukan.
```

---

# Daftar Argument

| Argument     | Nilai                                            | Default   | Fungsi                    |
| ------------ | ------------------------------------------------ | --------- | ------------------------- |
| `--source`   | `pnl`, `dicoding`, `all`                         | `all`     | Memilih sumber event      |
| `--category` | `seminar`, `workshop`, `lomba`, `webinar`, `all` | `all`     | Memfilter kategori        |
| `--search`   | Teks bebas                                       | Tidak ada | Mencari berdasarkan judul |
| `--version`  | -                                                | -         | Menampilkan versi         |
| `--help`     | -                                                | -         | Menampilkan bantuan       |

---

# Menambahkan Sumber Baru

Buat scraper baru di folder:

```text
event_radar/scrapers/
```

Contoh:

```python
from event_radar.models import Event
from event_radar.scrapers.base import EventScraper


class NewSourceScraper(EventScraper):
    def scrape(self) -> list[Event]:
        return []
```

Kemudian daftarkan scraper pada `ScraperFactory`:

```python
from event_radar.scrapers.new_source_scraper import NewSourceScraper


class ScraperFactory:
    _scrapers = {
        "pnl": PNLScraper,
        "dicoding": DicodingScraper,
        "new-source": NewSourceScraper,
    }
```

Tambahkan juga sumber baru pada argument `--source` di `main.py`.

```python
choices=["pnl", "dicoding", "new-source", "all"]
```

---

# Menjalankan Setelah Clone

Setelah repository di-clone pada komputer lain:

```powershell
cd event-radar
conda env create --prefix .\.venv -f environment.yml
conda activate .\.venv
python main.py --help
```

---

# Memperbarui Environment

Setelah memasang dependency baru melalui Conda:

```powershell
conda install nama-package
```

Export kembali konfigurasi environment:

```powershell
conda env export --from-history |
    Where-Object { $_ -notmatch '^prefix:' } |
    Set-Content -Encoding utf8 environment.yml
```

Pastikan bagian `name` pada `environment.yml` tetap menggunakan:

```yaml
name: event-radar
```

---

# Troubleshooting

## `ModuleNotFoundError`

Pastikan command dijalankan dari root project:

```powershell
Get-Location
```

Posisi terminal harus berada pada folder:

```text
event-radar
```

Kemudian jalankan:

```powershell
python main.py
```

---

## Conda Environment Tidak Aktif

Aktifkan kembali:

```powershell
conda activate .\.venv
```

Cek lokasi Python:

```powershell
Get-Command python
```

Path Python harus mengarah ke folder:

```text
event-radar\.venv
```

---

## Website Tidak Bisa Diakses

EventRadar membutuhkan koneksi internet.

Jika website sumber sedang down, mengubah struktur HTML, atau menolak request, aplikasi dapat menampilkan pesan seperti:

```text
Gagal mengambil data dari PNL
```

Coba periksa:

* koneksi internet
* URL sumber
* status website
* struktur HTML website
* selector pada scraper

---

## Hasil Event Kosong

Hasil kosong dapat terjadi karena:

* tidak ada event yang cocok dengan kategori
* kata pencarian tidak ditemukan
* website mengubah struktur HTML
* selector scraper tidak lagi sesuai
* judul event tidak mengandung kata kunci kategori

Coba jalankan tanpa filter:

```powershell
python main.py --source all
```

---

# Keterbatasan

* EventRadar hanya membaca data publik.
* Data bergantung pada struktur HTML website sumber.
* Perubahan HTML dapat menyebabkan scraper tidak bekerja.
* Kategori ditentukan menggunakan pencocokan kata kunci sederhana.
* Tidak semua berita pada website sumber dianggap sebagai event.
* EventRadar tidak menyimpan data secara permanen.
* EventRadar tidak melakukan scraping terhadap halaman yang membutuhkan login.

---

# Penggunaan yang Bertanggung Jawab

Gunakan EventRadar secara wajar dan hanya untuk data publik.

Hindari:

* mengirim request berlebihan
* mengambil data pribadi
* melewati autentikasi
* mengakses halaman yang dilarang
* menggunakan data untuk spam

EventRadar dibuat untuk kebutuhan pembelajaran dan tugas penerapan Design Pattern.

---

# Status Project

Fitur utama yang telah selesai:

* [x] CLI Python
* [x] Strategy Pattern
* [x] Factory Pattern
* [x] Scraper PNL
* [x] Scraper Dicoding
* [x] Filter sumber
* [x] Filter kategori
* [x] Search berdasarkan judul
* [x] Formatter terminal
* [x] Error handling
* [x] Conda environment

---

# Pengembangan Selanjutnya

Beberapa fitur yang dapat ditambahkan:

* sorting berdasarkan tanggal
* pembatasan jumlah output
* output dalam format JSON
* output dalam format CSV
* sumber event tambahan
* unit testing
* logging
* warna output terminal
* caching sederhana
