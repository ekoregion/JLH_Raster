# Pemodelan Spasial Jasa Lingkungan Hidup (JLH) Resolusi Ultra-Tinggi (0.5 Meter)
**Studi Kasus: Provinsi Sumatera Barat (Tahun Analisis 2025–2026)**  
**Penyusun:** Direktorat Penyelenggaraan Sumber Daya Alam Berkelanjutan — Kementerian Lingkungan Hidup / BPLH

Repositori ini berisi **seluruh skrip pemodelan geospasial (Python & GDAL)**, **katalog tabel skor & bobot (`KBA`, `KVA`, `PL`, `JLH Tinggi`)**, **simbologi QGIS (`.qml`)**, **Jupyter Notebooks**, serta **dokumentasi metodologi dan laporan** sehingga tidak terpencar dan siap direproduksi kapan saja.

---

## 📂 Struktur Folder Repositori

```text
git_upload/
├── README.md                                  # Dokumentasi utama proyek & panduan alur skrip (halaman ini)
├── requirements.txt                           # Daftar dependensi library Python
├── .gitignore                                 # Konfigurasi pengabaian file raster besar (*.tif, *.gdb, *.gpkg)
│
├── config_skor/                               # 📌 PUSAT TABEL SKOR, BOBOT & SIMBOLOGI QGIS
│   ├── README_TABEL_SKOR.md                   # Katalog lengkap seluruh tabel skor (KBA 83 kelas, KVA 94 kelas, PL, Bobot)
│   ├── Skor_JLH_2026.xlsx                     # Master Excel asli (Sheet 'Skor KBA' & 'Skor KVA')
│   ├── bobot_indikator_sumatera.csv           # Tabel bobot W_KBA, W_KVA, W_PL untuk 6 Indikator JLH
│   ├── skor_penutupan_lahan.csv               # Tabel lookup skor 15 kelas Penutupan Lahan (Multiscale 0.5m)
│   ├── skor_kba.csv                           # Ekstraksi CSV 83 kelas Karakteristik Bentang Alam (KBA)
│   ├── skor_kva.csv                           # Ekstraksi CSV 94 kelas Karakteristik Vegetasi Alami (KVA)
│   ├── kodefikasi_jlh_tinggi.csv              # Skema kode 2-digit UInt8 & warna Diagram Venn JLH Tinggi (A, B1-B3, C1-C3)
│   └── style_qgis/                            # File simbologi siap pakai di QGIS
│       ├── jlh_symbologi.qml                  # Simbologi 5 kelas skor JLH (Sangat Rendah s.d. Sangat Tinggi)
│       └── sumbar_2025_jlh_tinggi_seamless.qml # Simbologi 8 kelas irisan JLH Tinggi (Diagram Venn)
│
├── scripts/                                   # 📌 SKRIP KOMPUTASI PYTHON (Terurut sesuai tahapan pipeline)
│   ├── 01_preprocessing/                      # Tahap 1: Rasterisasi & Penyiapan Data Dasar
│   │   ├── generate_kba_kva_grids.py          # Rasterisasi GDB KBA & KVA ke grid tile 0.5m sesuai Skor_JLH_2026.xlsx
│   │   ├── create_seamless_kba_kva.py         # Penggabungan grid KBA & KVA menjadi 1 file COG Seamless UInt8
│   │   ├── rasterize_kalbar_seamless.py       # Utilitas rasterisasi seamless untuk wilayah Kalimantan Barat
│   │   └── fetch_osm_sumbar.py                # Pengunduhan jaringan jalan & bangunan OpenStreetMap (OSM) Sumbar
│   │
│   ├── 02_core_calculation/                   # Tahap 2: Perhitungan Inti 6 JLH, Koreksi KK, JLH Tinggi & Relokasi
│   │   ├── calculate_jlh_sumbar_2025.py       # Kalkulasi paralel multi-core 6 Indikator JLH (0.5m)
│   │   ├── apply_kk_phk.py                    # Penyesuaian Kriteria Khusus (Kawasan Konservasi = Skor 5.0) pada PHK
│   │   ├── calculate_jlh_tinggi_sumbar.py     # Pemetaan JLH Tinggi (>= 4.20) dengan Aljabar Bitwise 3-Bit (PGA, PHK, PPK)
│   │   └── run_local_10m.py                   # Pemodelan kesesuaian lahan relokasi permukiman (resolusi 10m)
│   │
│   ├── 03_mosaic_packaging/                   # Tahap 3: Pengemasan Cloud Optimized GeoTIFF (COG) LERC_ZSTD
│   │   ├── create_seamless_jlh_lerc.py        # Konversi VRT ke GeoTIFF Seamless terkompresi LERC_ZSTD (presisi 0.01)
│   │   ├── create_seamless_jlh_batch.py       # Pemrosesan batch seluruh layer JLH menjadi seamless COG
│   │   └── sync_seamless_jlh.sh               # Skrip shell sinkronisasi & pembuatan piramida overview (.ovr)
│   │
│   └── 04_reporting_generators/               # Tahap 4: Otomasi Pembuatan Dokumen Word, PPTX & Notebook
│       ├── build_detailed_jlh_docx.py         # Generator dokumen pedoman teknis & metodologi (.docx)
│       ├── build_analisis_mendalam_jlh_pptx.py # Generator paparan analisis mendalam KBA, KVA, PL & JLH (.pptx)
│       ├── build_modern_tabel_jlh.py          # Generator matriks perbandingan visual modern (.pptx)
│       ├── build_presentation_matrix.py       # Generator slide matriks komparasi indikator
│       ├── build_jlh_docx.py                  # Generator dokumen ringkasan JLH (.docx)
│       ├── generate_jlh_documentation.py      # Generator dokumentasi HTML/Markdown
│       ├── generate_pptx.py                   # Generator slide presentasi ringkas
│       ├── generate_notebook.py               # Generator template Jupyter Notebook kalkulasi JLH
│       └── make_notebook_local.py             # Generator Jupyter Notebook kajian kesesuaian relokasi
│
├── notebooks/                                 # 📌 JUPYTER NOTEBOOKS INTERAKTIF
│   ├── Kalkulasi_JLH_Sumbar.ipynb             # Notebook interaktif perhitungan 6 Indikator JLH
│   └── Kajian_Kesesuaian_Relokasi_JLH_Sumbar.ipynb # Notebook analisis multi-kriteria kesesuaian lahan relokasi
│
├── docs/                                      # 📌 DOKUMENTASI TEKNIS & BAHAN PAPARAN
│   ├── Dokumentasi_Metodologi_dan_Skrip_JLH_Sumbar.md   # Pedoman teknis lengkap (Markdown)
│   ├── Dokumentasi_Metodologi_dan_Skrip_JLH_Sumbar.docx # Pedoman teknis lengkap (Microsoft Word)
│   ├── Dokumentasi_Metodologi_dan_Skrip_JLH_Sumbar.html # Pedoman teknis versi Web/HTML
│   ├── Panduan_JLH_Sumbar.md                  # Ringkasan cepat rumus & tabel skor
│   ├── Presentasi_Perhitungan_JLH.md          # Outline materi presentasi
│   └── presentations/                         # Kumpulan file PowerPoint (.pptx) & Dashboard HTML hasil analisis
│
└── data_samples_metadata/                     # 📌 METADATA & STATISTIK LUASAN HASIL (JSON)
    └── luasan_jlh_tinggi.json                 # Rekapitulasi jumlah piksel & luas hektar per kelas JLH Tinggi Sumbar
```

