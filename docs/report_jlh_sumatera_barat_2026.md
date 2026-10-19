# Pemodelan Spasial Jasa Lingkungan Hidup (JLH) Berbasis KBA, KVA, dan Penutupan Lahan Multiskala Resolusi 0.5 Meter di Sumatera Barat

**Kementerian Lingkungan Hidup / Badan Pengendalian Lingkungan Hidup (BPLH)**  
**Direktorat Penyelenggaraan Sumber Daya Alam Berkelanjutan**  
**Tahun Analisis:** 2025–2026  
**Sistem Proyeksi (CRS):** EPSG:3857 (WGS 84 / Pseudo-Mercator)  
**Resolusi Spasial Grid:** 0.5 Meter x 0.5 Meter Seamless  

---

## 1. Pendahuluan

Jasa Lingkungan Hidup (JLH) atau *ecosystem services* merupakan kontribusi langsung maupun tidak langsung dari ekosistem alami dan struktur bentang alam terhadap kesejahteraan manusia, ketahanan pangan, dan keberlanjutan fungsi biosfer. Dalam kerangka hukum pengelolaan lingkungan di Indonesia, mandat inventarisasi dan pemetaan JLH diatur secara tegas melalui **Undang-Undang Nomor 32 Tahun 2009 tentang Perlindungan dan Pengelolaan Lingkungan Hidup (PPLH)**. Pada Pasal 15 dan 19 diamanatkan bahwa Rencana Perlindungan dan Pengelolaan Lingkungan Hidup (RPPLH) serta Kajian Lingkungan Hidup Strategis (KLHS) wajib disusun berbasis inventarisasi Daya Dukung dan Daya Tampung Lingkungan Hidup (D3TLH). Amanat ini diperkuat oleh **Peraturan Pemerintah Nomor 46 Tahun 2017 tentang Instrumen Ekonomi Lingkungan Hidup** serta **Permen LHK Nomor P.27/MENLHK/SETJEN/KUM.1/7/2018** yang mewajibkan pemetaan fungsi penyedia, pengatur, dan pendukung ekosistem sebagai acuan dasar neraca sumber daya alam dan skema kompensasi jasa lingkungan.

Provinsi Sumatera Barat memiliki konfigurasi biofisik yang unik sekaligus rentan. Wilayah ini dibelah oleh jalur pegunungan vulkanik aktif Bukit Barisan dan sistem sesar aktif Patahan Semangko yang memicu dinamika tektonik dan kerentanan tanah longsor tinggi. Di sisi lain, deretan kerucut vulkanik seperti Gunung Marapi, Gunung Singgalang, dan Gunung Talang menyediakan material tanah vulkanis yang sangat subur bagi pertanian pangan, serta berperan sebagai menara air alami (*water towers*) yang menopang daerah aliran sungai (DAS) lintas provinsi. Keberadaan danau tekto-vulkanik utama seperti Danau Singkarak, Danau Maninjau, Danau Diatas, dan Danau Dibawah menegaskan peran krusial lanskap Sumatera Barat dalam regulasi hidrologi regional.

Selama ini, pemetaan daya dukung lingkungan dan jasa ekosistem di tingkat regional umumnya mengandalkan data skala makro (1:250.000 hingga 1:50.000). Data pada skala makro memiliki keterbatasan signifikan dalam menangkap batas tapak, tebing curam, fragmentasi sempadan sungai kecil, dan batas kawasan terbangun mikro. Hal ini menimbulkan kesenjangan saat hasil analisis digunakan untuk perizinan berusaha, evaluasi pola ruang mikro kabupaten/kota, atau perencanaan zonasi mitigasi bencana.

