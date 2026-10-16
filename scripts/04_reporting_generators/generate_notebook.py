import json

notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Kajian Lingkungan Hidup Kesesuaian Lahan Relokasi Masyarakat (JLH Ruang Hidup)\n",
    "## Multi-Criteria Evaluation (MCE) Berbasis Jasa Lingkungan Hidup (JLH) & Bahaya Bencana se-Sumatera Barat\n",
    "\n",
    "Dokumen Jupyter Notebook ini memuat alur kerja analitis terpadu, metodologi komputasi spasial, serta evaluasi hasil perbandingan:\n",
    "1. **Skenario 1**: Keselamatan Bahaya Hidrometeorologi (Banjir + Banjir Bandang/Galodo + Tanah Longsor)\n",
    "2. **Skenario 2**: Keselamatan Multibahaya Komprehensif (BNPB/InaRISK)\n",
    "3. **Integrasi 6 Pilar Layanan Ekosistem JLH 2025** (Pedoman Resmi Rapid Environmental Assessment KemenLH)\n",
    "4. **Screening Hukum & Kebijakan Wilayah**: Kawasan Hutan 2026 & RTRW Pola Ruang Provinsi Sumatera Barat."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import os\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "import geopandas as gpd\n",
    "import rasterio\n",
    "import matplotlib.pyplot as plt\n",
    "\n",
    "print(\"Library spasial berhasil diinisialisasi!\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "### 1. Landasan Teori & Matriks Skoring Rapid Environmental Assessment (KemenLH)\n",
    "\n",
    "Setiap pilar Jasa Lingkungan Hidup (JLH) memiliki fungsi dan respon spasial yang berbeda terhadap tapak hunian:\n",
    "- **Penyedia Air (PYA) & Pangan (PGN)**: Bersifat *linear/inline* dengan kebutuhan dasar hidup manusia (semakin tinggi kelas JLH, semakin layak untuk tapak relokasi).\n",
    "- **Pengatur Air (PGA) & Udara (PKU)**: Bersifat *parabolik/inverted-U* (zona optimum adalah kelas sedang; kelas sangat tinggi dieliminasi/dihindari karena mencerminkan tanah jenuh/lembab atau hutan perawan).\n",
    "- **Habitat & Kehati (PHK) & Karbon (PPK)**: Bersifat *restriktif konservasi* (kelas sangat tinggi / KK 1 dan stok karbon tinggi wajib dilindungi penuh dari pembukaan permukiman).\n",
    "\n",
    "| Pilar JLH | Sifat Respon | Sangat Rendah (1) | Rendah (2) | Sedang (3) | Tinggi (4) | Sangat Tinggi (5) |\n",
    "| :--- | :--- | :---: | :---: | :---: | :---: | :---: |\n",
    "| **PYA (Air)** | Inline | 0.00 | 0.25 | 0.50 | 0.75 | 1.00 |\n",
    "| **PGN (Pangan)** | Inline | 0.00 | 0.25 | 0.50 | 0.75 | 1.00 |\n",
    "| **PGA (Tata Air)** | Parabolik | 0.00 | 0.20 | **1.00** | 0.50 | 0.00 (Konservasi) |\n",
    "| **PKU (Udara)** | Parabolik | 0.00 | 0.20 | **1.00** | 0.50 | 0.00 (Konservasi) |\n",
    "| **PHK (Kehati)** | Restriktif | **1.00** | 0.75 | 0.50 | 0.20 (KK2/3) | **0.00 (KK1 Constraint)** |\n",
    "| **PPK (Karbon)** | Restriktif | **1.00** | 0.75 | 0.50 | 0.20 | **0.00 (HCS Constraint)** |"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Definisi Lookup Table (LUT) Pembobotan JLH\n",
    "lut_pya = np.array([0.0, 0.0, 0.25, 0.50, 0.75, 1.00], dtype=np.float32)\n",
    "lut_pgn = np.array([0.0, 0.0, 0.25, 0.50, 0.75, 1.00], dtype=np.float32)\n",
    "lut_pga = np.array([0.0, 0.0, 0.20, 1.00, 0.50, 0.00], dtype=np.float32)\n",
    "lut_pku = np.array([0.0, 0.0, 0.20, 1.00, 0.50, 0.00], dtype=np.float32)\n",
    "lut_phk = np.array([0.0, 1.0, 0.75, 0.50, 0.20, 0.00], dtype=np.float32)\n",
    "lut_ppk = np.array([0.0, 1.0, 0.75, 0.50, 0.20, 0.00], dtype=np.float32)\n",
    "\n",
    "print(\"Lookup tables JLH siap digunakan!\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "### 2. Komparasi Empiris: Skenario Hidrometeorologi vs Multibahaya\n",
    "\n",
    "Pada analisis keselamatan tapak:\n",
    "- Indeks Bahaya $0.00 - 0.33 \\to$ **1.0** (*Factor*: Sangat Aman)\n",
    "- Indeks Bahaya $0.34 - 0.66 \\to$ **0.5** (*Factor*: Bersyarat Rekayasa Mitigasi)\n",
    "- Indeks Bahaya $0.67 - 1.00 \\to$ **0.0** (*Constraint*: Dieliminasi Total)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Hasil Statistik Spasial Komparatif se-Sumatera Barat\n",
    "data_komparasi = pd.DataFrame({\n",
    "    'Kategori': ['Aman / Sangat Layak (Skor 1.0)', 'Bersyarat / Rekayasa (Skor 0.5)', 'Bahaya Tinggi / Dieliminasi (Skor 0.0)'],\n",
    "    'Skenario 1 (Hidrometeorologi: Banjir, Galodo, Longsor)': [3.97, 36.55, 59.48],\n",
    "    'Skenario 2 (Multibahaya Komprehensif)': [0.53, 19.29, 80.18]\n",
    "})\n",
    "\n",
    "print(data_komparasi.to_string(index=False))\n",
    "\n",
    "# Visualisasi Grafik Perbandingan\n",
    "plt.figure(figsize=(10, 5))\n",
    "x = np.arange(len(data_komparasi['Kategori']))\n",
    "width = 0.35\n",
    "\n",
    "plt.bar(x - width/2, data_komparasi['Skenario 1 (Hidrometeorologi: Banjir, Galodo, Longsor)'], width, label='Skenario 1 (Hidromet: Banjir, Galodo, Longsor)', color='#2b83ba')\n",
    "plt.bar(x + width/2, data_komparasi['Skenario 2 (Multibahaya Komprehensif)'], width, label='Skenario 2 (Multibahaya)', color='#d7191c')\n",
    "\n",
    "plt.ylabel('Persentase Luas Daratan (%)')\n",
    "plt.title('Perbandingan Luas Kategori Keselamatan Bencana se-Sumatera Barat')\n",
    "plt.xticks(x, ['Aman (1.0)', 'Bersyarat (0.5)', 'Dieliminasi (0.0)'])\n",
    "plt.legend()\n",
    "plt.grid(axis='y', linestyle='--', alpha=0.7)\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "### 3. Data Pendukung Aksesibilitas & Kesejahteraan Masyarakat\n",
    "\n",
    "Dari ekstraksi OpenStreetMap (OSM) dan dataset bangunan yang berhasil diekstrak:\n",
    "- **Jaringan Jalan**: 186.190 ruas garis jalan se-Sumatera Barat\n",
    "- **Fasilitas Umum**: 1.863 titik fasilitas penting (Rumah Sakit, Puskesmas, Sekolah, Pasar)\n",
    "- **Tapak Bangunan Eksisting**: 985.269 poligon tapak bangunan"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "gpkg_path = 'data/osm_sumbar.gpkg'\n",
    "if os.path.exists(gpkg_path):\n",
    "    gdf_poi = gpd.read_file(gpkg_path, layer='poi_fasilitas_sumbar')\n",
    "    print(\"Distribusi Fasilitas Umum Terpetakan:\")\n",
    "    print(gdf_poi['amenity'].value_counts())\n",
    "else:\n",
    "    print(\"File osm_sumbar.gpkg belum berada di direktori lokal.\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "### 4. Tahap Screening Hukum & Rekomendasi Kebijakan\n",
    "\n",
    "Kawasan Hutan (2026) dan RTRW Provinsi bertindak sebagai **penentu arahan kebijakan operasional**:\n",
    "\n",
    "| Status Lahan | Pola Ruang RTRW | Arahan & Rekomendasi Tindak Lanjut |\n",
    "| :--- | :--- | :--- |\n",
    "| **APL (100700)** | Kawasan Budidaya Permukiman | **Prioritas Utama (Siap Bangun)**: Legalitas bersih, dapat langsung dibangun Huntap/Huntara. |\n",
    "| **APL (100700)** | Kawasan Budidaya Pertanian/Perkebunan | **Dapat Diberikan Izin**: Penyesuaian pemanfaatan ruang melalui rekomendasi PKKPR bencana. |\n",
    "| **HPK / HPT / HP** | Kawasan Hutan Produksi | **Rekomendasi Bersyarat**: Diperlukan mekanisme Persetujuan Penggunaan Kawasan Hutan (PPKH) / Pelepasan Kawasan Hutan sesuai UU Kehutanan. |\n",
    "| **HL / CA / TN** | Kawasan Lindung / Konservasi | **Dilarang untuk Permukiman Permanen**: Alihkan ke luar zona inti kawasan lindung. |"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Membaca data Kawasan Hutan dan RTRW Provinsi\n",
    "kh_path = 'data/jlh_seamless/Kawasan Hutan/kawasan_hutan_sumbar_2026.shp'\n",
    "rtrw_path = 'data/jlh_seamless/RTRW Provinsi/RTRW_Provinsi_Sumatera_Barat.shp'\n",
    "\n",
    "if os.path.exists(kh_path):\n",
    "    gdf_kh = gpd.read_file(kh_path)\n",
    "    print(\"Jumlah Poligon Kawasan Hutan:\", len(gdf_kh))\n",
    "    print(\"Distribusi Fungsi Kawasan Hutan:\")\n",
    "    print(gdf_kh['FUNGSIKWS'].value_counts())\n",
    "\n",
    "if os.path.exists(rtrw_path):\n",
    "    gdf_rtrw = gpd.read_file(rtrw_path)\n",
    "    print(\"\\nJumlah Poligon Pola Ruang RTRW:\", len(gdf_rtrw))\n",
    "    print(\"Distribusi Pola Ruang Utama:\")\n",
    "    print(gdf_rtrw['NAMOBJ'].value_counts().head(10))"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbformat_minor": 2
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}

with open('Kajian_Kesesuaian_Relokasi_JLH_Sumbar.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1)

print("Notebook Kajian_Kesesuaian_Relokasi_JLH_Sumbar.ipynb berhasil dibuat!")