---

## 🧮 Ringkasan Rumus, Bobot, dan Tabel Skor

> 📖 **Ingin melihat tabel lengkap 83 kelas KBA dan 94 kelas KVA?**  
> Buka langsung [**`config_skor/README_TABEL_SKOR.md`**](config_skor/README_TABEL_SKOR.md) atau file CSV di dalam folder [`config_skor/`](config_skor/).

### 1. Persamaan Kombinasi Linear Terbobot
$$\text{JLH}_k = \left(\text{Skor KBA}_k \times W_{\text{KBA}, k}\right) + \left(\text{Skor KVA}_k \times W_{\text{KVA}, k}\right) + \left(\text{Skor PL}_k \times W_{\text{PL}, k}\right)$$

### 2. Bobot Komponen Regional Sumatera (`config_skor/bobot_indikator_sumatera.csv`)

| Kode | Indikator Jasa Lingkungan Hidup | $W_{\text{KBA}}$ | $W_{\text{KVA}}$ | $W_{\text{PL}}$ | Total |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **PGA** | Pengaturan Air (*Water Regulation*) | 0.28 | 0.12 | 0.60 | 1.00 |
| **PHK** | Pendukung Habitat & Kehati (*Biodiversity*) | 0.24 | 0.16 | 0.60 | 1.00 |
| **PPK** | Penyerap & Penyimpan Karbon (*Carbon Storage*) | 0.20 | 0.20 | 0.60 | 1.00 |
| **PYA** | Penyedia Air (*Water Provisioning*) | 0.32 | 0.08 | 0.60 | 1.00 |
| **PGN** | Penyedia Pangan (*Food Provisioning - Sumatera*) | 0.28 | 0.12 | 0.60 | 1.00 |
| **PKU** | Pengatur Kualitas Udara (*Air Quality Regulation*) | 0.15 | 0.25 | 0.60 | 1.00 |

### 3. Matriks Skor Penutupan Lahan 0.5m (`config_skor/skor_penutupan_lahan.csv`)

