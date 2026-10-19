# Pemodelan Spasial Jasa Lingkungan Hidup (JLH) Sumatera Barat
**Direktorat Penyelenggaraan Sumber Daya Alam Berkelanjutan — Kementerian Lingkungan Hidup / BPLH**

Repositori ini memuat skrip pemrosesan geospasial (Python & GDAL), tabel acuan skor dan bobot (`KBA`, `KVA`, `PL`, `JLH Tinggi`), simbologi QGIS (`.qml`), serta dokumentasi teknis perhitungan 6 Indikator Jasa Lingkungan Hidup (JLH) Provinsi Sumatera Barat pada resolusi spasial 0.5 meter (`EPSG:3857`).

---

## Struktur Direktori

```text
.
├── README.md                                  # Dokumentasi utama dan alur pemrosesan
├── requirements.txt                           # Dependensi pustaka Python
├── .gitignore                                 # Pengecualian file raster/vektor berukuran besar
│
├── config_skor/                               # Tabel skor, bobot, dan simbologi QGIS
│   ├── README_TABEL_SKOR.md                   # Tabel referensi lengkap (KBA, KVA, PL, Bobot, JLH Tinggi)
│   ├── Skor_JLH_2026.xlsx                     # File Excel acuan skor KBA dan KVA
│   ├── bobot_indikator_sumatera.csv           # Bobot W_KBA, W_KVA, W_PL untuk 6 indikator JLH
│   ├── skor_penutupan_lahan.csv               # Skor 15 kelas Penutupan Lahan (0.5m)
│   ├── skor_kba.csv                           # Skor 83 kelas Karakteristik Bentang Alam (KBA)
│   ├── skor_kva.csv                           # Skor 94 kelas Karakteristik Vegetasi Alami (KVA)
│   ├── kodefikasi_jlh_tinggi.csv              # Kodefikasi raster UInt8 dan warna kelas JLH Tinggi
│   └── style_qgis/                            # Simbologi layer untuk QGIS (.qml)
│       ├── jlh_symbologi.qml
│       └── sumbar_2025_jlh_tinggi_seamless.qml
│
├── scripts/                                   # Skrip pemrosesan utama
│   ├── 01_preprocessing/                      # Tahap 1: Rasterisasi dan penyiapan input
│   │   ├── generate_kba_kva_grids.py          # Rasterisasi GDB KBA & KVA ke grid 0.5m
│   │   ├── create_seamless_kba_kva.py         # Penggabungan grid KBA & KVA menjadi COG seamless
│   │   └── rasterize_kalbar_seamless.py       # Utilitas rasterisasi wilayah Kalimantan Barat
│   │
│   ├── 02_core_calculation/                   # Tahap 2: Kalkulasi indikator JLH dan JLH Tinggi
│   │   ├── calculate_jlh_sumbar_2025.py       # Perhitungan paralel 6 indikator JLH (0.5m)
│   │   ├── apply_kk_phk.py                    # Penyesuaian Kriteria Khusus (Kawasan Konservasi) pada PHK
│   │   └── calculate_jlh_tinggi_sumbar.py     # Pemetaan kelas JLH Tinggi (>= 4.20) berbasis bitwise
│   │
│   └── 03_mosaic_packaging/                   # Tahap 3: Pengemasan mozaik dan kompresi COG
│       ├── create_seamless_jlh_lerc.py        # Konversi VRT ke GeoTIFF seamless (LERC_ZSTD)
│       ├── create_seamless_jlh_batch.py       # Pemrosesan batch seluruh layer JLH menjadi COG
│       └── sync_seamless_jlh.sh               # Pembuatan piramida overview (.ovr)
│
├── docs/                                      # Laporan teknis & metodologi
│   ├── report_jlh_sumatera_barat_2026.docx    # Laporan teknis kajian JLH format Word (template DL4LULC)
│   ├── report_jlh_sumatera_barat_2026.md      # Laporan teknis kajian JLH format Markdown
│   └── Dokumentasi_Metodologi_dan_Skrip_JLH_Sumbar.html
│
└── sample_data/                               # Potongan data sampel input & hasil JLH (0.5m)
    ├── README.md                              # Penjelasan spesifikasi file sampel
    ├── aoi_sample.geojson                     # Poligon batas area sampel (AOI)
    ├── luasan_jlh_tinggi_sumbar.json          # Statistik luasan JLH Tinggi se-Sumatera Barat
    ├── 01_input_komponen/                     # Sampel raster & vektor input (KBA, KVA, PL, KK)
    │   ├── sample_kba_05m.tif
    │   ├── sample_kva_05m.tif
    │   ├── sample_penutupan_lahan_2025_05m.tif
    │   ├── sample_vektor_kba_kva.geojson
    │   └── sample_vektor_kriteria_khusus.geojson
    └── 02_output_jlh/                         # Sampel raster hasil 6 JLH, PHK_KK & JLH Tinggi (+ .qml)
        ├── sample_jlh_pga_05m.tif
        ├── sample_jlh_phk_05m.tif
        ├── sample_jlh_phk_kk_05m.tif
        ├── sample_jlh_ppk_05m.tif
        ├── sample_jlh_pya_05m.tif
        ├── sample_jlh_pgn_05m.tif
        ├── sample_jlh_pku_05m.tif
        └── sample_jlh_tinggi_05m.tif
```

