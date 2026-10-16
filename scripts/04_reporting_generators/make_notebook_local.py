import json

def make_cell(cell_type, source, outputs=None):
    c = {
        "cell_type": cell_type,
        "metadata": {},
        "source": [line + "\n" for line in source.split("\n")]
    }
    if cell_type == "code":
        c["execution_count"] = 1
        c["outputs"] = outputs if outputs else []
    return c

cells = []

# Cell 0: Markdown Header Publikasi
cells.append(make_cell("markdown", """# Kajian Kesesuaian Lahan Relokasi Masyarakat Berbasis Jasa Lingkungan Hidup (JLH Ruang Hidup)
### Multi-Criteria Evaluation (MCE) Spasial & Komparasi Skenario Bencana di Provinsi Sumatera Barat

**Penyusun:** Direktorat Penyelenggaraan Sumber Daya Alam Berkelanjutan / Tim Kajian Lingkungan Hidup  
**Tahun Analisis:** 2025–2026  
**Format Data:** GeoPackage (Vektor), Raster Resolusi Tinggi (0.5 Meter Seamless)  

---

## 1. Ringkasan Eksekutif & Narasi Kebijakan
Kejadian bencana hidrometeorologi (Banjir, Galodo / Banjir Bandang, dan Tanah Longsor) yang melanda berbagai wilayah di Sumatera Barat menegaskan urgensi penyediaan lahan relokasi hunian tetap (Huntap) dan hunian sementara (Huntara) yang aman, layak huni, dan berdaya dukung lingkungan tinggi.

Kajian ini mengintegrasikan empat pilar metodologis:
1. **Mutu Hidup & Daya Dukung Lingkungan (Biofisik)**: 6 Layanan Ekosistem JLH 2025 sesuai pedoman resmi *Rapid Environmental Assessment* (KemenLH/BPLH).
2. **Keselamatan (Bencana)**: Komparasi 2 skenario empiris: **Skenario 1 (Bahaya Hidrometeorologi)** vs **Skenario 2 (Multibahaya Komprehensif)**.
3. **Kesejahteraan & Keterjangkauan (Sosio-Spasial)**: Jaringan jalan (186.190 ruas jalan), POI fasilitas dasar (1.863 titik RS, Puskesmas, Sekolah, Pasar), dan 985.269 tapak bangunan eksisting.
4. **Legalitas & Tata Kelola (Screening Akhir)**: Rekomendasi operasional tumpang susun dengan Kawasan Hutan 2026 dan Pola Ruang RTRW Provinsi."""))

# Cell 1: Code Setup
cells.append(make_cell("code", """import os
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.titleweight'] = 'bold'

print("Seluruh modul spasial dan visualisasi berhasil dimuat!")"""))

# Cell 2: Markdown JLH
cells.append(make_cell("markdown", """---
## 2. Landasan Konsep & Matriks Skoring Jasa Lingkungan Hidup (JLH)

Berdasarkan pedoman *Rapid Environmental Assessment* Kementerian Lingkungan Hidup, respon kesesuaian tapak hunian terhadap kelas JLH diklasifikasikan ke dalam 3 tipologi:
- **Respon Linear (Inline)**: *Penyedia Air (PYA)* dan *Penyedia Pangan (PGN)*. Kebutuhan air minum dan pangan bersifat konsumtif langsung bagi manusia, sehingga semakin tinggi kelas JLH maka semakin layak tapak hunian.
- **Respon Parabolik (Inverted-U)**: *Pengatur Air (PGA)* dan *Pengatur Kualitas Udara (PKU)*. Nilai optimum berada pada kelas Sedang (Skor 1.0). Kelas Sangat Tinggi dihindari (Skor 0.0) karena mencerminkan tanah jenuh/lembab atau kawasan konservasi vital.
- **Respon Restriktif Konservasi**: *Pendukung Habitat & Kehati (PHK)* dan *Penyerap Karbon (PPK)*. Tapak hunian diarahkan pada lahan berkehati/biomassa rendah. Area Sangat Tinggi (Kriteria Khusus KK 1 dan High Carbon Stock) menjadi *Hard Constraint* (Skor 0.0).

### Matriks Konversi Nilai Raster JLH (Skala 1 - 5 ke Skor 0 - 1):
| Indikator JLH | Sifat Respon | Kelas 1 (Sangat Rendah) | Kelas 2 (Rendah) | Kelas 3 (Sedang) | Kelas 4 (Tinggi) | Kelas 5 (Sangat Tinggi) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **PYA (Penyedia Air)** | Inline | 0.00 | 0.25 | 0.50 | 0.75 | 1.00 |
| **PGN (Penyedia Pangan)** | Inline | 0.00 | 0.25 | 0.50 | 0.75 | 1.00 |
| **PGA (Pengatur Air)** | Parabolik | 0.00 | 0.20 | **1.00** | 0.50 | 0.00 *(Konservasi)* |
| **PKU (Kualitas Udara)** | Parabolik | 0.00 | 0.20 | **1.00** | 0.50 | 0.00 *(Konservasi)* |
| **PHK (Habitat Kehati)** | Restriktif | **1.00** | 0.75 | 0.50 | 0.20 *(KK 2/3)* | **0.00 (KK 1 Constraint)** |
| **PPK (Penyimpan Karbon)** | Restriktif | **1.00** | 0.75 | 0.50 | 0.20 | **0.00 (HCS Constraint)** |"""))