| Value | Kelas Penutupan Lahan (PL 2025) | PGA | PHK | PPK | PYA | PGN | PKU |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | Water (Badan Air / Danau / Sungai) | 5 | 1 | 1 | 5 | 4 | 5 |
| **2** | Natural Forest (Hutan Hujan Alami) | 5 | 5 | 5 | 3 | 4 | 5 |
| **4** | Flooded Vegetation (Vegetasi Rawa / Mangrove) | 4 | 3 | 3 | 3 | 4 | 5 |
| **5** | Crops (Pertanian Tanaman Pangan / Sawah) | 3 | 1 | 1 | 3 | 4 | 3 |
| **7** | Development Space (Lahan Terbuka Binaan) | 2 | 1 | 1 | 2 | 1 | 2 |
| **8** | Bare Ground (Tanah Terbuka / Tambang) | 1 | 1 | 1 | 1 | 1 | 1 |
| **11** | Rangeland (Padang Rumput / Semak Belukar) | 3 | 2 | 2 | 1 | 2 | 3 |
| **12** | Plantation (Perkebunan Tahunan / Sawit / Karet) | 3 | 2 | 2 | 2 | 3 | 4 |
| **13** | Uncertain Trees (Pepohonan Campuran / Agroforestri) | 3 | 3 | 2 | 2 | 3 | 3 |
| **14** | Road (Jaringan Jalan & Infrastruktur) | 1 | 1 | 1 | 1 | 1 | 1 |
| **15** | Building (Kawasan Terbangun / Permukiman) | 1 | 1 | 1 | 2 | 1 | 1 |

### 4. Skema Kodefikasi JLH Tinggi (`config_skor/kodefikasi_jlh_tinggi.csv`)
Menggunakan ambang batas **$\ge 4.20$ (Kelas Sangat Tinggi)** pada 3 indikator kunci (**PGA**, **PHK**, **PPK**) dengan rumus Bitwise `Bitmask = 4*(PGA>=4.2) + 2*(PHK>=4.2) + 1*(PPK>=4.2)`:

| Kode Raster (`UInt8`) | Bitmask | Kode | Kategori Utama | JLH Penyusun | Warna Hex |
| :---: | :---: | :---: | :--- | :--- | :---: |
| **10** | `7 (111)` | **A** | Kategori A (3 JLH Tinggi) | PGA + PHK + PPK | `#9A7029` |
| **21** | `6 (110)` | **B1** | Kategori B (2 JLH Tinggi) | PGA + PHK | `#63C5DA` |
| **22** | `3 (011)` | **B2** | Kategori B (2 JLH Tinggi) | PHK + PPK | `#F2EA3B` |
| **23** | `5 (101)` | **B3** | Kategori B (2 JLH Tinggi) | PGA + PPK | `#AE529A` |
| **31** | `4 (100)` | **C1** | Kategori C (1 JLH Tinggi) | PGA | `#305496` |
| **32** | `2 (010)` | **C2** | Kategori C (1 JLH Tinggi) | PHK | `#54B948` |
| **33** | `1 (001)` | **C3** | Kategori C (1 JLH Tinggi) | PPK | `#ED1C24` |
| **1** | `0 (000)` | **Non-JLHT** | Di Luar JLH Tinggi (< 4.2) | Tidak Ada (< 4.2) | `#E2E8F0` |

---

## 🚀 Urutan Eksekusi Pipeline Skrip

1. **Tahap 1 — Rasterisasi KBA & KVA ke Grid 0.5m (`scripts/01_preprocessing/`)**
   - Jalankan `generate_kba_kva_grids.py` untuk mengonversi poligon GDB Unit Ekoregion (`UE_Verlap_Sumbar.gdb`) menjadi grid tile 0.5m sesuai kode `Value` di `config_skor/Skor_JLH_2026.xlsx`.
   - Jalankan `create_seamless_kba_kva.py` untuk menyatukan seluruh tile menjadi `sumbar_2025_kba_seamless.tif` dan `sumbar_2025_kva_seamless.tif`.
2. **Tahap 2 — Perhitungan 6 Indikator JLH & JLH Tinggi (`scripts/02_core_calculation/`)**
   - Jalankan `calculate_jlh_sumbar_2025.py` untuk menghitung nilai kontinu 6 indikator (`PGA`, `PHK`, `PPK`, `PYA`, `PGN`, `PKU`) secara paralel.
   - Jalankan `apply_kk_phk.py` untuk menerapkan aturan Kriteria Khusus (Kawasan Konservasi = 5.0) pada indikator `PHK`.
   - Jalankan `calculate_jlh_tinggi_sumbar.py` untuk memetakan irisan **JLH Tinggi** (`sumbar_2025_jlh_tinggi_seamless.tif`) beserta file statistik `luasan_jlh_tinggi.json` dan simbologi `.qml`.
3. **Tahap 3 — Kompresi Seamless COG (`scripts/03_mosaic_packaging/`)**
   - Jalankan `create_seamless_jlh_lerc.py` atau `create_seamless_jlh_batch.py` untuk mengemas hasil perhitungan ke format Cloud Optimized GeoTIFF (`LERC_ZSTD`).
4. **Tahap 4 — Pembuatan Laporan & Paparan Otomatis (`scripts/04_reporting_generators/`)**
   - Jalankan `build_detailed_jlh_docx.py` dan `build_analisis_mendalam_jlh_pptx.py` bila ingin memperbarui dokumen Word atau slide presentasi secara otomatis.

---

## 🌐 Cara Upload Folder Ini ke GitHub

Folder `git_upload` ini sudah diinisialisasi dengan Git dan dilengkapi `.gitignore`. Untuk mengunggah ke repositori GitHub Anda:

```bash
cd git_upload
git branch -M main
git remote add origin https://github.com/ekoregion/JLH_Raster.git
git push -u origin main
```
