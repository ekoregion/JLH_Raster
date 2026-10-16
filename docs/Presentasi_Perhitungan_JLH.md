# MATERI PRESENTASI POWERPOINT: PEMODELAN & PERHITUNGAN JASA LINGKUNGAN HIDUP (JLH)
**Kementerian Lingkungan Hidup / Badan Pengendalian Lingkungan Hidup**  
**Direktorat Penyelenggaraan Sumber Daya Alam Berkelanjutan**

---

## SLIDE 1: HALAMAN JUDUL (TITLE SLIDE)

### Judul Utama:
# PEMODELAN DAN PERHITUNGAN INDEKS JASA LINGKUNGAN HIDUP (JLH)
### Sub-Judul:
#### Integrasi Spasial Resolusi Tinggi Berbasis Kawasan Bentang Alam (KBA), Kawasan Vegetasi Alami (KVA), dan Penutupan Lahan Multiskala

---
**Penyusun:** Tim Teknis Daya Dukung & Daya Tampung Lingkungan Hidup (D3TLH)  
**Institusi:** Kementerian Lingkungan Hidup (KLH) / BPLH  
**Tahun:** 2025 / 2026  
**Wilayah Studi Implementasi:** Provinsi Sumatera Barat  

> **Catatan Presenter / Speaker Notes:**  
> *"Selamat pagi/siang Bapak/Ibu sekalian. Pada sesi ini kita akan membahas secara komprehensif metodologi, formulasi matematis, dan rantai komputasi spasial dalam pemodelan Jasa Lingkungan Hidup (JLH). Pemutakhiran ini mengintegrasikan data biofisik beresolusi tinggi 0.5 meter guna menghasilkan arahan daya dukung dan daya tampung lingkungan hidup yang presisi dan akuntabel."*

---

## SLIDE 2: OUTLINE PRESENTASI (AGENDA)

### Struktur Pembahasan:
1. **Latar Belakang & Landasan Regulasi**
   - Urgensi pemetaan JLH berbasis UU 32/2009 & PP 46/2016
   - Peran JLH dalam RPJMD, RTRW, dan KLHS
2. **Konsep & Tiga Pilar Parameter Spasial**
   - Kawasan Bentang Alam (KBA) — Bentukan geomorfologi & kestabilan geologi
   - Kawasan Vegetasi Alami (KVA) — Struktur tutupan biotis alami
   - Penutupan Lahan Multiskala (PL) — Dinamika pemanfaatan ruang terkini
3. **Formulasi Matematis & Skema Pembobotan**
   - Formula Linear Berbobot (Weighted Linear Combination / WLC)
   - Matriks Bobot 6 Indikator JLH (PGA, PHK, PPK, PYA, PGN, PKU)
   - Skoring Matriks Penutupan Lahan
4. **Alur Pemrosesan Raster Skala Besar (0.5 Meter)**
   - Standardisasi Grid Spasial & Resampling Snapping (EPSG:3857)
   - Windowed Processing & Kompresi Multi-Band (Anti-OOM)
5. **Klasifikasi & Interpretasi Tingkat Jasa Lingkungan**
   - Interval 5 Kelas Daya Dukung & Daya Tampung (Sangat Rendah s.d. Sangat Tinggi)
6. **Hasil & Pemanfaatan Spasial (WebGIS & Analisis Kebijakan)**
   - Visualisasi VRT Seamless se-Provinsi Sumatera Barat
   - Rekomendasi Pemanfaatan Ruang Berkelanjutan

---

## SLIDE 3: KONSEP DASAR & TIGA PILAR JASA LINGKUNGAN HIDUP

### Apa itu Jasa Lingkungan Hidup (JLH)?
Jasa Lingkungan Hidup adalah manfaat yang diperoleh manusia dari ekosistem, mencakup fungsi penyediaan (*provisioning*), pengaturan (*regulating*), budaya (*cultural*), dan pendukung (*supporting*).

### Tiga Pilar Pembentuk Nilai JLH:
```
┌────────────────────────────────────────────────────────┐
│              INDEKS JASA LINGKUNGAN HIDUP              │
└──────────────────────────┬─────────────────────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
   ┌───────────┐     ┌───────────┐     ┌───────────┐
   │    KBA    │     │    KVA    │     │    PL     │
   │  Bentang  │  +  │ Vegetasi  │  +  │ Penutupan │
   │   Alam    │     │   Alami   │     │   Lahan   │
   │ (Geomorf) │     │  (Biotis) │     │ (Aktual)  │
   └───────────┘     └───────────┘     └───────────┘
```

1. **KBA (Kawasan Bentang Alam):**
   - Merepresentasikan stabilitas fisik bentang alam, morfogenesa, lereng, dan batuan induk.
   - Contoh: Danau, Pegunungan Vulkanik, Dataran Aluvium, Karst.
