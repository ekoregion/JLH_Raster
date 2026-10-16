import os

doc_content = """# DOKUMENTASI LENGKAP METODOLOGI & SKRIP PEMODELAN JASA LINGKUNGAN HIDUP (JLH)
## Provinsi Sumatera Barat (Tahun Analisis: 2025–2026)

**Instansi Penyusun:** Direktorat Penyelenggaraan Sumber Daya Alam Berkelanjutan  
**Kementerian Lingkungan Hidup / Badan Pengendalian Lingkungan Hidup (BPLH)**  
**Resolusi Spasial:** Ultra-Tinggi (0.5 Meter Seamless)  
**Sistem Proyeksi (CRS):** EPSG:3857 (WGS 84 / Pseudo-Mercator)  

---

## DAFTAR ISI
1. [Latar Belakang & Kerangka Konseptual JLH](#1-latar-belakang--kerangka-konseptual-jlh)
2. [Tiga Pilar Komponen Input JLH](#2-tiga-pilar-komponen-input-jlh)
   - [2.1 Karakteristik Bentang Alam (KBA)](#21-karakteristik-bentang-alam-kba)
   - [2.2 Karakteristik Vegetasi Alami (KVA)](#22-karakteristik-vegetasi-alami-kva)
   - [2.3 Penutupan Lahan Multiskala 2025 (PL)](#23-penutupan-lahan-multiskala-2025-pl)
3. [Formulasi Matematis & Bobot 6 Indikator JLH](#3-formulasi-matematis--bobot-6-indikator-jlh)
4. [Tabel Matriks Skor Penutupan Lahan (PL Lookup Table)](#4-tabel-matriks-skor-penutupan-lahan-pl-lookup-table)
5. [Skrip Python: Transformasi & Kalkulasi JLH Grid 0.5m](#5-skrip-python-transformasi--kalkulasi-jlh-grid-05m)
6. [Skrip Python: Mozaik Seamless Se-Sumbar & Kompresi LERC_ZSTD](#6-skrip-python-mozaik-seamless-se-sumbar--kompresi-lerc_zstd)
7. [Penyesuaian Kriteria Khusus (KK.gpkg) pada Layer PHK](#7-penyesuaian-kriteria-khusus-kkgpkg-pada-layer-phk)
8. [Hilirisasi Analisis: JLH Ruang Hidup (Kesesuaian Relokasi Huntap/Huntara)](#8-hilirisasi-analisis-jlh-ruang-hidup-kesesuaian-relokasi-huntaphuntara)

---

## 1. Latar Belakang & Kerangka Konseptual JLH

Jasa Lingkungan Hidup (JLH) atau *Ecosystem Services* merupakan manfaat yang diperoleh manusia dari berfungsinya ekosistem alami dan bentang alam secara lestari. Pemodelan JLH di Provinsi Sumatera Barat disusun untuk menyediakan basis data spasial beresolusi sangat detail (0.5 meter) sebagai instrumen:
1. **Rencana Perlindungan dan Pengelolaan Lingkungan Hidup (RPPLH)**.
2. **Penentuan Daya Dukung dan Daya Tampung Lingkungan Hidup (D3TLH)**.
3. **Mitigasi Bencana & Pemilihan Lokasi Relokasi Masyarakat (Huntap/Huntara)**.

Pemodelan ini mengevaluasi **6 Indikator Layanan Ekosistem**:
1. **PGA** (*Pengaturan Air*): Kemampuan lanskap mengatur siklus hidrologi, retensi air, infiltrasi, dan pencegahan banjir/kekeringan.
2. **PHK** (*Pendukung Habitat & Keanekaragaman Hayati*): Kemampuan lanskap mempertahankan keanekaragaman flora/fauna dan koridor ekologis.
3. **PPK** (*Penyerap & Penyimpan Karbon*): Potensi biomassa vegetasi dan tanah dalam menyerap emisi CO2 atmosfer.
4. **PYA** (*Penyedia Air*): Ketersediaan air bersih dari sumber alami (air permukaan & tanah) untuk kebutuhan domestik manusia.
5. **PGN** (*Penyedia Pangan*): Potensi lanskap menyediakan hasil pertanian, perkebunan, dan sumber pangan hewani lokal.
6. **PKU** (*Pengatur Kualitas Udara*): Kapasitas vegetasi dalam menyerap polutan udara, memproduksi oksigen, dan menjaga kenyamanan iklim mikro.

---

## 2. Tiga Pilar Komponen Input JLH

Setiap piksel indikator JLH dihitung dari perpaduan linear antara 3 komponen spasial:

$$\\mathbf{JLH} = (\\text{Skor KBA} \\times W_{\\text{KBA}}) + (\\text{Skor KVA} \\times W_{\\text{KVA}}) + (\\text{Skor PL} \\times W_{\\text{PL}})$$

### 2.1 Karakteristik Bentang Alam (KBA)
- **Definisi:** Representasi faktor fisik abiotik permanen yang meliputi bentuk lahan (*landform*), elevasi topografi, geomorfologi, kelerengan, dan sifat batuan induk.
- **Tipe Data:** Raster Float32 / UInt8 (Skala 1 s.d. 5).
- **Format:** Cloud Optimized GeoTIFF (COG), resolusi 0.5 meter.
- **Peran:** Menjadi pembobot stabilitas fisik tanah. Misalnya, pada PGA, bentang alam pegunungan dengan batuan permeabel memiliki skor KBA tinggi untuk infiltrasi.

### 2.2 Karakteristik Vegetasi Alami (KVA)
- **Definisi:** Representasi tutupan vegetasi klimaks alami (ekosistem hutan primer, hutan rawa gambut, vegetasi riparian) yang belum terganggu antropogenik berat.
- **Tipe Data:** Raster Float32 / UInt8 (Skala 1 s.d. 5).
- **Format:** Cloud Optimized GeoTIFF (COG), resolusi 0.5 meter.
- **Peran:** Menilai integritas ekologis dan peran tutupan hutan alami dalam menjaga stabilitas iklim, kehati, dan retensi air tanah.

### 2.3 Penutupan Lahan Multiskala 2025 (PL)
- **Definisi:** Peta tutupan lahan aktual berbasis klasifikasi citra satelit resolusi tinggi tahun 2025 yang terbagi dalam ~2.300+ grid tile.
- **Tipe Data:** Raster Categorical / UInt8 (Nilai kelas 1 s.d. 15).
- **Peran:** Komponen paling dinamis dengan bobot dominan (60%) yang mencerminkan pemanfaatan permukaan bumi saat ini (hutan, sawah, kebun, badan air, hingga permukiman/jalan).

---

## 3. Formulasi Matematis & Bobot 6 Indikator JLH

Penetapan bobot ($W$) pada masing-masing indikator mengacu pada karakteristik biogeofisik Regional Sumatera:

| Indikator JLH | Bobot KBA ($W_{\\text{KBA}}$) | Bobot KVA ($W_{\\text{KVA}}$) | Bobot PL ($W_{\\text{PL}}$) | Total Bobot | Rasionalisasi Ilmiah |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **PGA** (Pengaturan Air) | **0.28** | **0.12** | **0.60** | 1.00 | Bentang alam (kemiringan lereng & jenis batuan KBA) sangat menentukan laju infiltrasi air. |
| **PHK** (Habitat & Kehati) | **0.24** | **0.16** | **0.60** | 1.00 | Tipe ekosistem alami (KVA) dan bentuk bentang alam (KBA) menyediakan relung ekologis spesifik. |
| **PPK** (Penyerap Karbon) | **0.20** | **0.20** | **0.60** | 1.00 | Vegetasi alami (KVA) dan biomassa tutupan lahan aktual (PL) memiliki kontribusi seimbang terhadap stok karbon. |
| **PYA** (Penyedia Air) | **0.32** | **0.08** | **0.60** | 1.00 | Cekungan air tanah dan geomorfologi KBA paling dominan dalam menampung debit air permukaan dan mata air. |
| **PGN** (Penyedia Pangan) | **0.28** | **0.12** | **0.60** | 1.00 | Kesuburan tanah vulkanik dan dataran aluvium (KBA) menentukan produktivitas pangan. |
| **PKU** (Kualitas Udara) | **0.15** | **0.25** | **0.60** | 1.00 | Kerapatan tajuk vegetasi alami (KVA) sangat krusial dalam menyaring partikulat udara dan menyerap panas. |

---

## 4. Tabel Matriks Skor Penutupan Lahan (PL Lookup Table)

Nilai kelas penutupan lahan (1 - 15) dikonversikan ke skor layanan ekosistem skala 1 (Sangat Rendah) hingga 5 (Sangat Tinggi):

| Kode | Kategori Penutupan Lahan | PL PGA | PL PHK | PL PPK | PL PYA | PL PGN | PL PKU |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | Water (Badan Air) | 5 | 1 | 1 | 5 | 4 | 5 |
| **2** | Natural Forest (Hutan Alami) | 5 | 5 | 5 | 3 | 4 | 5 |
| **4** | Flooded Vegetation (Rawa/Mangrove) | 4 | 3 | 3 | 3 | 4 | 5 |
| **5** | Crops (Pertanian/Sawah) | 3 | 1 | 1 | 3 | 4 | 3 |
| **7** | Development Space (Lahan Terbuka Binaan) | 2 | 1 | 1 | 2 | 1 | 2 |
| **8** | Bare Ground (Tanah Terbuka) | 1 | 1 | 1 | 1 | 1 | 1 |
| **11** | Rangeland (Padang Rumput/Semak) | 3 | 2 | 2 | 1 | 2 | 3 |
| **12** | Plantation (Perkebunan) | 3 | 2 | 2 | 2 | 3 | 4 |
| **13** | Uncertain Trees (Pohon Campuran) | 3 | 3 | 2 | 2 | 3 | 3 |
| **14** | Road (Jaringan Jalan) | 1 | 1 | 1 | 1 | 1 | 1 |
| **15** | Building (Bangunan/Gedung) | 1 | 1 | 1 | 2 | 1 | 1 |

---

## 5. Skrip Python: Transformasi & Kalkulasi JLH Grid 0.5m

Pemrosesan dilakukan per-grid tile penutupan lahan (~2.300+ tile) menggunakan teknik *windowed reading* pada raster KBA dan KVA untuk mencegah lonjakan memori (anti-OOM/crash):

```python
import os
import glob
import numpy as np
import rasterio
from rasterio.windows import from_bounds
from tqdm import tqdm

# 1. Konfigurasi Parameter Bobot
JLH_CONFIG = {
    'pga': {'name': 'Pengaturan Air',             'w_kba': 0.28, 'w_kva': 0.12, 'w_pl': 0.60},
    'phk': {'name': 'Pendukung Habitat & Kehati', 'w_kba': 0.24, 'w_kva': 0.16, 'w_pl': 0.60},
    'ppk': {'name': 'Penyerap & Simpan Karbon',   'w_kba': 0.20, 'w_kva': 0.20, 'w_pl': 0.60},
    'pya': {'name': 'Penyedia Air',               'w_kba': 0.32, 'w_kva': 0.08, 'w_pl': 0.60},
    'pgn': {'name': 'Penyedia Pangan (Sumatera)', 'w_kba': 0.28, 'w_kva': 0.12, 'w_pl': 0.60},
    'pku': {'name': 'Pengatur Kualitas Udara',    'w_kba': 0.15, 'w_kva': 0.25, 'w_pl': 0.60}
}

# 2. Lookup Skor PL ke Array 1D NumPy (Index 0 - 255)
PL_LOOKUP = {
    1:  {'pga': 5, 'phk': 1, 'ppk': 1, 'pya': 5, 'pgn': 4, 'pku': 5},
    2:  {'pga': 5, 'phk': 5, 'ppk': 5, 'pya': 3, 'pgn': 4, 'pku': 5},
    4:  {'pga': 4, 'phk': 3, 'ppk': 3, 'pya': 3, 'pgn': 4, 'pku': 5},
    5:  {'pga': 3, 'phk': 1, 'ppk': 1, 'pya': 3, 'pgn': 4, 'pku': 3},
    7:  {'pga': 2, 'phk': 1, 'ppk': 1, 'pya': 2, 'pgn': 1, 'pku': 2},
    8:  {'pga': 1, 'phk': 1, 'ppk': 1, 'pya': 1, 'pgn': 1, 'pku': 1},
    11: {'pga': 3, 'phk': 2, 'ppk': 2, 'pya': 1, 'pgn': 2, 'pku': 3},
    12: {'pga': 3, 'phk': 2, 'ppk': 2, 'pya': 2, 'pgn': 3, 'pku': 4},
    13: {'pga': 3, 'phk': 3, 'ppk': 2, 'pya': 2, 'pgn': 3, 'pku': 3},
    14: {'pga': 1, 'phk': 1, 'ppk': 1, 'pya': 1, 'pgn': 1, 'pku': 1},
    15: {'pga': 1, 'phk': 1, 'ppk': 1, 'pya': 2, 'pgn': 1, 'pku': 1}
}

PL_REMAP = {}
for key in JLH_CONFIG.keys():
    arr = np.zeros(256, dtype=np.float32)
    for c_val, scores in PL_LOOKUP.items():
        arr[c_val] = scores[key]
    PL_REMAP[key] = arr

# 3. Fungsi Komputasi Per Tile Grid
def process_single_grid(pl_tile_path, kba_datasets, kva_datasets, output_path):
    with rasterio.open(pl_tile_path) as src_pl:
        pl_data = src_pl.read(1)
        bounds = src_pl.bounds
        shape = pl_data.shape
        meta = src_pl.meta.copy()

        # Deteksi piksel valid (bukan nodata)
        valid_mask = pl_data > 0
        if not np.any(valid_mask):
            return False

        meta.update({
            'count': 6,
            'dtype': 'float32',
            'nodata': 0.0,
            'compress': 'deflate',
            'predictor': 3
        })

        jlh_stack = np.zeros((6, shape[0], shape[1]), dtype=np.float32)

        for band_idx, (key, cfg) in enumerate(JLH_CONFIG.items()):
            # A. Skor PL via Array Indexing Instan
            score_pl = PL_REMAP[key][pl_data]

            # B. Windowed Reading KBA & KVA sesuai bounds tile
            win_kba = from_bounds(*bounds, transform=kba_datasets[key].transform)
            score_kba = kba_datasets[key].read(1, window=win_kba, out_shape=shape).astype(np.float32)

            win_kva = from_bounds(*bounds, transform=kva_datasets[key].transform)
            score_kva = kva_datasets[key].read(1, window=win_kva, out_shape=shape).astype(np.float32)

            # C. Perhitungan Kombinasi Linier
            jlh_val = (score_kba * cfg['w_kba']) + (score_kva * cfg['w_kva']) + (score_pl * cfg['w_pl'])
            jlh_val = np.where(valid_mask, jlh_val, 0.0)
            jlh_stack[band_idx] = jlh_val

        with rasterio.open(output_path, 'w', **meta) as dst:
            dst.write(jlh_stack)
            for idx, key in enumerate(JLH_CONFIG.keys(), start=1):
                dst.set_band_description(idx, f"JLH_{key.upper()}")
        return True
```

---

## 6. Skrip Python: Mozaik Seamless Se-Sumbar & Kompresi LERC_ZSTD

Setelah ribuan tile grid selesai dihitung, seluruh tile digabungkan menjadi 1 file tunggal utuh per indikator (*seamless 1-file per layer*) menggunakan format kompresi modern **LERC_ZSTD**:

```python
import rasterio
from rasterio.windows import Window
import numpy as np

def export_seamless_lerc_zstd(input_vrt_path, output_tif_path, width, height, num_chunks=245):
    with rasterio.open(input_vrt_path) as src:
        profile = src.profile.copy()
        profile.update({
            'driver': 'GTiff',
            'dtype': 'float32',
            'nodata': 0.0,
            'compress': 'lerc_zstd',
            'max_z_error': 0.005,
            'tiled': True,
            'blockxsize': 512,
            'blockysize': 512,
            'bigtiff': 'YES'
        })

        chunk_size = 4096
        with rasterio.open(output_tif_path, 'w', **profile) as dst:
            for c in range(num_chunks):
                r_start = c * chunk_size
                curr_h = min(chunk_size, height - r_start)
                win = Window(0, r_start, width, curr_h)

                chunk_data = src.read(1, window=win)
                dst.write(chunk_data, 1, window=win)
                print(f"Chunk {c+1}/{num_chunks} tersimpan!")
```

### Hasil File Seamless 0.5m se-Sumatera Barat:
- `sumbar_2025_jlh_pga_seamless.tif` (403 MB)
- `sumbar_2025_jlh_phk_seamless.tif` (362 MB)
- `sumbar_2025_jlh_ppk_seamless.tif` (307 MB)
- `sumbar_2025_jlh_pya_seamless.tif` (360 MB)
- `sumbar_2025_jlh_pgn_seamless.tif` (342 MB)
- `sumbar_2025_jlh_pku_seamless.tif` (427 MB)
- `sumbar_2025_kba_seamless.tif` (178 MB) & `sumbar_2025_kva_seamless.tif` (169 MB)

---

## 7. Penyesuaian Kriteria Khusus (KK.gpkg) pada Layer PHK

Pada indikator Habitat & Keanekaragaman Hayati (PHK), dilakukan penyesuaian khusus menggunakan layer vektor poligon **Kriteria Khusus (`KK.gpkg`)**:
- Jika `KK_PHK25 == 'Kriteria Khusus 1'` $\\to$ Nilai dipaksa menjadi **`5.0`** (Zona Inti Konservasi Mutlak).
- Jika `KK_PHK25 IN ('Kriteria Khusus 2', 'Kriteria Khusus 3')` $\\to$ Nilai dipaksa menjadi **`4.0`** (Zona Penyangga Ekologis).
- Area di luar poligon KK tetap mempertahankan nilai asli PHK.
- File hasil penyesuaian: `sumbar_2025_jlh_phk_kk_seamless.tif` (375 MB).

---

## 8. Hilirisasi Analisis: JLH Ruang Hidup (Kesesuaian Relokasi Huntap/Huntara)

Layer JLH yang telah dimodelkan kemudian dihilirkan ke dalam analisis penentuan ruang hidup dan rekomendasi relokasi masyarakat pasca-bencana dengan mengintegrasikan:
1. **Bahaya Bencana Hidrometeorologi**: Banjir, Banjir Bandang (Galodo), dan Tanah Longsor.
2. **Formula Pembobotan Realistis**:
   - **50% Keselamatan Jiwa**: Longsor (20%), Banjir (15%), Galodo (15%).
   - **50% Mutu Hidup & Daya Dukung**: Penyedia Air (17.5%), Penyedia Pangan (17.5%), Pengatur Air (10%), Pengatur Udara (5%).
   - **Constraint Mutlak**: Bahaya Tinggi ($>0.66$) langsung dieliminasi.
3. **Screening Hukum**: Tumpang susun dengan **Kawasan Hutan 2026** (APL vs HPK vs HPT vs HL) dan **Pola Ruang RTRW Provinsi** untuk menghasilkan matriks rekomendasi kebijakan perizinan operasional.

---
*Dokumen ini disusun sebagai panduan teknis geospasial resmi proses komputasi end-to-end Jasa Lingkungan Hidup Provinsi Sumatera Barat.*
"""

with open('Dokumentasi_Metodologi_dan_Skrip_JLH_Sumbar.md', 'w', encoding='utf-8') as f:
    f.write(doc_content)

print("Dokumen Dokumentasi_Metodologi_dan_Skrip_JLH_Sumbar.md BERHASIL DIBUAT!")
