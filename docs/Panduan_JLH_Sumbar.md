# Pemodelan Jasa Lingkungan Hidup (JLH) Sumatera Barat

**Penyusun:** Direktorat Penyelenggaraan Sumber Daya Alam Berkelanjutan  

Notebook ini digunakan untuk menghitung **6 Indikator Jasa Lingkungan Hidup (JLH)** menggunakan data:
1. **KBA (Kawasan Berhutan Alami)** - 6 file raster COG (0.5 meter)
2. **KVA (Kawasan Vegetasi Alami)** - 6 file raster COG (0.5 meter)
3. **Penutupan Lahan (PL)** - ~2.300+ file raster grid tile (0.5 meter)

---
### Rumus Perhitungan:
$$\text{JLH} = (\text{Skor KBA} \times W_{\text{KBA}}) + (\text{Skor KVA} \times W_{\text{KVA}}) + (\text{Skor PL} \times W_{\text{PL}})$$

### 6 Indikator JLH & Bobot:

| Indikator JLH | Bobot KBA (W_KBA) | Bobot KVA (W_KVA) | Bobot PL (W_PL) |
| :--- | :---: | :---: | :---: |
| **PGA** (Pengaturan Air) | 0.28 | 0.12 | 0.60 |
| **PHK** (Pendukung Habitat & Kehati) | 0.24 | 0.16 | 0.60 |
| **PPK** (Penyerap & Penyimpan Karbon) | 0.20 | 0.20 | 0.60 |
| **PYA** (Penyedia Air) | 0.32 | 0.08 | 0.60 |
| **PGN** (Penyedia Pangan - Sumatera) | 0.28 | 0.12 | 0.60 |
| **PKU** (Pengatur Kualitas Udara) | 0.15 | 0.25 | 0.60 |

---
### Skor Penutupan Lahan (PL):

| Value | Kelas | PL PGA | PL PHK | PL PPK | PL PYA | PL PGN (Sumatera) | PL PKU |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | Water | 5 | 1 | 1 | 5 | 4 | 5 |
| **2** | Natural Forest | 5 | 5 | 5 | 3 | 4 | 5 |
| **4** | Flooded Vegetation | 4 | 3 | 3 | 3 | 4 | 5 |
| **5** | Crops | 3 | 1 | 1 | 3 | 4 | 3 |
| **7** | Development Space | 2 | 1 | 1 | 2 | 1 | 2 |
| **8** | Bare Ground | 1 | 1 | 1 | 1 | 1 | 1 |
| **11** | Rangeland | 3 | 2 | 2 | 1 | 2 | 3 |
| **12** | Plantation | 3 | 2 | 2 | 2 | 3 | 4 |
| **13** | Uncertain Trees | 3 | 3 | 2 | 2 | 3 | 3 |
| **14** | Road | 1 | 1 | 1 | 1 | 1 | 1 |
| **15** | Building | 1 | 1 | 1 | 2 | 1 | 1 |

> **Catatan Arsitektur:** Pemrosesan dilakukan **per-grid tile** menggunakan teknik *windowed reading* pada file COG KBA/KVA. Hasil per-grid disimpan sebagai 1 file GeoTIFF 6-band terkompresi DEFLATE (ringan & anti-OOM/memory crash), kemudian digabungkan secara virtual menjadi `.vrt` untuk QGIS.