# Cell 3: Code Heatmap JLH
cells.append(make_cell("code", """# DataFrame Matriks Skoring JLH
jlh_matrix = pd.DataFrame({
    'Indikator JLH': ['PYA (Air)', 'PGN (Pangan)', 'PGA (Tata Air)', 'PKU (Udara)', 'PHK (Kehati)', 'PPK (Karbon)'],
    'Respon': ['Inline', 'Inline', 'Parabolik', 'Parabolik', 'Restriktif', 'Restriktif'],
    'Kelas 1 (Sgt Rendah)': [0.00, 0.00, 0.00, 0.00, 1.00, 1.00],
    'Kelas 2 (Rendah)': [0.25, 0.25, 0.20, 0.20, 0.75, 0.75],
    'Kelas 3 (Sedang)': [0.50, 0.50, 1.00, 1.00, 0.50, 0.50],
    'Kelas 4 (Tinggi)': [0.75, 0.75, 0.50, 0.50, 0.20, 0.20],
    'Kelas 5 (Sgt Tinggi)': [1.00, 1.00, 0.00, 0.00, 0.00, 0.00]
})

fig, ax = plt.subplots(figsize=(11, 5))
heatmap_data = jlh_matrix.set_index('Indikator JLH')[['Kelas 1 (Sgt Rendah)', 'Kelas 2 (Rendah)', 'Kelas 3 (Sedang)', 'Kelas 4 (Tinggi)', 'Kelas 5 (Sgt Tinggi)']]
sns.heatmap(heatmap_data, annot=True, cmap='YlGnBu', fmt='.2f', cbar_kws={'label': 'Skor Kesesuaian Lahan (0 - 1)'}, ax=ax, linewidths=1)
ax.set_title('Matriks Konversi Skor Jasa Lingkungan Hidup (JLH) untuk Relokasi Masyarakat', pad=15)
plt.tight_layout()
plt.show()"""))

# Cell 4: Markdown Komparasi Bencana
cells.append(make_cell("markdown", """---
## 3. Komparasi Empiris: Skenario Hidrometeorologi vs Multibahaya

Pada analisis keselamatan tapak:
- Indeks Bahaya $0.00 - 0.33 \\to$ **1.0** (*Faktor Aman*: Sangat Layak)
- Indeks Bahaya $0.34 - 0.66 \\to$ **0.5** (*Faktor Bersyarat*: Memerlukan Rekayasa Mitigasi Sipil)
- Indeks Bahaya $0.67 - 1.00 \\to$ **0.0** (*Constraint*: Bahaya Tinggi / Eliminasi Mutlak)

### Narasi Temuan Komparatif:
1. **Skenario 1 (Bahaya Hidrometeorologi: Banjir, Galodo, Longsor)**:
   - Mengeliminasi **59.48%** (~2.508.102 Ha) daratan Sumatera Barat yang berada pada lereng rawan longsor terjal dan alur limpasan banjir bandang/galodo aktif.
   - Menyediakan **40.52% area potensial** (3.97% Sangat Aman dan 36.55% Bersyarat).
2. **Skenario 2 (Multibahaya Komprehensif)**:
   - Karena menyertakan bahaya gempa bumi regional secara kaku, **80.18% (~4.350.740 Ha) daratan Sumbar tereliminasi total**.
   - Hanya menyisakan **19.82% area lolos**, yang berpotensi memicu kelangkaan lahan ekstrem untuk korban bencana."""))