2. **KVA (Kawasan Vegetasi Alami):**
   - Merepresentasikan integritas biotis ekosistem alami asli setempat.
   - Menggambarkan daya pulih, cadangan plasma nutfah, dan keanekaragaman hayati.
3. **PL (Penutupan Lahan Aktual):**
   - Penentu dinamika tapak terkini (Hutan Primer/Sekunder, Perkebunan, Sawah, Permukiman, Badan Air).
   - Menjadi variabel penentu terbesar (bobot 60%) terhadap respon biofisik riil saat ini.

---

## SLIDE 4: PENGEMBANGAN FORMULA PERHITUNGAN JLH

### Formula Matematis:
Pendekatan yang digunakan adalah **Multi-Criteria Evaluation (MCE)** dengan metode **Weighted Linear Combination (WLC)**:

$$\mathbf{JLH}_i = \left( \mathbf{Skor}_{\text{KBA}, i} \times W_{\text{KBA}, i} \right) + \left( \mathbf{Skor}_{\text{KVA}, i} \times W_{\text{KVA}, i} \right) + \left( \mathbf{Skor}_{\text{PL}, i} \times W_{\text{PL}} \right)$$

Dimana:
- $i$ = Indikator Jasa Lingkungan yang dihitung ($i \in \{\text{PGA}, \text{PHK}, \text{PPK}, \text{PYA}, \text{PGN}, \text{PKU}\}$)
- $\mathbf{Skor}_{\text{KBA}, i}, \mathbf{Skor}_{\text{KVA}, i}, \mathbf{Skor}_{\text{PL}, i} \in [1, 5]$ (Skala ordinal 1 = Sangat Rendah s.d. 5 = Sangat Tinggi)
- Batasan Pembobotan:
  $$\sum W = W_{\text{KBA}, i} + W_{\text{KVA}, i} + W_{\text{PL}} = 1.00$$
  Dengan konsistensi: $W_{\text{PL}} = 0.60$ (tetap) dan $W_{\text{KBA}} + W_{\text{KVA}} = 0.40$.

> **Nilai Akhir Indeks JLH:**  
> Bergerak kontinu pada rentang **$1.00 \le \text{JLH} \le 5.00$** (Nilai 0 dialokasikan khusus untuk NoData / Luar Batas Administrasi).

---

## SLIDE 5: 6 INDIKATOR JLH & MATRIKS PEMBOBOTAN SPESIFIK

| Kode | Nama Indikator Jasa Lingkungan | Fungsi Ekologis | Bobot KBA ($W_{\text{KBA}}$) | Bobot KVA ($W_{\text{KVA}}$) | Bobot PL ($W_{\text{PL}}$) | Alasan Penentuan Bobot |
| :---: | :--- | :--- | :---: | :---: | :---: | :--- |
| **PGA** | **Pengaturan Tata Aliran Air** | Pengendali banjir, infiltrasi, tata debit sungai | **0.28** | **0.12** | **0.60** | Geomorfologi (kemiringan lereng & litologi KBA) sangat dominan memengaruhi hidrograf air. |
| **PHK** | **Pendukung Habitat & Kehati** | Perlindungan flora/fauna & plasma nutfah | **0.24** | **0.16** | **0.60** | KVA dan tutupan kanopi vegetasi sangat menentukan daya dukung relung ekologis. |
| **PPK** | **Penyimpan & Penyerap Karbon** | Mitigasi perubahan iklim & rosot karbon | **0.20** | **0.20** | **0.60** | Peran seimbang antara simpanan karbon tanah (KBA) dan biomassa atas tanah (KVA). |
| **PYA** | **Penyedia Air Bersih** | Ketersediaan kuantitas mata air & akifer | **0.32** | **0.08** | **0.60** | Formasi bentang alam hidrogeologis (imbuhan air) KBA memegang peranan krusial. |
| **PGN** | **Penyedia Pangan (Regio Sumatera)** | Daya dukung pangan nabati & hewani | **0.28** | **0.12** | **0.60** | Kesuburan dataran fluvial aluvium dan vulkanik KBA menjadi fondasi kesesuaian lahan pangan. |
| **PKU** | **Pengatur Kualitas Udara** | Penyerap polutan, debu, & pensuplai $O_2$ | **0.15** | **0.25** | **0.60** | Komposisi stratifikasi tajuk vegetasi (KVA) bertindak sebagai bio-filter utama polutan. |

---

## SLIDE 6: DETAIL SKORING PENUTUPAN LAHAN (PL) MULTISKALA

Tabel konversi nilai kelas tutupan lahan hasil klasifikasi deep learning (0.5 meter) ke dalam nilai kemampuan fungsi ekologis:

| Kode Piksel | Kelas Penutupan Lahan | PGA (Air) | PHK (Kehati) | PPK (Karbon) | PYA (Air) | PGN (Pangan) | PKU (Udara) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | Badan Air / Water | 5 | 1 | 1 | 5 | 4 | 5 |
| **2** | Hutan Alami / Natural Forest | 5 | 5 | 5 | 3 | 4 | 5 |
| **4** | Vegetasi Tergenang / Mangrove | 4 | 3 | 3 | 3 | 4 | 5 |
| **5** | Lahan Pertanian / Crops | 3 | 1 | 1 | 3 | 4 | 3 |
| **7** | Ruang Terbangun / Development | 2 | 1 | 1 | 2 | 1 | 2 |
| **8** | Lahan Terbuka / Bare Ground | 1 | 1 | 1 | 1 | 1 | 1 |
| **11** | Padang Rumput / Rangeland | 3 | 2 | 2 | 1 | 2 | 3 |
| **12** | Perkebunan / Plantation | 3 | 2 | 2 | 2 | 3 | 4 |
| **13** | Vegetasi Pohon Acak / Uncertain Trees | 3 | 3 | 2 | 2 | 3 | 3 |
| **14** | Jaringan Jalan / Road | 1 | 1 | 1 | 1 | 1 | 1 |
| **15** | Bangunan Gedung / Building | 1 | 1 | 1 | 2 | 1 | 1 |

---

## SLIDE 7: ARSITEKTUR KOMPUTASI RASTER (BIG DATA SPASIAL 0.5 METER)

### Tantangan:
- Wilayah Sumatera Barat terdiri dari **3.206 tile grid** (resolusi 0.5m x 0.5m).
- Jika digabung uncompressed: menghasilkan **ratusan gigabyte data**, rentan *Out of Memory (OOM)*.

### Solusi Desain Komputasi:
```
┌────────────────────────────────────────────────────────────────────────┐
│                        PIPELINE PERHITUNGAN JLH                        │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
    1. Grid Snapping: Setiap tile PL (0.5m) membaca extent spasialnya
                                    │
    2. Windowed Reading: Bounding box diekstrak langsung dari COG KBA & KVA
                                    │
    3. NumPy Vectorized Map: Konversi matriks kelas -> skor via Lookup Table
                                    │
    4. Matrix Algebra: JLH[1..6] dihitung secara paralel (Float32)
                                    │
    5. Smart Storage: Disimpan sebagai 6-Band GeoTIFF DEFLATE (Predictor 3)
       -> Menghemat ruang disk hingga 90-95% (<1.5 MB per grid)
                                    │
    6. Virtual Raster Mozaic: 6 file .VRT virtual tanpa duplikasi data fisik!
```

---

## SLIDE 8: KLASIFIKASI KELAS DAYA DUKUNG & DAYA TAMPUNG

Hasil nilai indeks kontinu $[1.00, 5.00]$ diklasifikasikan ke dalam 5 tingkatan standar KLH:

| Kelas Indeks | Rentang Nilai | Simbol Warna | Arahan Pengelolaan Lingkungan Hidup |
| :--- | :---: | :---: | :--- |
| **Sangat Tinggi** | $4.21 - 5.00$ | 🟩 Hijau Tua | Zona inti perlindungan & konservasi mutlak; fungsi penyangga ekosistem utama. |
| **Tinggi** | $3.41 - 4.20$ | 🟩 Hijau Muda | Pemanfaatan terbatas dengan syarat konservasi ketat; restorasi fungsi penyangga. |
| **Sedang** | $2.61 - 3.40$ | 🟨 Kuning | Zona budidaya terkendali; wajib menerapkan kaidah *Good Agricultural Practices*. |
| **Rendah** | $1.81 - 2.60$ | 🟧 Oranye | Kawasan terbangun/budidaya intensif; memerlukan mitigasi bahaya & RTH memadai. |
| **Sangat Rendah**| $1.00 - 1.80$ | 🟥 Merah | Kawasan kritis ekologis; kapasitas asimilasi jenuh, moratorium ekspansi terbangun. |

---

## SLIDE 9: KESIMPULAN & REKOMENDASI IMPLEMENTASI

1. **Akurasi Tinggi & Akuntabel:**  
   Metode ini mengintegrasikan data fisik geomorfologi makro (KBA) dan mikroskopis penutupan lahan 0.5 meter (PL), memberikan presisi tinggi yang belum pernah dicapai sebelumnya.
2. **Kesiapan Layanan WebGIS Interaktif:**  
   Format COG dan VRT memungkinkan visualisasi instan di WebGIS tanpa membebani server, siap diakses para pengambil kebijakan secara real-time.
3. **Pemanfaatan Dokumen Strategis:**  
   Menjadi basis data spasial resmi dalam penyusunan Kajian Lingkungan Hidup Strategis (KLHS), Rencana Tata Ruang Wilayah (RTRW), dan Rencana Perlindungan dan Pengelolaan Lingkungan Hidup (RPPLH).