Ketersediaan data tutupan lahan multiskala resolusi 0.5 meter (hasil integrasi *deep learning* resolusi menengah dan citra resolusi sangat tinggi tahun 2025) membuka peluang strategis untuk mentransformasikan pemodelan JLH ke skala tapak ultra-tinggi. Kajian ini bertujuan memodelkan 6 indikator layanan ekosistem prioritas (Pengaturan Air, Pendukung Habitat & Kehati, Penyimpan Karbon, Penyedia Air, Penyedia Pangan, dan Pengatur Kualitas Udara) secara seamless pada grid 0.5 meter, serta menyusun peta komposit terintegrasi Jasa Lingkungan Hidup Tinggi (JLH Tinggi) se-Provinsi Sumatera Barat.

---

## 2. Metodologi

Bagian ini menjelaskan kerangka alur pikir pemodelan, dataset masukan yang digunakan, formulasi matematis kombinasi linear terbobot regional, matriks penilaian skor, serta metode penggabungan bitwise untuk kawasan JLH Tinggi.

### 2.1 Alur Pikir Pemodelan
Pemodelan JLH dibangun atas sintesis tiga pilar spasial yang saling melengkapi: faktor abiotik bentang alam permanen (KBA), faktor integritas ekologis vegetasi klimaks asli (KVA), dan faktor pemanfaatan aktual antropogenik (Penutupan Lahan 2025). Setiap piksel berukuran 0.5 meter x 0.5 meter merefleksikan interaksi ketiga faktor tersebut melalui kombinasi linear terbobot. Nilai indeks kontinu yang dihasilkan selanjutnya dikoreksi dengan lapisan legal Kriteria Khusus pada kawasan konservasi, kemudian diekstraksi ke dalam zonasi komposit JLH Tinggi melalui aljabar bitwise 3-bit.

### 2.2 Dataset Masukan
Kajian ini memanfaatkan empat dataset spasial utama:
1. **Karakteristik Bentang Alam (KBA):** Merepresentasikan faktor geomorfologi abiotik permanen yang diturunkan dari peta Unit Ekoregion skala 1:250.000. Komponen KBA di Sumatera Barat mencakup 83 satuan bentuklahan, antara lain kerucut vulkanik muda Marapi-Singgalang-Talang, dataran fluvial aluvium, karst Payakumbuh, perbukitan tektonik denudasional Bukit Barisan, serta dataran endapan pantai pesisir barat.
2. **Karakteristik Vegetasi Alami (KVA):** Merepresentasikan tipe ekosistem vegetasi klimaks asli sebelum terjadi konversi antropogenik yang juga bersumber dari Unit Ekoregion 1:250.000. Teridentifikasi 94 tipe formasi ekosistem di Sumatera Barat, meliputi hutan hujan pegunungan atas dan bawah, hutan Dipterocarpaceae pamah, formasi rawa gambut pesisir, vegetasi riparian tepian sungai, serta mangrove pesisir.
3. **Penutupan Lahan (PL) Multiskala 2025:** Penutupan Lahan aktual merupakan produk fusi multiskala tahun 2025 beresolusi 0.5 meter yang menggabungkan model *deep learning* mikro (OpenEarthMap pada citra satelit resolusi sangat tinggi) dan meso (Sentinel-2 4-kanal 10m). Lapisan ini terbagi menjadi 15 kelas tutupan lahan.
4. **Layer Vektor Kriteria Khusus Kawasan Konservasi:** Lapisan vektor batas legal kawasan suaka alam dan kawasan pelestarian alam (Taman Nasional Kerinci Seblat, Taman Nasional Siberut, Suaka Margasatwa Tarusan Kamang, Cagar Alam Rimbo Panti, dll.) yang digunakan sebagai faktor koreksi legal pada indikator keanekaragaman hayati.

### 2.3 Formulasi Matematis dan Pembobotan Regional Sumatera
Setiap piksel indikator JLH ke-$k$ dihitung menggunakan model kombinasi linear terbobot (*Weighted Linear Combination*):

$$\text{JLH}_k = \left(\text{Skor KBA}_k \times W_{\text{KBA}, k}\right) + \left(\text{Skor KVA}_k \times W_{\text{KVA}, k}\right) + \left(\text{Skor PL}_k \times W_{\text{PL}, k}\right)$$