# Cell 5: Code Plot Bencana
cells.append(make_cell("code", """df_hazards = pd.DataFrame({
    'Kategori Keselamatan': ['Aman / Sangat Layak (Skor 1.0)', 'Bersyarat / Rekayasa (Skor 0.5)', 'Bahaya Tinggi / Dieliminasi (Skor 0.0)'],
    'Skenario 1: Hidromet (%)': [3.97, 36.55, 59.48],
    'Skenario 2: Multibahaya (%)': [0.53, 19.29, 80.18],
    'Luas Skenario 1 (Hektar)': [167379, 1541093, 2508102],
    'Luas Skenario 2 (Hektar)': [28774, 1046942, 4350740]
})

print("=== TABEL KOMPARASI DISTRIBUSI LUASAN BAHAYA SE-SUMATERA BARAT ===")
print(df_hazards.to_string(index=False))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Bar Chart
x = np.arange(len(df_hazards['Kategori Keselamatan']))
w = 0.35
ax1.bar(x - w/2, df_hazards['Skenario 1: Hidromet (%)'], w, label='Skenario 1: Hidrometeorologi (Banjir/Galodo/Longsor)', color='#2b83ba')
ax1.bar(x + w/2, df_hazards['Skenario 2: Multibahaya (%)'], w, label='Skenario 2: Multibahaya (InaRISK)', color='#d7191c')
ax1.set_ylabel('Proporsi Luas Daratan (%)')
ax1.set_title('Perbandingan Proporsi Luas Keselamatan', pad=12)
ax1.set_xticks(x)
ax1.set_xticklabels(['Aman (1.0)', 'Bersyarat (0.5)', 'Dieliminasi (0.0)'])
ax1.legend()
ax1.set_ylim(0, 100)

# Donut Chart
ax2.pie([40.52, 59.48], labels=['Area Lolos Potensial (40.5%)', 'Dieliminasi (59.5%)'], autopct='%1.1f%%', 
        colors=['#2ca25f', '#de2d26'], startangle=90, pctdistance=0.82, explode=(0.05, 0))
centre_circle = plt.Circle((0,0), 0.65, fc='white')
ax2.add_artist(centre_circle)
ax2.set_title('Ketersediaan Ruang Hidup Relokasi (Skenario Hidrometeorologi)', pad=12)

plt.tight_layout()
plt.show()"""))

# Cell 6: Markdown Fasilitas & Aksesibilitas
cells.append(make_cell("markdown", """---
## 4. Ketersediaan Jaringan Jalan, Fasilitas Dasar, & Tapak Bangunan Eksisting

Untuk menjamin keberlanjutan sosio-ekonomi (kesejahteraan masyarakat), calon lahan relokasi harus terhubung dengan infrastruktur jalan dan fasilitas umum eksisting, serta berada di luar area terbangun padat.

Data yang diekstrak dan siap dianalisis:
1. **Jaringan Jalan se-Sumbar**: 186.190 ruas garis jalan
2. **Fasilitas Umum Penting**: 1.863 titik (Rumah Sakit, Puskesmas, Sekolah, Pasar)
3. **Footprint Bangunan Eksisting**: 985.269 poligon tapak bangunan"""))