---

## Formulasi, Bobot, dan Tabel Skor

Daftar lengkap **83 kelas KBA** dan **94 kelas KVA** tersedia pada [`config_skor/README_TABEL_SKOR.md`](config_skor/README_TABEL_SKOR.md) serta file CSV di dalam direktori [`config_skor/`](config_skor/).

### 1. Persamaan Perhitungan JLH
$$\text{JLH}_k = \left(\text{Skor KBA}_k \times W_{\text{KBA}, k}\right) + \left(\text{Skor KVA}_k \times W_{\text{KVA}, k}\right) + \left(\text{Skor PL}_k \times W_{\text{PL}, k}\right)$$

### 2. Bobot Komponen Regional Sumatera (`config_skor/bobot_indikator_sumatera.csv`)

| Kode | Indikator Jasa Lingkungan Hidup | $W_{\text{KBA}}$ | $W_{\text{KVA}}$ | $W_{\text{PL}}$ | Total |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **PGA** | Pengaturan Air | 0.28 | 0.12 | 0.60 | 1.00 |
| **PHK** | Pendukung Habitat & Kehati | 0.24 | 0.16 | 0.60 | 1.00 |
| **PPK** | Penyerap & Penyimpan Karbon | 0.20 | 0.20 | 0.60 | 1.00 |
| **PYA** | Penyedia Air | 0.32 | 0.08 | 0.60 | 1.00 |
| **PGN** | Penyedia Pangan (Sumatera) | 0.28 | 0.12 | 0.60 | 1.00 |
| **PKU** | Pengatur Kualitas Udara | 0.15 | 0.25 | 0.60 | 1.00 |

### 3. Skor Penutupan Lahan 0.5m (`config_skor/skor_penutupan_lahan.csv`)

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

### 4. Kodefikasi JLH Tinggi (`config_skor/kodefikasi_jlh_tinggi.csv`)
Menggunakan ambang batas **$\ge 4.20$ (Kelas Sangat Tinggi)** pada 3 indikator (**PGA**, **PHK**, **PPK**) dengan pengodean bitwise `Bitmask = 4*(PGA>=4.2) + 2*(PHK>=4.2) + 1*(PPK>=4.2)`:

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

## Alur Eksekusi Skrip

1. **Tahap 1 — Rasterisasi KBA & KVA ke Grid 0.5m (`scripts/01_preprocessing/`)**
   - `generate_kba_kva_grids.py`: Mengonversi poligon GDB Unit Ekoregion (`UE_Verlap_Sumbar.gdb`) menjadi grid tile 0.5m sesuai kolom `Value` pada `config_skor/Skor_JLH_2026.xlsx`.
   - `create_seamless_kba_kva.py`: Menggabungkan grid tile menjadi raster seamless `sumbar_2025_kba_seamless.tif` dan `sumbar_2025_kva_seamless.tif`.
2. **Tahap 2 — Perhitungan 6 Indikator JLH & JLH Tinggi (`scripts/02_core_calculation/`)**
   - `calculate_jlh_sumbar_2025.py`: Menghitung skor kontinu 6 indikator (`PGA`, `PHK`, `PPK`, `PYA`, `PGN`, `PKU`) secara paralel.
   - `apply_kk_phk.py`: Menerapkan Kriteria Khusus (Kawasan Konservasi = 5.0) pada layer `PHK`.
   - `calculate_jlh_tinggi_sumbar.py`: Menghasilkan peta komposit **JLH Tinggi** (`sumbar_2025_jlh_tinggi_seamless.tif`), rekapitulasi luasan (`luasan_jlh_tinggi.json`), dan simbologi `.qml`.
3. **Tahap 3 — Pengemasan Seamless COG (`scripts/03_mosaic_packaging/`)**
   - `create_seamless_jlh_lerc.py` dan `create_seamless_jlh_batch.py`: Mengemas output menjadi Cloud Optimized GeoTIFF (`LERC_ZSTD`).
