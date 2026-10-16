# Data Sampel Input & Hasil Pemodelan JLH (Resolusi 0.5 Meter)

Direktori ini berisi potongan data spasial (*clip*) berdasarkan poligon [`aoi_sample.geojson`](aoi_sample.geojson) (`100.4533° BT s.d. 100.4985° BT`, `-0.9877° LS s.d. -0.9541° LS`, ukuran matriks `10.060 x 7.485` piksel pada resolusi 0.5 meter, `EPSG:3857`).

---

## 1. Komponen Input (`01_input_komponen/`)

| Nama File | Tipe | Deskripsi |
| :--- | :---: | :--- |
| `sample_kba_05m.tif` | Raster (`UInt8`, ZSTD) | Kode `Value` Karakteristik Bentang Alam (KBA) sesuai `config_skor/skor_kba.csv` |
| `sample_kva_05m.tif` | Raster (`UInt8`, ZSTD) | Kode `Value` Karakteristik Vegetasi Alami (KVA) sesuai `config_skor/skor_kva.csv` |
| `sample_penutupan_lahan_2025_05m.tif` | Raster (`UInt8`, ZSTD) | Kelas Penutupan Lahan Multiskala 2025 (1–15) sesuai `config_skor/skor_penutupan_lahan.csv` |
| `sample_vektor_kba_kva.geojson` | Vektor (`GeoJSON`) | Poligon Unit Ekoregion (atribut KBA & KVA) hasil pemotongan dari `UE_Verlap_Sumbar.gdb` |
| `sample_vektor_kawasan_konservasi.geojson` | Vektor (`GeoJSON`) | Poligon Kawasan Konservasi (Kriteria Khusus PHK) di dalam area sampel |

---

## 2. Hasil Perhitungan JLH (`02_output_jlh/`)

Setiap file `.tif` dilengkapi file simbologi `.qml` bernama sama sehingga ketika dibuka di QGIS, pewarnaan kelas otomatis diterapkan.

| Nama File | Tipe | Deskripsi |
| :--- | :---: | :--- |
| `sample_jlh_pga_05m.tif` | Raster (`Float32`, LERC_ZSTD) | Skor JLH Pengaturan Air (1.00 – 5.00) |
| `sample_jlh_phk_05m.tif` | Raster (`Float32`, LERC_ZSTD) | Skor JLH Pendukung Habitat & Kehati murni sebelum koreksi KK (1.00 – 5.00) |
| `sample_jlh_phk_kk_05m.tif` | Raster (`Float32`, LERC_ZSTD) | Skor JLH Pendukung Habitat & Kehati setelah koreksi Kawasan Konservasi = 5.00 |
| `sample_jlh_ppk_05m.tif` | Raster (`Float32`, LERC_ZSTD) | Skor JLH Penyerap & Penyimpan Karbon (1.00 – 5.00) |
| `sample_jlh_pya_05m.tif` | Raster (`Float32`, LERC_ZSTD) | Skor JLH Penyedia Air (1.00 – 5.00) |
| `sample_jlh_pgn_05m.tif` | Raster (`Float32`, LERC_ZSTD) | Skor JLH Penyedia Pangan Regional Sumatera (1.00 – 5.00) |
| `sample_jlh_pku_05m.tif` | Raster (`Float32`, LERC_ZSTD) | Skor JLH Pengatur Kualitas Udara (1.00 – 5.00) |
| `sample_jlh_tinggi_05m.tif` | Raster (`UInt8`, ZSTD) | Komposit JLH Tinggi ($\ge 4.20$) dengan kode hierarkis 2-digit (`10=A`, `21=B1`, `22=B2`, `23=B3`, `31=C1`, `32=C2`, `33=C3`, `1=Non-JLHT`) |