*Keterangan: $\text{Skor KBA}$ dan $\text{Skor KVA}$ bernilai integer 1–5; $\text{Skor PL}$ bernilai integer 1–5; sedangkan bobot regional Sumatera berjumlah total 1.00.*

#### Tabel 1. Matriks Bobot Regional Sumatera untuk 6 Indikator JLH dan Rasionalisasi Saintifik
| Indikator JLH | Kode | $W_{\text{KBA}}$ | $W_{\text{KVA}}$ | $W_{\text{PL}}$ | Rasionalisasi Saintifik Regional Sumatera |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Pengaturan Air** | PGA | 0.28 | 0.12 | 0.60 | Kemiringan lereng dan porositas batuan induk KBA sangat mendominasi laju infiltrasi dan debit limpasan air permukaan. |
| **Pendukung Habitat & Kehati** | PHK | 0.24 | 0.16 | 0.60 | Struktur topografi terjal KBA dan formasi vegetasi klimaks KVA membentuk relung ekologis satwa kunci Sumatera. |
| **Penyerap & Simpan Karbon** | PPK | 0.20 | 0.20 | 0.60 | Biomassa tutupan aktual PL dan cadangan karbon bawah tanah formasi klimaks KVA berkontribusi seimbang. |
| **Penyedia Air Bersih** | PYA | 0.32 | 0.08 | 0.60 | Cekungan air tanah, rekahan litologi, dan geomorfologi KBA paling menentukan ketersediaan debit mata air alami. |
| **Penyedia Pangan (Sumatera)** | PGN | 0.28 | 0.12 | 0.60 | Morfologi dataran aluvial dan kesuburan tanah vulkanik KBA menjadi faktor penentu produktivitas pertanian. |
| **Pengatur Kualitas Udara** | PKU | 0.15 | 0.25 | 0.60 | Kerapatan kanopi vegetasi alami KVA sangat efektif dalam menyerap emisi gas rumah kaca dan partikulat debu. |

### 2.4 Matriks Penilaian Skor Penutupan Lahan
Setiap kelas penutupan lahan 2025 diberi skor 1 hingga 5 pada masing-masing indikator layanan ekosistem:

#### Tabel 2. Matriks Skor 15 Kelas Penutupan Lahan Multiskala 2025
| Value | Kelas Penutupan Lahan | Deskripsi Tipologis | PGA | PHK | PPK | PYA | PGN | PKU |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | Water | Badan Air, Danau Tektonik, Sungai | 5 | 1 | 1 | 5 | 4 | 5 |
| **2** | Natural Forest | Hutan Hujan Alami Pegunungan & Dataran Rendah | 5 | 5 | 5 | 3 | 4 | 5 |
| **4** | Flooded Vegetation | Vegetasi Rawa Air Tawar, Hutan Gambut, Mangrove | 4 | 3 | 3 | 3 | 4 | 5 |
| **5** | Crops | Lahan Pertanian Basah, Sawah Beririgasi | 3 | 1 | 1 | 3 | 4 | 3 |
| **7** | Development Space | Ruang Terbuka Fasilitas Umum Binaan | 2 | 1 | 1 | 2 | 1 | 2 |
| **8** | Bare Ground | Tanah Terbuka, Singkapan Batuan, Tambang | 1 | 1 | 1 | 1 | 1 | 1 |
| **11** | Rangeland | Padang Rumput Alami, Semak Belukar | 3 | 2 | 2 | 1 | 2 | 3 |
| **12** | Plantation | Perkebunan Monokultur (Sawit, Karet) | 3 | 2 | 2 | 2 | 3 | 4 |
| **13** | Uncertain Trees | Pepohonan Campuran, Agroforestri, Kebun Campur | 3 | 3 | 2 | 2 | 3 | 3 |
| **14** | Road | Jaringan Jalan Beraspal & Infrastruktur Transportasi | 1 | 1 | 1 | 1 | 1 | 1 |
| **15** | Building | Kawasan Terbangun Permukiman & Gedung Komersial | 1 | 1 | 1 | 2 | 1 | 1 |