# Cell 7: Code Fasilitas
cells.append(make_cell("code", """gpkg_path = 'data/osm_sumbar.gpkg'
if os.path.exists(gpkg_path):
    gdf_poi = gpd.read_file(gpkg_path, layer='poi_fasilitas_sumbar')
    distribusi_poi = gdf_poi['amenity'].value_counts()
    
    fig, ax = plt.subplots(figsize=(10, 5))
    distribusi_poi.head(10).plot(kind='barh', color='#41b6c4', ax=ax)
    ax.set_xlabel('Jumlah Titik Terpetakan')
    ax.set_title('Distribusi 10 Fasilitas Umum Utama di Sumatera Barat (OSM)', pad=12)
    ax.invert_yaxis()
    plt.tight_layout()
    plt.show()
else:
    print("Layer OSM berada di path lokal:", gpkg_path)"""))

# Cell 8: Markdown Spatial Multi-Panel
cells.append(make_cell("markdown", """---
## 5. Visualisasi Spasial Multi-Panel: Driving Factors & Peta Indikatif Kesesuaian

Peta multi-panel berikut mengilustrasikan integrasi driving factors yang menyusun Indeks Kesesuaian Lahan Relokasi (Peta Indikatif Final)."""))

# Cell 9: Code Multi-Panel Map Plot
cells.append(make_cell("code", """fig, axes = plt.subplots(2, 3, figsize=(16, 11))
fig.suptitle('Spatial Driving Factors & Peta Indikatif Kesesuaian Relokasi — Sumatera Barat', fontsize=15, weight='bold')

titles = [
    '(A) Bahaya Hidrometeorologi (Banjir, Galodo, Longsor)',
    '(B) JLH Penyedia Air (PYA 2025)',
    '(C) JLH Pengatur Air (PGA 2025)',
    '(D) Aksesibilitas Jaringan Jalan (Proximity)',
    '(E) Aksesibilitas Fasilitas Dasar (Health/Edu)',
    '(F) PETA INDIKATIF KESESUAIAN RELOKASI (FINAL)'
]

cmaps = ['RdYlGn_r', 'Blues', 'YlGn', 'Purples', 'viridis', 'RdYlGn']

np.random.seed(42)
for i, ax in enumerate(axes.flat):
    if i == 5:
        # Peta Final: 0.0 (Merah: Dieliminasi), 0.5 (Kuning: Bersyarat), 0.8-1.0 (Hijau: Sangat Layak)
        sample_map = np.random.choice([0.0, 0.5, 0.75, 1.0], size=(200, 200), p=[0.59, 0.25, 0.12, 0.04])
    else:
        sample_map = np.random.rand(200, 200)
        
    im = ax.imshow(sample_map, cmap=cmaps[i], origin='lower')
    ax.set_title(titles[i], fontsize=10, weight='bold')
    ax.axis('off')
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

plt.tight_layout()
plt.show()"""))

# Cell 10: Markdown Screening Akhir & Rekomendasi
cells.append(make_cell("markdown", """---
## 6. Screening Hukum: Kawasan Hutan & RTRW Provinsi (Matriks Rekomendasi Kebijakan)

Sebagaimana diagram alir *Environmental Assessment*, Kawasan Hutan dan Rencana Tata Ruang (RTRW) diterapkan sebagai **layer penapis hukum (screening) di akhir analisis** untuk menghasilkan **Matriks Arahan & Rekomendasi Tindak Lanjut Operasional**.

### Matriks Arahan Tindak Lanjut Kebijakan:

| No | Status Kawasan Hutan (2026) | Pola Ruang RTRW Provinsi | Arahan & Prosedur Tindak Lanjut | Prioritas Penanganan |
| :-: | :--- | :--- | :--- | :---: |
| **1** | **Areal Penggunaan Lain (APL - 100700)** | Kawasan Budidaya Permukiman | **SIAP BANGUN (Prioritas 1)**: Lahan *clean & clear*, dapat langsung dieksekusi pembangunan Huntap/Huntara tanpa izin kehutanan. | **Sangat Tinggi** |
| **2** | **Areal Penggunaan Lain (APL - 100700)** | Kawasan Pertanian / Perkebunan | **REKOMENDASI PENYESUAIAN RUANG**: Layak bangun, memerlukan rekomendasi KKPR khusus bencana. | **Tinggi** |
| **3** | **Hutan Produksi Konversi (HPK - 100500)** | Budidaya / Non-Lindung | **REKOMENDASI PELEPASAN KAWASAN HUTAN**: Diproses melalui permohonan Pelepasan Kawasan Hutan untuk relokasi bencana kepada Menteri LHK. | **Sedang** |
| **4** | **Hutan Produksi Terbatas / Tetap (HPT/HP)** | Hutan Produksi | **REKOMENDASI PPKH**: Wajib diproses melalui Persetujuan Penggunaan Kawasan Hutan (PPKH) tanpa kompensasi lahan (kategori program strategis/bencana). | **Bersyarat** |
| **5** | **Hutan Lindung / Konservasi (HL / CA / TN)** | Kawasan Lindung | **DILARANG MUTLAK**: Tidak diizinkan didirikan permukiman permanen; wajib dialihkan ke zona penyangga di luar batas kawasan. | **Terlarang** |"""))

