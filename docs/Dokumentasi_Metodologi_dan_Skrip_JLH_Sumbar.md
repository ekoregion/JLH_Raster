# PEDOMAN TEKNIS & DOKUMENTASI METODOLOGI PENYUSUNAN JASA LINGKUNGAN HIDUP (JLH)
## Provinsi Sumatera Barat (Tahun Analisis: 2025–2026)
### Transformasi Spasial KBA, KVA, dan PL Multiskala Berbasis Cloud Computing Resolusi Ultra-Tinggi (0.5 Meter Seamless)

**Instansi Penyusun:** Direktorat Penyelenggaraan Sumber Daya Alam Berkelanjutan  
**Kementerian Lingkungan Hidup / Badan Pengendalian Lingkungan Hidup (BPLH)**  
**Resolusi Spasial Grid:** 0.5 Meter x 0.5 Meter (Ultra-High Resolution Seamless)  
**Sistem Proyeksi (CRS):** EPSG:3857 (WGS 84 / Pseudo-Mercator)  
**Format Penyimpanan:** Cloud Optimized GeoTIFF (COG), Kompresi LERC_ZSTD & Zstandard  

---

## DAFTAR ISI
1. [Landasan Hukum, Kebijakan, dan Kerangka Konseptual JLH](#1-landasan-hukum-kebijakan-dan-kerangka-konseptual-jlh)
2. [Definisi & Karakteristik Fisis 6 Indikator Layanan Ekosistem Prioritas](#2-definisi--karakteristik-fisis-6-indikator-layanan-ekosistem-prioritas)
3. [Tiga Pilar Komponen Input JLH (KBA, KVA, dan PL 2025)](#3-tiga-pilar-komponen-input-jlh-kba-kva-dan-pl-2025)
   - 3.1 Karakteristik Bentang Alam (KBA) - Faktor Abiotik Geomorfologi
   - 3.2 Karakteristik Vegetasi Alami (KVA) - Faktor Integritas Ekologis
   - 3.3 Penutupan Lahan (PL) Multiskala 2025 - Faktor Pemanfaatan Antropogenik
4. [Formulasi Matematis & Pembobotan Regional Sumatera](#4-formulasi-matematis--pembobotan-regional-sumatera)
   - 4.1 Model Kombinasi Linear Terbobot
   - 4.2 Rasionalisasi Saintifik Proporsi Bobot Tiap Indikator
5. [Matriks Penilaian & Tabel Lookup Penutupan Lahan (15 Kelas)](#5-matriks-penilaian--tabel-lookup-penutupan-lahan-15-kelas)
6. [Pipeline Arsitektur Komputasi Python Grid 0.5 Meter](#6-pipeline-arsitektur-komputasi-python-grid-05-meter)
   - 6.1 Skrip Tahap 1: Ekstraksi & Rasterisasi Grid KBA dan KVA (`generate_kba_kva_grids.py`)
   - 6.2 Skrip Tahap 2: Penggabungan Master KBA & KVA Menjadi Seamless UInt8 ZSTD (`create_seamless_kba_kva.py`)
   - 6.3 Skrip Tahap 3: Kalkulasi Paralel Multi-Core 6 Indikator JLH (`calculate_jlh_sumbar_2025.py`)
   - 6.4 Skrip Tahap 4: Mozaik Virtual Raster (VRT) & Ekspor LERC_ZSTD Chunking (`create_seamless_jlh_lerc.py`)
   - 6.5 Skrip Tahap 5: Penyesuaian Legal Kriteria Khusus pada Layer PHK (`apply_kk_phk.py`)
   - 6.6 Skrip Tahap 6: Pembentukan Piramida Resolusi Spasial (Internal Overviews)
7. [Spesifikasi Teknis Produk Akhir Raster Seamless Se-Sumatera Barat](#7-spesifikasi-teknis-produk-akhir-raster-seamless-se-sumatera-barat)
8. [Panduan Standard Operating Procedure (SOP) Analisis & Visualisasi di QGIS / ArcGIS](#8-panduan-standard-operating-procedure-sop-analisis--visualisasi-di-qgis--arcgis)
9. [Ringkasan & Rekomendasi Pemeliharaan Data Geospasial](#9-ringkasan--rekomendasi-pemeliharaan-data-geospasial)

---

## 1. Landasan Hukum, Kebijakan, dan Kerangka Konseptual JLH

Jasa Lingkungan Hidup (JLH) atau *Ecosystem Services* didefinisikan sebagai kontribusi langsung maupun tidak langsung dari ekosistem alami dan bentang alam terhadap kesejahteraan manusia, ketahanan pangan, dan keberlanjutan biosfer.

### Landasan Hukum:
1. **Undang-Undang Nomor 32 Tahun 2009 tentang Perlindungan dan Pengelolaan Lingkungan Hidup (PPLH)**:
   - Pasal 15 dan 19 mengamanatkan penyusunan Rencana Perlindungan dan Pengelolaan Lingkungan Hidup (RPPLH) serta Kajian Lingkungan Hidup Strategis (KLHS) berbasis inventarisasi Daya Dukung dan Daya Tampung Lingkungan Hidup (D3TLH).
2. **Peraturan Pemerintah Nomor 46 Tahun 2017 tentang Instrumen Ekonomi Lingkungan Hidup**:
   - Mewajibkan pemetaan fungsi penyedia, pengatur, dan pendukung ekosistem sebagai basis neraca sumber daya alam dan kompensasi jasa lingkungan.
3. **Konteks Kebutuhan Daerah Provinsi Sumatera Barat**:
   - Terletak di sepanjang busur vulkanik aktif Bukit Barisan dan Patahan Semangko, Sumatera Barat membutuhkan zonasi perlindungan ekologis berskala tapak (0.5 meter) untuk mengamankan kawasan tangkapan air dan koridor keanekaragaman hayati.

---

## 2. Definisi & Karakteristik Fisis 6 Indikator Layanan Ekosistem Prioritas

1. **PGA (Pengaturan Air / Water Regulation)**:
   - Kapasitas lanskap dalam meregulasi hidrologi permukaan dan bawah permukaan: infiltrasi tanah, retensi air limpasan hujan, pemeliharaan aliran dasar sungai (*baseflow*), dan pencegahan banjir/kekeringan.
2. **PHK (Pendukung Habitat & Keanekaragaman Hayati / Biodiversity Support)**:
   - Kemampuan ekosistem menyediakan habitat berkembang biak, pakan, dan koridor migrasi satwa liar kunci Sumatera (Harimau Sumatera, Tapir, Burung Rangkong, flora Rafflesia).
3. **PPK (Penyerap & Penyimpan Karbon / Carbon Storage)**:
   - Potensi biomassa vegetasi di atas dan di bawah tanah serta bahan organik tanah mengunci emisi CO2 atmosfer guna mendukung target Indonesia FOLU Net Sink 2030.
4. **PYA (Penyedia Air Bersih / Water Provisioning)**:
   - Ketersediaan debit dan volume air bersih alami yang dapat dimanfaatkan langsung oleh masyarakat untuk kebutuhan air minum domestik dan irigasi.
5. **PGN (Penyedia Pangan / Food Provisioning)**:
   - Produktivitas lanskap dalam menyediakan komoditas pangan nabati maupun hewani lokal secara lestari (sawah irigasi, kebun pangan, peternakan, perikanan darat).
6. **PKU (Pengatur Kualitas Udara / Air Quality Regulation)**:
   - Kapasitas kanopi vegetasi menyaring partikulat polutan (PM2.5, PM10), mereduksi gas rumah kaca, memproduksi oksigen, dan meredam pulau panas (*heat island*).

---

## 3. Tiga Pilar Komponen Input JLH (KBA, KVA, dan PL 2025)

Setiap nilai piksel JLH dihitung dari sintesis linear tiga komponen spasial:

### 3.1 Karakteristik Bentang Alam (KBA)
- **Definisi:** Representasi abiotik geomorfologi permanen: bentuklahan (*landform*), kelerengan DEMNAS, elevasi, dan litologi batuan induk.
- **Tipe Satuan di Sumbar:** Kerucut vulkanik muda (Marapi, Singgalang, Talang), karst struktural (Payakumbuh), dataran aluvial pesisir barat, dan perbukitan tektonik Bukit Barisan.
- **Skala Nilai:** Integer 1 sampai 5 (Skor 5 = Fungsi bentang alam optimal).

### 3.2 Karakteristik Vegetasi Alami (KVA)
- **Definisi:** Rekonstruksi tipe formasi ekosistem klimaks vegetasi asli sebelum konversi antropogenik.
- **Tipe Ekosistem:** Hutan hujan tropika pegunungan tinggi, hutan dataran rendah Dipterocarpaceae, hutan rawa air tawar/gambut, dan formasi mangrove pesisir.
- **Skala Nilai:** Integer 1 sampai 5.

### 3.3 Penutupan Lahan (PL) Multiskala 2025
- **Definisi:** Peta tutupan lahan aktual hasil klasifikasi citra satelit resolusi 0.5 meter tahun 2025 yang terbagi dalam ~2.300+ grid tile.
- **Skala Nilai:** Kategori kelas 1 s.d. 15.

---

## 4. Formulasi Matematis & Pembobotan Regional Sumatera

### 4.1 Model Kombinasi Linear Terbobot
$$\mathbf{JLH}_k = (\text{Skor KBA}_k \times W_{\text{KBA}, k}) + (\text{Skor KVA}_k \times W_{\text{KVA}, k}) + (\text{Skor PL}_k \times W_{\text{PL}, k})$$

### 4.2 Matriks Bobot Regional Sumatera:
| Indikator JLH | $W_{\text{KBA}}$ | $W_{\text{KVA}}$ | $W_{\text{PL}}$ | Total Bobot | Rasionalisasi Saintifik Regional Sumatera |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **PGA** (Pengaturan Air) | **0.28** | **0.12** | **0.60** | 1.00 | Bentang alam (kemiringan lereng & sifat batuan KBA) sangat mendominasi laju resapan air dan debit limpasan. |
| **PHK** (Habitat & Kehati) | **0.24** | **0.16** | **0.60** | 1.00 | Formasi vegetasi klimaks KVA dan keragaman topografi KBA membentuk relung habitat satwa liar endemik. |
| **PPK** (Penyimpan Karbon) | **0.20** | **0.20** | **0.60** | 1.00 | Tutupan biomassa aktual PL dan potensi tegakan hutan klimaks KVA berkontribusi seimbang terhadap stok karbon. |
| **PYA** (Penyedia Air) | **0.32** | **0.08** | **0.60** | 1.00 | Cekungan air tanah dan geomorfologi KBA paling dominan dalam menampung debit mata air alami. |
| **PGN** (Penyedia Pangan) | **0.28** | **0.12** | **0.60** | 1.00 | Morfologi dataran dan kesuburan tanah vulkanik KBA menentukan produktivitas pangan. |
| **PKU** (Kualitas Udara) | **0.15** | **0.25** | **0.60** | 1.00 | Kerapatan kanopi vegetasi alami KVA sangat efektif menyerap partikulat debu polutan dan gas emisi. |

---

## 5. Matriks Penilaian & Tabel Lookup Penutupan Lahan (15 Kelas)

| Kode | Kategori Penutupan Lahan (PL 2025) | PGA | PHK | PPK | PYA | PGN | PKU |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | Water (Badan Air / Danau / Sungai) | 5 | 1 | 1 | 5 | 4 | 5 |
| **2** | Natural Forest (Hutan Hujan Alami) | 5 | 5 | 5 | 3 | 4 | 5 |
| **4** | Flooded Vegetation (Rawa / Mangrove) | 4 | 3 | 3 | 3 | 4 | 5 |
| **5** | Crops (Pertanian Tanaman Pangan / Sawah) | 3 | 1 | 1 | 3 | 4 | 3 |
| **7** | Development Space (Lahan Terbuka Binaan) | 2 | 1 | 1 | 2 | 1 | 2 |
| **8** | Bare Ground (Tanah Terbuka / Tambang) | 1 | 1 | 1 | 1 | 1 | 1 |
| **11** | Rangeland (Padang Rumput / Semak Belukar) | 3 | 2 | 2 | 1 | 2 | 3 |
| **12** | Plantation (Perkebunan Sawit / Karet / dsb) | 3 | 2 | 2 | 2 | 3 | 4 |
| **13** | Uncertain Trees (Pohon Campuran / Agroforestri) | 3 | 3 | 2 | 2 | 3 | 3 |
| **14** | Road (Jaringan Jalan & Infrastruktur) | 1 | 1 | 1 | 1 | 1 | 1 |
| **15** | Building (Kawasan Terbangun / Permukiman) | 1 | 1 | 1 | 2 | 1 | 1 |

---

## 6. Pipeline Arsitektur Komputasi Python Grid 0.5 Meter

### 6.1 Skrip Tahap 1: Ekstraksi & Rasterisasi Grid KBA/KVA (`generate_kba_kva_grids.py`)
```python
import os, glob, time, openpyxl
import numpy as np
import rasterio
from rasterio.features import rasterize
from rasterio.transform import from_origin
from shapely.geometry import box
import geopandas as gpd

REF_X = 11110809.99449189      # Origin X Top-Left
REF_Y = 101049.75140393605     # Origin Y Top-Left
STEP_M = 3974.7246             # Ukuran grid per tile (meter)
TILE_W, TILE_H = 7949, 7949    # Lebar dan tinggi piksel
RES = 0.5                      # Resolusi spasial 0.5 meter

def rasterize_tile_vector(gdf_layer, col_val, bounds, out_tif_path):
    minx, miny, maxx, maxy = bounds
    tile_geom = box(minx, miny, maxx, maxy)
    sub_gdf = gdf_layer[gdf_layer.intersects(tile_geom)]
    if sub_gdf.empty:
        arr = np.zeros((TILE_H, TILE_W), dtype=np.uint8)
    else:
        shapes = ((geom, int(val)) for geom, val in zip(sub_gdf.geometry, sub_gdf[col_val]))
        trans = from_origin(minx, maxy, RES, RES)
        arr = rasterize(shapes=shapes, out_shape=(TILE_H, TILE_W), transform=trans, fill=0, dtype=np.uint8)
        
    profile = {
        'driver': 'GTiff', 'dtype': 'uint8', 'nodata': 0,
        'width': TILE_W, 'height': TILE_H, 'count': 1,
        'crs': 'EPSG:3857', 'transform': from_origin(minx, maxy, RES, RES),
        'tiled': True, 'blockxsize': 512, 'blockysize': 512, 'compress': 'lzw'
    }
    with rasterio.open(out_tif_path, 'w', **profile) as dst:
        dst.write(arr, 1)
```

### 6.2 Skrip Tahap 2: Penggabungan Master KBA & KVA UInt8 ZSTD (`create_seamless_kba_kva.py`)
```python
import rasterio
from rasterio.windows import Window
import numpy as np

def convert_vrt_to_seamless_uint8(vrt_path, output_path, chunk_size=8192):
    with rasterio.open(vrt_path) as src:
        meta = src.meta.copy()
        width, height = src.width, src.height
        meta.update({
            "driver": "GTiff", "dtype": "uint8", "count": 1,
            "tiled": True, "blockxsize": 512, "blockysize": 512,
            "compress": "zstd", "zstd_level": 9, "nodata": 0,
            "bigtiff": "YES", "num_threads": "ALL_CPUS"
        })
        with rasterio.open(output_path, "w", **meta) as dst:
            total_chunks = (height + chunk_size - 1) // chunk_size
            for chunk_idx, y_start in enumerate(range(0, height, chunk_size)):
                actual_chunk_height = min(chunk_size, height - y_start)
                window = Window(0, y_start, width, actual_chunk_height)
                chunk_data = src.read(1, window=window)
                dst.write(chunk_data, 1, window=window)
```

### 6.3 Skrip Tahap 3: Kalkulasi Paralel 6 Indikator JLH (`calculate_jlh_sumbar_2025.py`)
```python
import os, multiprocessing as mp
import numpy as np
import rasterio
from rasterio.windows import from_bounds

JLH_CONFIG = {
    'pga': {'name': 'Pengaturan Air',             'w_kba': 0.28, 'w_kva': 0.12, 'w_pl': 0.60},
    'phk': {'name': 'Pendukung Habitat & Kehati', 'w_kba': 0.24, 'w_kva': 0.16, 'w_pl': 0.60},
    'ppk': {'name': 'Penyerap & Simpan Karbon',   'w_kba': 0.20, 'w_kva': 0.20, 'w_pl': 0.60},
    'pya': {'name': 'Penyedia Air',               'w_kba': 0.32, 'w_kva': 0.08, 'w_pl': 0.60},
    'pgn': {'name': 'Penyedia Pangan (Sumatera)', 'w_kba': 0.28, 'w_kva': 0.12, 'w_pl': 0.60},
    'pku': {'name': 'Pengatur Kualitas Udara',    'w_kba': 0.15, 'w_kva': 0.25, 'w_pl': 0.60}
}
JLH_KEYS = list(JLH_CONFIG.keys())

def process_tile_task(task_args):
    kba_path, kva_path, out_path = task_args
    if os.path.exists(out_path):
        return 'skip'

    global worker_src_pl, shared_remap
    pl_remap, kba_remap, kva_remap = shared_remap['pl'], shared_remap['kba'], shared_remap['kva']

    with rasterio.open(kba_path) as src_kba, rasterio.open(kva_path) as src_kva:
        kba_data, kva_data = src_kba.read(1), src_kva.read(1)
        bounds = src_kba.bounds
        h, w = src_kba.height, src_kba.width
        prof = src_kba.profile.copy()

    # Windowed reading LULC 2025
    win_pl = from_bounds(*bounds, transform=worker_src_pl.transform)
    pl_data = worker_src_pl.read(1, window=win_pl, out_shape=(h, w), boundless=True, fill_value=0)
    nodata_mask = (pl_data == 0) | (pl_data == 255)

    if np.all(nodata_mask) and np.all(kba_data == 0) and np.all(kva_data == 0):
        return 'empty'

    # Kalkulasi 6 Band JLH Secara Vektorisasi
    jlh_result = np.zeros((6, h, w), dtype=np.float32)
    for idx, k in enumerate(JLH_KEYS):
        cfg = JLH_CONFIG[k]
        sk_kba = kba_remap[k][kba_data]
        sk_kva = kva_remap[k][kva_data]
        sk_pl = pl_remap[k][pl_data]

        band = (sk_kba * cfg['w_kba']) + (sk_kva * cfg['w_kva']) + (sk_pl * cfg['w_pl'])
        band[nodata_mask] = 0.0
        jlh_result[idx] = band

    prof.update({
        'count': 6, 'dtype': 'float32', 'nodata': 0.0,
        'compress': 'deflate', 'predictor': 3,
        'tiled': True, 'blockxsize': 512, 'blockysize': 512
    })
    with rasterio.open(out_path, 'w', **prof) as dst:
        dst.write(jlh_result)
        for b_idx, k in enumerate(JLH_KEYS, 1):
            dst.set_band_description(b_idx, f"JLH_{k.upper()}_{JLH_CONFIG[k]['name']}")
    return 'processed'
```

### 6.4 Skrip Tahap 4: Mozaik VRT & Ekspor LERC_ZSTD Chunking (`create_seamless_jlh_lerc.py`)
```python
import rasterio
from rasterio.windows import Window
import numpy as np

def export_seamless_lerc_zstd(input_vrt_path, output_tif_path, chunk_rows=4096):
    with rasterio.open(input_vrt_path) as src:
        profile = src.profile.copy()
        width, height = src.width, src.height
        profile.update({
            'driver': 'GTiff', 'dtype': 'float32', 'nodata': 0.0,
            'compress': 'lerc_zstd', 'max_z_error': 0.005,
            'tiled': True, 'blockxsize': 512, 'blockysize': 512,
            'bigtiff': 'YES', 'num_threads': 'all_cpus'
        })
        num_chunks = (height + chunk_rows - 1) // chunk_rows
        with rasterio.open(output_tif_path, 'w', **profile) as dst:
            for c in range(num_chunks):
                r_start = c * chunk_rows
                curr_h = min(chunk_rows, height - r_start)
                win = Window(0, r_start, width, curr_h)
                chunk_data = src.read(1, window=win)
                dst.write(chunk_data, 1, window=win)
```

### 6.5 Skrip Tahap 5: Penyesuaian Legal Kriteria Khusus (`apply_kk_phk.py`)
```python
import geopandas as gpd
import rasterio
from rasterio.features import rasterize
import numpy as np

def apply_kriteria_khusus(input_phk_tif, kk_gpkg_path, output_phk_kk_tif):
    gdf = gpd.read_file(kk_gpkg_path)
    gdf_kk1 = gdf[gdf['KK_PHK25'] == 'Kriteria Khusus 1']
    gdf_kk23 = gdf[gdf['KK_PHK25'].isin(['Kriteria Khusus 2', 'Kriteria Khusus 3'])]

    with rasterio.open(input_phk_tif) as src:
        meta = src.meta.copy()
        phk_data = src.read(1)
        transform = src.transform
        shape = phk_data.shape

        mask_kk1 = rasterize([(geom, 1) for geom in gdf_kk1.geometry], out_shape=shape, transform=transform, default_value=0, dtype=np.uint8)
        mask_kk23 = rasterize([(geom, 1) for geom in gdf_kk23.geometry], out_shape=shape, transform=transform, default_value=0, dtype=np.uint8)

        phk_adjusted = np.where(mask_kk1 == 1, 5.0, phk_data)
        phk_adjusted = np.where((mask_kk23 == 1) & (phk_adjusted < 4.0), 4.0, phk_adjusted)

        with rasterio.open(output_phk_kk_tif, 'w', **meta) as dst:
            dst.write(phk_adjusted, 1)
```

### 6.6 Skrip Tahap 6: Membangun Piramida Resolusi (Internal Overviews)
```python
import rasterio
from rasterio.enums import Resampling

def build_pyramid_overviews(tif_path):
    with rasterio.open(tif_path, 'r+') as dst:
        factors = [2, 4, 8, 16, 32, 64, 128]
        dst.build_overviews(factors, Resampling.nearest)
        dst.update_tags(ns='rio_overview', resampling='nearest')
```

---

## 7. Spesifikasi Teknis Produk Akhir Raster Seamless Se-Sumatera Barat

| Nama File Master | Ukuran File | Tipe Data | Kompresi | Deskripsi Lapisan |
| :--- | :---: | :---: | :---: | :--- |
| `sumbar_2025_jlh_pga_seamless.tif` | 403 MB | Float32 (1.0–5.0) | LERC_ZSTD | JLH Pengaturan Air (Water Regulation) |
| `sumbar_2025_jlh_phk_seamless.tif` | 362 MB | Float32 (1.0–5.0) | LERC_ZSTD | JLH Pendukung Habitat & Kehati (Alami) |
| `sumbar_2025_jlh_phk_kk_seamless.tif` | 375 MB | Float32 (1.0–5.0) | LERC_ZSTD | JLH Habitat & Kehati dengan Penyesuaian Kriteria Khusus |
| `sumbar_2025_jlh_ppk_seamless.tif` | 307 MB | Float32 (1.0–5.0) | LERC_ZSTD | JLH Penyerap & Penyimpan Karbon (Carbon Storage) |
| `sumbar_2025_jlh_pya_seamless.tif` | 360 MB | Float32 (1.0–5.0) | LERC_ZSTD | JLH Penyedia Air Bersih (Water Provisioning) |
| `sumbar_2025_jlh_pgn_seamless.tif` | 342 MB | Float32 (1.0–5.0) | LERC_ZSTD | JLH Penyedia Pangan (Food Provisioning) |
| `sumbar_2025_jlh_pku_seamless.tif` | 427 MB | Float32 (1.0–5.0) | LERC_ZSTD | JLH Pengatur Kualitas Udara (Air Quality) |
| `sumbar_2025_kba_seamless.tif` | 178 MB | UInt8 (1–255) | Zstandard L9 | Master Karakteristik Bentang Alam Se-Sumbar |
| `sumbar_2025_kva_seamless.tif` | 169 MB | UInt8 (1–255) | Zstandard L9 | Master Karakteristik Vegetasi Alami Se-Sumbar |

---

## 8. Panduan Standard Operating Procedure (SOP) Analisis & Visualisasi di QGIS / ArcGIS

1. **Menambahkan Layer Raster ke Kanvas Peta**:
   - *Drag-and-drop* file raster `sumbar_2025_jlh_*_seamless.tif` ke panel Layers QGIS atau ArcGIS Pro.
2. **Konfigurasi Nilai NoData (Transparansi Laut)**:
   - Klik kanan layer > Properties > Transparency. Pastikan nilai *Additional no data value* diisi `0.0` agar area laut menjadi transparan.
3. **Pengaturan Simbologi Warna (Singleband Pseudocolor)**:
   - Pilih *Color Ramp* gradasi ekologis seperti `Viridis`, `YlGn` (Kuning ke Hijau), atau `Spectral` (Inverted).
4. **Batas Rentang Nilai (Min / Max)**:
   - Tetapkan Min = `1.0` (Layanan Sangat Rendah) dan Max = `5.0` (Layanan Sangat Tinggi).
5. **Klasifikasi 5 Kelas Daya Dukung Lingkungan**:
   - `1.00 - 1.80`: Sangat Rendah (Merah)
   - `1.81 - 2.60`: Rendah (Oranye)
   - `2.61 - 3.40`: Sedang (Kuning)
   - `3.41 - 4.20`: Tinggi (Hijau Muda)
   - `4.21 - 5.00`: Sangat Tinggi (Hijau Tua Konservasi)

---

## 9. Ringkasan & Rekomendasi Pemeliharaan Data Geospasial

- **Pembaruan Berkala**: Cukup memperbarui layer Penutupan Lahan (PL) tahunan atau lima tahunan, karena lapisan KBA dan KVA bersifat statis dalam skala dekade.
- **Publikasi WebGIS**: Format Cloud Optimized GeoTIFF (COG) berarsitektur LERC_ZSTD siap disajikan melalui Map Server (GeoServer / TiTiler) untuk integrasi lintas instansi.
- **Pemanfaatan Kebijakan**: Menjadi instrumen primer dalam penyusunan RPPLH, KLHS, revisi RTRW, penetapan Nilai Ekonomi Karbon (NEK), dan evaluasi AMDAL.

---
*Dokumen ini disusun sebagai pedoman teknis resmi dan repositori kode sumber pemodelan Jasa Lingkungan Hidup (JLH) Provinsi Sumatera Barat tahun 2025–2026.*