### 2.5 Metode Penggabungan Kawasan JLH Tinggi
Untuk memetakan wilayah dengan prioritas konservasi mutlak, dilakukan penggabungan multi-indikator menggunakan 3 indikator kunci:
1. **PGA (Pengaturan Air):** Menjamin fungsi tata air dan pencegahan bencana hidrometeorologi.
2. **PHK (Pendukung Habitat & Kehati):** Melindungi koridor genetik dan spesies flora-fauna endemik.
3. **PPK (Penyerap & Penyimpan Karbon):** Mengamankan stok karbon daratan guna mendukung target FOLU Net Sink 2030.

Piksel dikategorikan sebagai "Tinggi" jika nilainya mencapai ambang batas $\ge 4.20$ (pada skala 1–5). Aljabar bitwise 3-bit digunakan untuk menggabungkan status ketiga indikator:

$$\text{Bitmask} = 4 \times b_{\text{PGA}} + 2 \times b_{\text{PHK}} + 1 \times b_{\text{PPK}}$$

#### Tabel 3. Matriks Kebenaran (Truth Table) Aljabar Bitwise 3-Bit dan Skema Klasifikasi JLH Tinggi
| Kode UInt8 | Bitmask | Kode | Kategori Utama | JLH Penyusun ($\ge 4.2$) | Label Kelas | Warna Hex |
| :---: | :---: | :---: | :--- | :---: | :--- | :---: |
| **10** | `7 (111)` | **A** | Kategori A (3 JLH) | PGA + PHK + PPK | A - JLH Tinggi: Pengatur Air, Kehati & Karbon | `#9A7029` |
| **21** | `6 (110)` | **B1** | Kategori B (2 JLH) | PGA + PHK | B1 - JLH Tinggi: Pengatur Air & Kehati | `#63C5DA` |
| **22** | `3 (011)` | **B2** | Kategori B (2 JLH) | PHK + PPK | B2 - JLH Tinggi: Kehati & Karbon | `#F2EA3B` |
| **23** | `5 (101)` | **B3** | Kategori B (2 JLH) | PGA + PPK | B3 - JLH Tinggi: Pengatur Air & Karbon | `#AE529A` |
| **31** | `4 (100)` | **C1** | Kategori C (1 JLH) | PGA | C1 - JLH Tinggi: Pengatur Air | `#305496` |
| **32** | `2 (010)` | **C2** | Kategori C (1 JLH) | PHK | C2 - JLH Tinggi: Pendukung Habitat & Kehati | `#54B948` |
| **33** | `1 (001)` | **C3** | Kategori C (1 JLH) | PPK | C3 - JLH Tinggi: Penyerap & Penyimpan Karbon | `#ED1C24` |
| **1** | `0 (000)` | **Non-JLHT** | Di Luar JLH Tinggi | Tidak Ada (< 4.2) | Non-JLH Tinggi (Ketiga JLH < 4.2) | `#E2E8F0` |
| **0** | - | **NoData** | NoData | - | Laut / Di Luar Batas Wilayah Sumatera Barat | Transparan |

---

## 3. Implementasi Komputasi & Arsitektur Pipeline

Pemrosesan spasial pada resolusi 0.5 meter untuk wilayah daratan seluas 4,28 juta hektar mencakup lebih dari 171 miliar piksel per layer indikator.

### 3.1 Arsitektur Pipeline Pemrosesan
Pipeline komputasi disusun secara modular menjadi tiga tahapan skrip Python:
- **Tahap 1: Ekstraksi & Rasterisasi Grid KBA/KVA** (`generate_kba_kva_grids.py` dan `create_seamless_kba_kva.py`). Mengonversi vektor Unit Ekoregion menjadi grid raster UInt8 terkompresi Zstandard.
- **Tahap 2: Kalkulasi Paralel Multi-Core 6 Indikator JLH** (`calculate_jlh_sumbar_2025.py` dan `apply_kk_phk.py`). Mengeksekusi rumus kombinasi linear terbobot per tile dan menerapkan koreksi legal kawasan konservasi.
- **Tahap 3: Pengemasan Cloud Optimized GeoTIFF (COG) dan Klasifikasi JLH Tinggi** (`create_seamless_jlh_lerc.py` dan `calculate_jlh_tinggi_sumbar.py`). Menggabungkan VRT virtual menjadi raster fisik terkompresi LERC_ZSTD dan mengekstrak lapisan JLH Tinggi.