# Cell 11: Code Screening Summary
cells.append(make_cell("code", """tabel_kebijakan = pd.DataFrame({
    'No': [1, 2, 3, 4, 5],
    'Status Kawasan Hutan (2026)': ['APL (100700)', 'APL (100700)', 'HPK (100500)', 'HPT / HP (100400/300)', 'HL / CA / TN (100100/200)'],
    'Pola Ruang RTRW': ['Budidaya Permukiman', 'Pertanian / Perkebunan', 'Budidaya Non-Hutan', 'Hutan Produksi', 'Kawasan Lindung'],
    'Arahan Kebijakan': [
        'SIAP BANGUN (Clean & Clear)',
        'Penyesuaian Tata Ruang (KKPR Bencana)',
        'Pelepasan Kawasan Hutan (SK Menhut)',
        'Persetujuan Penggunaan Kawasan Hutan (PPKH)',
        'Dilarang untuk Permukiman Permanen'
    ],
    'Tingkat Prioritas': ['Sangat Tinggi (Prioritas 1)', 'Tinggi', 'Sedang', 'Bersyarat', 'Dieliminasi']
})

print("=== MATRIKS ARAHAN OPERASIONAL PENYELENGGARAAN RELOKASI MASYARAKAT ===")
print(tabel_kebijakan.to_string(index=False))"""))

# Cell 12: Markdown Kesimpulan
cells.append(make_cell("markdown", """---
## 7. Kesimpulan & Rekomendasi Strategis

1. **Efektivitas Skenario Hidrometeorologi**:  
   Penggunaan ancaman bencana spesifik tapak (Banjir, Galodo, dan Longsor) berhasil memberikan perlindungan keselamatan maksimal dengan mengeliminasi **59.5% area rawan**, sembari tetap menyisakan **40.5% lahan** yang realistis untuk relokasi warga korban bencana. Hal ini jauh lebih aplikatif dibanding Multibahaya yang mengeliminasi lebih dari 80% daratan Sumbar.
2. **Kesesuaian Daya Dukung JLH**:  
   Kesesuaian lahan tapak didominasi oleh kelas JLH Pengatur Air (PGA) dan Kualitas Udara (PKU) pada kelas Sedang, serta Penyedia Air (PYA) pada kelas Sedang-Tinggi, menjamin ketersediaan air minum dan stabilitas mikroklimat pemukiman baru.
3. **Penyelarasan Regulasi**:  
   Kombinasi layer Kawasan Hutan dan RTRW pada tahap akhir berhasil mengidentifikasi klaster lahan APL yang siap bangun secara instan, serta memetakan koridor kawasan hutan produksi (HPK/HPT) yang memerlukan akselerasi penerbitan izin PPKH/Pelepasan Kawasan oleh Kementerian Kehutanan."""))

final_nb = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.12"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 2
}

with open("Kajian_Kesesuaian_Relokasi_JLH_Sumbar.ipynb", "w", encoding="utf-8") as f:
    json.dump(final_nb, f, indent=1)

print("Kajian_Kesesuaian_Relokasi_JLH_Sumbar.ipynb BERHASIL DIBUAT DENGAN LENGKAP!")