### 3.2 Strategi Optimasi Memori dan Pencegahan Out-of-Memory (Anti-OOM)
1. **Chunking Tiled Grid 512x512:** Seluruh raster internal dipecah menjadi blok petak 512x512 piksel, memungkinkan pembacaan sebagian (*windowed reading*) tanpa memuat seluruh citra ke memori.
2. **Pemetaan Lookup NumPy 1D:** Nilai skor diubah menjadi array pre-allocated 256 elemen bertipe float32. Pemetaan skor dari kode raster dilakukan secara tervektorisasi murni (*indexing array*) dengan kecepatan eksekusi mikrosekon per blok.
3. **Kompresi LERC_ZSTD:** Data raster kontinu 6 indikator disimpan menggunakan format kompresi LERC (*Limited Error Raster Compression*) dengan toleransi kesalahan maksimal 0.01 (`MAX_Z_ERROR=0.01`) dikombinasikan dengan Zstandard tingkat 12. Strategi ini mereduksi ukuran file hingga 85% tanpa menurunkan signifikansi presisi ilmiah.

### 3.3 Lingkungan Komputasi dan Konfigurasi Perangkat Keras
Kalkulasi dijalankan pada workstation komputasi multi-core dengan alokasi 16 proses worker paralel. Pustaka Python utama yang digunakan mencakup Rasterio 1.5.2, GDAL 3.9, Shapely 2.0, PyOgrio 0.7, NumPy 1.26, dan OpenPyXL 3.1.

---

## 4. Hasil dan Pembahasan

Kajian ini berhasil menghasilkan 8 layer raster seamless se-Sumatera Barat pada resolusi spasial 0.5 meter: 6 layer indikator JLH kontinu, 1 layer PHK terkoreksi Kriteria Khusus, dan 1 layer klasifikasi komposit JLH Tinggi.

### 4.1 Distribusi Spasial 6 Indikator Layanan Ekosistem
1. **Pengaturan Air (PGA):** Skor Sangat Tinggi ($\ge 4.2$) terkonsentrasi di punggung Bukit Barisan, lereng atas kompleks gunung api Marapi-Singgalang-Talang, dan hulu DAS Batang Kuranji, Batang Anai, dan Batang Ombilin. Kawasan ini memiliki kapasitas retensi hidrologis sangat tinggi dalam meminimalkan debit puncak banjir bandang (galodo).
2. **Pendukung Habitat & Kehati (PHK):** Koreksi Kriteria Khusus memperkuat perlindungan koridor TNKS di Solok Selatan dan Pesisir Selatan serta TNSL di Kepulauan Mentawai. Area ini mempertahankan integritas kanopi hutan primer Dipterocarpaceae pamah yang menjadi habitat satwa karismatik Sumatera.
3. **Penyerap & Penyimpan Karbon (PPK):** Stok biomassa karbon tertinggi berkolokasi dengan hutan primer dataran tinggi Bukit Barisan. Sementara kawasan perkebunan kelapa sawit monokultur di Dharmasraya dan Pasaman Barat menunjukkan nilai skor sedang (2.2 - 2.8).
4. **Penyedia Air Bersih (PYA):** Skor tertinggi teridentifikasi di danau-danau tekto-vulkanik dan mata air rekahan kaki lereng vulkanik yang melayani kebutuhan air baku perkotaan dan irigasi ribuan hektar persawahan.
5. **Penyedia Pangan (PGN):** Lembah-lembah aluvial subur di Dataran Agam, Tanah Datar, Solok, dan pesisir Padang Pariaman mencatatkan skor tertinggi berkat produktivitas pertanian sawah yang intensif.
6. **Pengatur Kualitas Udara (PKU):** Hutan lebat pegunungan Bukit Barisan berfungsi sebagai biofilter atmosferik utama yang meredam pulau panas regional dan menyerap partikulat debu lintas wilayah.

### 4.2 Analisis Luasan dan Karakteristik Kawasan JLH Tinggi
Dari total luas daratan Provinsi Sumatera Barat sebesar **4.287.713,83 hektar** (171,5 miliar piksel valid), seluas **2.640.838,16 hektar atau 61,59% daratan terkualifikasi sebagai Kawasan Jasa Lingkungan Hidup Tinggi (JLH Tinggi)**. Hal ini membuktikan bahwa mayoritas bentang alam Sumatera Barat mengemban fungsi ekologis vital berskala nasional.

#### Tabel 4. Rekapitulasi Statistik Jumlah Piksel, Luas Hektar, dan Persentase terhadap Luas Daratan Sumatera Barat untuk Kelas JLH Tinggi
| Kode | Kategori | JLH Penyusun ($\ge 4.2$) | Jumlah Piksel (0.5m) | Luas (Hektar) | Proporsi Daratan (%) |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **A** | Kategori A (3 JLH Tinggi) | PGA + PHK + PPK | 66.130.124.753 | 1.653.253,12 | 38,56% |
| **B1** | Kategori B (2 JLH Tinggi) | PGA + PHK | 3.933.223.228 | 98.330,58 | 2,29% |
| **B2** | Kategori B (2 JLH Tinggi) | PHK + PPK | 16.931.476.389 | 423.286,91 | 9,87% |
| **B3** | Kategori B (2 JLH Tinggi) | PGA + PPK | 10.325.456.044 | 258.136,40 | 6,02% |
| **C1** | Kategori C (1 JLH Tinggi) | PGA | 2.142.245.529 | 53.556,14 | 1,25% |
| **C2** | Kategori C (1 JLH Tinggi) | PHK | 2.428.607.342 | 60.715,18 | 1,42% |
| **C3** | Kategori C (1 JLH Tinggi) | PPK | 3.742.393.193 | 93.559,83 | 2,18% |
| **Subtotal** | **Total JLH Tinggi (A + B + C)** | **Minimal 1 Indikator $\ge 4.2$** | **105.633.526.478** | **2.640.838,16** | **61,59%** |
| **Non-JLHT** | Di Luar JLH Tinggi | Ketiga Indikator < 4.2 | 65.875.026.850 | 1.646.875,67 | 38,41% |
| **Total** | **Total Luas Daratan Sumbar** | **Seluruh Piksel Valid** | **171.508.553.328** | **4.287.713,83** | **100,00%** |

- **Kategori A (3 JLH Tinggi)** mendominasi dengan luas 1.653.253,12 ha (38,56% daratan). Kawasan ini merupakan benteng ekologis utama yang secara simultan menyelenggarakan fungsi perlindungan air, konservasi keanekaragaman hayati, dan penyerapan karbon maksimal. Wilayah ini diprioritaskan sebagai Kawasan Lindung Mutlak dalam RTRW.
- **Kategori B (2 JLH Tinggi)** mencakup 779.753,89 ha (18,19% daratan), didominasi oleh kelas B2 (PHK + PPK) seluas 423.286,91 ha (9,87%) dan kelas B3 (PGA + PPK) seluas 258.136,40 ha (6,02%). Wilayah ini berfungsi sebagai zona penyangga (*buffer zone*) kritis antara kawasan inti hutan lindung dan kawasan budidaya.
- **Kategori C (1 JLH Tinggi)** mencakup 207.831,15 ha (4,85% daratan), yang memerlukan pengelolaan tematik spesifik sesuai indikator keunggulannya.

---

## 5. Kesimpulan dan Rencana Tindak Lanjut

Kajian pemodelan Jasa Lingkungan Hidup (JLH) berbasis KBA, KVA, dan Penutupan Lahan Multiskala 2025 di Provinsi Sumatera Barat berhasil membangun basis data geospasial resolusi ultra-tinggi (0.5 meter) pertama yang mencakup seluruh daratan provinsi.

### 5.1 Kesimpulan Utama
1. Integrasi data abiotik (KBA), biotik (KVA), dan antropogenik (PL 2025) pada grid 0.5 meter mampu mengeliminasi bias generalisasi peta skala makro, sehingga menyajikan batas ekologis yang presisi hingga tingkat tapak.
2. Sebanyak 61,59% (2,64 juta hektar) daratan Sumatera Barat terkualifikasi sebagai Kawasan JLH Tinggi, dengan porsi terbesar berada pada Kategori A (38,56%) yang mengintegrasikan fungsi tata air, habitat kehati, dan cadangan karbon sekaligus.
3. Penerapan aljabar bitwise 3-bit terbukti menjadi solusi komputasi yang efisien dan elegan dalam menyatukan multi-indikator lingkungan ke dalam format raster terkompresi tanpa mengorbankan informasi individual penyusunnya.

### 5.2 Rencana Tindak Lanjut dan Rekomendasi Kebijakan
1. **Integrasi Kebijakan Tata Ruang:** Menggunakan peta JLH Tinggi sebagai masukan wajib dalam revisi Rencana Tata Ruang Wilayah (RTRW) Provinsi dan Kabupaten/Kota, serta penyusunan Rencana Perlindungan dan Pengelolaan Lingkungan Hidup (RPPLH).
2. **Diseminasi dan Interoperabilitas Data:** Mempublikasikan dataset raster COG LERC_ZSTD dan file simbologi QGIS ke dalam simpul jaringan geospasial (WebGIS Satu Data Indonesia) agar dapat diakses lintas sektor.
3. **Pemutakhiran Dinamis Berkala:** Memperbarui layer indikator JLH secara tahunan seiring tersedianya data pemutakhiran tutupan lahan multiskala berbasis citra satelit terbaru.

---

## Daftar Pustaka

- Costanza, R., d'Arge, R., de Groot, R., Farber, S., Grasso, M., Hannon, B., ... & van den Belt, M. (1997). The value of the world's ecosystem services and natural capital. *Nature*, 387(6630), 253-260.
- Costanza, R., de Groot, R., Sutton, P., van der Ploeg, S., Anderson, S. J., Kubiszewski, I., ... & Turner, R. K. (2014). Changes in the global value of ecosystem services. *Global Environmental Change*, 26, 152-158.
- De Groot, R. S., Wilson, M. A., & Boumans, R. M. (2002). A typology for the classification, description and valuation of ecosystem functions, goods and services. *Ecological Economics*, 41(3), 393-408.
- Haines-Young, R., & Potschin, M. (2018). *Common International Classification of Ecosystem Services (CICES) V5.1 and Guidance on the Application of the Revised Structure*. Fabis Consulting Ltd.
- Kementerian Lingkungan Hidup dan Kehutanan. (2018). *Peraturan Menteri LHK Nomor P.27/MENLHK/SETJEN/KUM.1/7/2018 tentang Pedoman Penyusunan Daya Dukung dan Daya Tampung Lingkungan Hidup*.
- Millennium Ecosystem Assessment (MEA). (2005). *Ecosystems and Human Well-being: Synthesis*. Island Press, Washington, DC.
- Pemerintah Republik Indonesia. (2009). *Undang-Undang Nomor 32 Tahun 2009 tentang Perlindungan dan Pengelolaan Lingkungan Hidup*. Lembaran Negara Republik Indonesia Tahun 2009 Nomor 140.
- Pemerintah Republik Indonesia. (2017). *Peraturan Pemerintah Nomor 46 Tahun 2017 tentang Instrumen Ekonomi Lingkungan Hidup*. Lembaran Negara Republik Indonesia Tahun 2017 Nomor 228.
- TEEB. (2010). *The Economics of Ecosystems and Biodiversity: Ecological and Economic Foundations*. Earthscan, London and Washington.
