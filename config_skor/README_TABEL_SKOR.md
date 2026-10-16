# Katalog Lengkap Tabel Skor, Bobot, dan Kodefikasi JLH (2025-2026)

Dokumen ini merangkum seluruh tabel referensi angka yang digunakan dalam skrip pemodelan **Jasa Lingkungan Hidup (JLH)** agar tidak terpencar dan dapat langsung dibaca di GitHub maupun diekspor ke CSV/Excel.

## Daftar File di Folder `config_skor/`

- `Skor_JLH_2026.xlsx` — File master Excel asli (Sheet `Skor KBA` dan `Skor KVA`).
- `bobot_indikator_sumatera.csv` — Tabel bobot $W_{\text{KBA}}, W_{\text{KVA}}, W_{\text{PL}}$ untuk 6 indikator JLH.
- `skor_penutupan_lahan.csv` — Matriks skor 15 kelas Penutupan Lahan (Multiscale 0.5m).
- `skor_kba.csv` — Tabel lengkap 83 kelas Karakteristik Bentang Alam (KBA) beserta skor 6 JLH.
- `skor_kva.csv` — Tabel lengkap 94 kelas Karakteristik Vegetasi Alami (KVA) beserta skor 6 JLH.
- `kodefikasi_jlh_tinggi.csv` — Skema kodefikasi hierarkis 2-digit (`UInt8`) dan palet warna Diagram Venn JLH Tinggi.
- `style_qgis/` — File simbologi `.qml` siap pakai di QGIS.

---
## 1. Tabel Bobot Indikator JLH Regional Sumatera

| Kode | Nama Indikator | $W_{\text{KBA}}$ | $W_{\text{KVA}}$ | $W_{\text{PL}}$ | Total |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **PGA** | Pengaturan Air | 0.28 | 0.12 | 0.60 | 1.00 |
| **PHK** | Pendukung Habitat & Kehati | 0.24 | 0.16 | 0.60 | 1.00 |
| **PPK** | Penyerap & Penyimpan Karbon | 0.20 | 0.20 | 0.60 | 1.00 |
| **PYA** | Penyedia Air | 0.32 | 0.08 | 0.60 | 1.00 |
| **PGN** | Penyedia Pangan (Sumatera) | 0.28 | 0.12 | 0.60 | 1.00 |
| **PKU** | Pengatur Kualitas Udara | 0.15 | 0.25 | 0.60 | 1.00 |

---
## 2. Tabel Skor Penutupan Lahan (PL Multiskala 0.5m)

| Value | Kelas PL | Deskripsi | PGA | PHK | PPK | PYA | PGN | PKU |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | Water | Badan Air / Danau / Sungai | 5 | 1 | 1 | 5 | 4 | 5 |
| **2** | Natural Forest | Hutan Hujan Alami | 5 | 5 | 5 | 3 | 4 | 5 |
| **4** | Flooded Vegetation | Vegetasi Rawa / Mangrove | 4 | 3 | 3 | 3 | 4 | 5 |
| **5** | Crops | Pertanian Tanaman Pangan / Sawah | 3 | 1 | 1 | 3 | 4 | 3 |
| **7** | Development Space | Lahan Terbuka Binaan | 2 | 1 | 1 | 2 | 1 | 2 |
| **8** | Bare Ground | Tanah Terbuka / Singkapan / Tambang | 1 | 1 | 1 | 1 | 1 | 1 |
| **11** | Rangeland | Padang Rumput / Semak Belukar | 3 | 2 | 2 | 1 | 2 | 3 |
| **12** | Plantation | Perkebunan Tahunan / Monokultur | 3 | 2 | 2 | 2 | 3 | 4 |
| **13** | Uncertain Trees | Pepohonan Campuran / Agroforestri | 3 | 3 | 2 | 2 | 3 | 3 |
| **14** | Road | Jaringan Jalan & Infrastruktur | 1 | 1 | 1 | 1 | 1 | 1 |
| **15** | Building | Bangunan / Permukiman | 1 | 1 | 1 | 2 | 1 | 1 |

---
## 3. Tabel Kodefikasi & Simbologi JLH Tinggi (Ambang Batas $\ge 4.20$)

| Kode Raster (`UInt8`) | Bitmask (`4*PGA + 2*PHK + 1*PPK`) | Kode Kelas | Kategori | JLH Penyusun | Warna Hex |
| :---: | :---: | :---: | :--- | :--- | :---: |
| **10** | `7 (111)` | **A** | Kategori A (3 JLH Tinggi) | PGA + PHK + PPK | `#9A7029` |
| **21** | `6 (110)` | **B1** | Kategori B (2 JLH Tinggi) | PGA + PHK | `#63C5DA` |
| **22** | `3 (011)` | **B2** | Kategori B (2 JLH Tinggi) | PHK + PPK | `#F2EA3B` |
| **23** | `5 (101)` | **B3** | Kategori B (2 JLH Tinggi) | PGA + PPK | `#AE529A` |
| **31** | `4 (100)` | **C1** | Kategori C (1 JLH Tinggi) | PGA | `#305496` |
| **32** | `2 (010)` | **C2** | Kategori C (1 JLH Tinggi) | PHK | `#54B948` |
| **33** | `1 (001)` | **C3** | Kategori C (1 JLH Tinggi) | PPK | `#ED1C24` |
| **1** | `0 (000)` | **Non-JLHT** | Di Luar JLH Tinggi (< 4.2) | Tidak Ada (< 4.2) | `#E2E8F0` |
| **0** | `-` | **NoData** | NoData | - | `Transparan` |

---
## 4. Tabel Lengkap Skor Karakteristik Bentang Alam (KBA - 83 Kelas)

| Value | Karakteristik Bentang Alam (KBA_250) | PGA | PHK | PPK | PYA | PGN | PKU |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | Danau | 4 | 1 | 2 | 5 | 5 | 5 |
| **2** | Dataran fluvial bermaterial aluvium | 1 | 5 | 2 | 4 | 5 | 3 |
| **3** | Dataran fluvial berombak-bergelombang bermaterial aluvium | 2 | 4 | 3 | 4 | 5 | 4 |
| **4** | Dataran fluviomarin bermaterial aluvium | 1 | 4 | 2 | 3 | 5 | 3 |
| **5** | Dataran fluviovulkanik bermaterial aluvium | 2 | 4 | 3 | 4 | 5 | 4 |
| **6** | Dataran lakustrin bermaterial aluvium | 2 | 4 | 3 | 4 | 5 | 4 |
| **7** | Dataran marin bermaterial batuan sedimen karbonat | 4 | 2 | 1 | 2 | 2 | 3 |
| **8** | Dataran marin berpasir bermaterial aluvium | 2 | 2 | 2 | 2 | 3 | 3 |
| **9** | Dataran organik bermaterial gambut | 2 | 4 | 5 | 3 | 2 | 5 |
| **10** | Dataran organik koralian bermaterial batuan sedimen karbonat | 1 | 1 | 2 | 1 | 1 | 4 |
| **11** | Dataran organik koralian berombak-bergelombang bermaterial batuan sedimen karbonat | 1 | 1 | 5 | 1 | 1 | 4 |
| **12** | Dataran solusional karst bermaterial batuan sedimen karbonat | 4 | 3 | 2 | 3 | 3 | 4 |
| **13** | Dataran solusional karst berombak-bergelombang bermaterial batuan sedimen karbonat | 5 | 4 | 2 | 3 | 3 | 4 |
| **14** | Dataran struktural bermaterial batuan sedimen karbonat | 4 | 2 | 3 | 3 | 3 | 4 |
| **15** | Dataran struktural berombak-bergelombang bermaterial batuan sedimen karbonat | 4 | 2 | 3 | 3 | 3 | 4 |
| **16** | Dataran struktural lipatan bermaterial batuan metamorfik | 2 | 2 | 2 | 3 | 2 | 4 |
| **17** | Dataran struktural lipatan bermaterial campuran batuan sedimen karbonat dan non karbonat | 4 | 3 | 2 | 3 | 4 | 4 |
| **18** | Dataran struktural lipatan berombak-bergelombang bermaterial batuan metamorfik | 2 | 2 | 2 | 3 | 2 | 4 |
| **19** | Dataran struktural lipatan berombak-bergelombang bermaterial batuan sedimen karbonat | 4 | 3 | 3 | 3 | 3 | 4 |
| **20** | Dataran struktural lipatan berombak-bergelombang bermaterial batuan sedimen non karbonat | 2 | 2 | 2 | 3 | 4 | 4 |
| **21** | Dataran struktural lipatan berombak-bergelombang bermaterial campuran batuan sedimen karbonat dan non karbonat | 2 | 2 | 2 | 3 | 4 | 4 |
| **22** | Dataran struktural plutonik berombak-bergelombang bermaterial batuan beku dalam | 2 | 1 | 2 | 2 | 2 | 4 |
| **23** | Dataran vulkanik bermaterial piroklastik | 2 | 4 | 2 | 4 | 5 | 4 |
| **24** | Dataran vulkanik berombak-bergelombang bermaterial batuan beku luar | 2 | 4 | 2 | 2 | 2 | 4 |
| **25** | Dataran vulkanik berombak-bergelombang bermaterial campuran batuan beku luar dan piroklastik | 3 | 4 | 2 | 4 | 4 | 4 |
| **26** | Dataran vulkanik berombak-bergelombang bermaterial piroklastik | 2 | 4 | 2 | 4 | 5 | 4 |
| **27** | Dataran vulkanik kipas bermaterial piroklastik | 4 | 4 | 1 | 4 | 5 | 4 |
| **28** | Lembah sungai bermaterial aluvium | 4 | 5 | 2 | 5 | 5 | 4 |
| **29** | Pegunungan denudasional bermaterial batuan metamorfik | 2 | 1 | 3 | 2 | 2 | 3 |
| **30** | Pegunungan denudasional bermaterial batuan metamorfik (ultrabasa) | 2 | 1 | 3 | 2 | 2 | 3 |
| **31** | Pegunungan denudasional bermaterial batuan sedimen karbonat | 3 | 1 | 3 | 2 | 3 | 3 |
| **32** | Pegunungan denudasional bermaterial batuan sedimen non karbonat | 3 | 1 | 2 | 3 | 4 | 3 |
| **33** | Pegunungan denudasional bermaterial campuran batuan beku luar dan piroklastik | 4 | 2 | 2 | 3 | 4 | 4 |
| **34** | Pegunungan denudasional bermaterial campuran batuan sedimen karbonat dan non karbonat | 3 | 2 | 2 | 3 | 4 | 4 |
| **35** | Pegunungan glasial bermaterial batuan metamorfik | 2 | 1 | 3 | 3 | 1 | 3 |
| **36** | Pegunungan glasial bermaterial batuan sedimen karbonat | 2 | 1 | 3 | 3 | 1 | 3 |
| **37** | Pegunungan kerucut vulkanik bermaterial batuan beku luar | 2 | 2 | 3 | 2 | 2 | 3 |
| **38** | Pegunungan kerucut vulkanik bermaterial campuran batuan beku luar dan piroklastik | 4 | 2 | 2 | 4 | 4 | 3 |
| **39** | Pegunungan kerucut vulkanik bermaterial piroklastik | 4 | 2 | 2 | 4 | 4 | 3 |
| **40** | Pegunungan kerucut vulkanik lereng atas bermaterial campuran batuan beku luar dan piroklastik | 3 | 2 | 2 | 3 | 4 | 3 |
| **41** | Pegunungan kerucut vulkanik lereng bawah bermaterial batuan beku luar | 4 | 2 | 3 | 3 | 3 | 3 |
| **42** | Pegunungan kerucut vulkanik lereng bawah bermaterial campuran batuan beku luar dan piroklastik | 3 | 2 | 2 | 4 | 4 | 3 |
| **43** | Pegunungan kerucut vulkanik lereng bawah bermaterial piroklastik | 3 | 2 | 2 | 4 | 4 | 4 |
| **44** | Pegunungan kerucut vulkanik lereng puncak bermaterial campuran batuan beku luar dan piroklastik | 3 | 2 | 2 | 3 | 4 | 4 |
| **45** | Pegunungan kerucut vulkanik lereng tengah bermaterial campuran batuan beku luar dan piroklastik | 3 | 2 | 2 | 4 | 4 | 4 |
| **46** | Pegunungan solusional karst bermaterial batuan sedimen karbonat | 5 | 2 | 2 | 2 | 3 | 3 |
| **47** | Pegunungan struktural lipatan bermaterial batuan metamorfik | 2 | 1 | 2 | 3 | 2 | 3 |
| **48** | Pegunungan struktural lipatan bermaterial batuan sedimen karbonat | 3 | 1 | 3 | 3 | 3 | 3 |
| **49** | Pegunungan struktural lipatan bermaterial batuan sedimen non karbonat | 3 | 2 | 2 | 3 | 4 | 3 |
| **50** | Pegunungan struktural lipatan bermaterial campuran batuan sedimen karbonat dan non karbonat | 3 | 2 | 2 | 3 | 4 | 4 |
| **51** | Pegunungan struktural patahan bermaterial batuan metamorfik | 3 | 1 | 3 | 2 | 2 | 3 |
| **52** | Pegunungan struktural plutonik bermaterial batuan beku dalam | 3 | 1 | 5 | 2 | 2 | 3 |
| **53** | Pegunungan vulkanik bermaterial batuan beku luar | 2 | 2 | 2 | 2 | 2 | 3 |
| **54** | Pegunungan vulkanik bermaterial campuran batuan beku luar dan piroklastik | 4 | 2 | 2 | 3 | 4 | 3 |
| **55** | Pegunungan vulkanik bermaterial piroklastik | 4 | 2 | 2 | 3 | 4 | 3 |
| **56** | Pegunungan vulkanik lereng bawah bermaterial piroklastik | 4 | 2 | 2 | 4 | 4 | 3 |
| **57** | Perbukitan denudasional bermaterial batuan metamorfik | 3 | 1 | 3 | 2 | 2 | 3 |
| **58** | Perbukitan denudasional bermaterial batuan metamorfik (ultrabasa) | 3 | 1 | 3 | 2 | 2 | 3 |
| **59** | Perbukitan denudasional bermaterial batuan sedimen karbonat | 3 | 2 | 2 | 2 | 3 | 3 |
| **60** | Perbukitan denudasional bermaterial batuan sedimen non karbonat | 3 | 2 | 2 | 3 | 4 | 3 |
| **61** | Perbukitan denudasional bermaterial campuran batuan beku luar dan piroklastik | 4 | 2 | 2 | 3 | 4 | 3 |
| **62** | Perbukitan denudasional bermaterial campuran batuan sedimen karbonat dan non karbonat | 3 | 2 | 2 | 3 | 4 | 3 |
| **63** | Perbukitan denudasional bermaterial piroklastik | 4 | 2 | 3 | 4 | 4 | 3 |
| **64** | Perbukitan glasial bermaterial batuan sedimen karbonat | 2 | 1 | 5 | 3 | 1 | 3 |
| **65** | Perbukitan kerucut vulkanik bermaterial batuan beku luar | 3 | 2 | 2 | 2 | 3 | 3 |
| **66** | Perbukitan kerucut vulkanik bermaterial campuran batuan beku luar dan piroklastik | 4 | 2 | 2 | 4 | 4 | 4 |
| **67** | Perbukitan kerucut vulkanik bermaterial piroklastik | 4 | 2 | 1 | 4 | 4 | 4 |
| **68** | Perbukitan kerucut vulkanik parasiter bermaterial batuan beku luar | 3 | 2 | 2 | 2 | 2 | 4 |
| **69** | Perbukitan kerucut vulkanik parasiter bermaterial campuran batuan beku luar dan piroklastik | 4 | 2 | 2 | 3 | 4 | 3 |
| **70** | Perbukitan solusional karst bermaterial batuan sedimen karbonat | 5 | 3 | 2 | 2 | 2 | 3 |
| **71** | Perbukitan struktural lipatan bermaterial batuan metamorfik | 3 | 1 | 2 | 2 | 2 | 3 |
| **72** | Perbukitan struktural lipatan bermaterial batuan sedimen karbonat | 3 | 2 | 2 | 2 | 2 | 3 |
| **73** | Perbukitan struktural lipatan bermaterial batuan sedimen non karbonat | 3 | 2 | 2 | 3 | 3 | 4 |
| **74** | Perbukitan struktural lipatan bermaterial campuran batuan sedimen karbonat dan non karbonat | 3 | 2 | 2 | 3 | 3 | 4 |
| **75** | Perbukitan struktural patahan bermaterial batuan metamorfik | 3 | 1 | 5 | 2 | 2 | 3 |
| **76** | Perbukitan struktural plutonik bermaterial batuan beku dalam | 3 | 1 | 2 | 1 | 2 | 3 |
| **77** | Perbukitan vulkanik bermaterial batuan beku luar | 3 | 2 | 2 | 2 | 2 | 3 |
| **78** | Perbukitan vulkanik bermaterial campuran batuan beku luar dan piroklastik | 4 | 3 | 2 | 3 | 4 | 4 |
| **79** | Perbukitan vulkanik bermaterial piroklastik | 4 | 2 | 2 | 4 | 4 | 4 |
| **80** | Perbukitan vulkanik kubah lava bermaterial batuan beku luar | 1 | 2 | 3 | 2 | 2 | 3 |
| **81** | Perbukitan vulkanik lereng bawah bermaterial piroklastik | 4 | 3 | 1 | 4 | 4 | 4 |
| **82** | Perbukitan vulkanik lereng tengah bermaterial piroklastik | 4 | 3 | 1 | 4 | 4 | 4 |
| **83** | Tebing kaldera bermaterial campuran batuan beku luar dan piroklastik | 1 | 1 | 2 | 1 | 2 | 3 |

---
## 5. Tabel Lengkap Skor Karakteristik Vegetasi Alami (KVA - 94 Kelas)

| Value | Karakteristik Vegetasi Alami (KVA_250) | PGA | PHK | PPK | PYA | PGN | PKU |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | Vegetasi hutan batuan ultrabasa pamah | 3 | 3 | 2 | 2 | 2 | 4 |
| **2** | Vegetasi hutan batuan ultrabasa pamah monsun | 2 | 2 | 1 | 1 | 2 | 4 |
| **3** | Vegetasi hutan batuan ultrabasa pamah monsun malar hijau | 3 | 3 | 2 | 2 | 2 | 4 |
| **4** | Vegetasi hutan batuan ultrabasa pamah monsun merangas | 2 | 2 | 1 | 1 | 2 | 4 |
| **5** | Vegetasi hutan batuan ultrabasa pegunungan | 2 | 1 | 1 | 2 | 2 | 4 |
| **6** | Vegetasi hutan batuan ultrabasa pegunungan alpin | 2 | 1 | 1 | 1 | 1 | 4 |
| **7** | Vegetasi hutan batuan ultrabasa pegunungan atas | 2 | 1 | 1 | 2 | 1 | 4 |
| **8** | Vegetasi hutan batuan ultrabasa pegunungan atas monsun | 2 | 1 | 1 | 1 | 1 | 4 |
| **9** | Vegetasi hutan batuan ultrabasa pegunungan bawah | 2 | 1 | 1 | 3 | 2 | 4 |
| **10** | Vegetasi hutan batuan ultrabasa pegunungan bawah monsun | 2 | 1 | 1 | 2 | 2 | 4 |
| **11** | Vegetasi hutan batuan ultrabasa pegunungan subalpin | 2 | 1 | 1 | 1 | 1 | 4 |
| **12** | Vegetasi hutan batugamping pamah | 4 | 2 | 2 | 2 | 3 | 4 |
| **13** | Vegetasi hutan batugamping pamah monsun | 3 | 3 | 1 | 2 | 2 | 4 |
| **14** | Vegetasi hutan batugamping pamah monsun malar hijau | 3 | 3 | 2 | 3 | 3 | 4 |
| **15** | Vegetasi hutan batugamping pamah monsun merangas | 3 | 2 | 1 | 2 | 2 | 4 |
| **16** | Vegetasi hutan batugamping pamah monsun merangas pada bentangalam karst | 4 | 3 | 2 | 3 | 2 | 4 |
| **17** | Vegetasi hutan batugamping pamah monsun pada bentangalam karst | 4 | 3 | 2 | 2 | 3 | 4 |
| **18** | Vegetasi hutan batugamping pamah pada bentangalam karst | 4 | 3 | 4 | 3 | 3 | 4 |
| **19** | Vegetasi hutan batugamping pegunungan alpin | 3 | 1 | 1 | 2 | 1 | 4 |
| **20** | Vegetasi hutan batugamping pegunungan atas | 3 | 1 | 1 | 2 | 1 | 4 |
| **21** | Vegetasi hutan batugamping pegunungan atas monsun pada bentangalam karst | 4 | 2 | 2 | 2 | 2 | 4 |
| **22** | Vegetasi hutan batugamping pegunungan atas pada bentangalam karst | 4 | 1 | 2 | 3 | 1 | 4 |
| **23** | Vegetasi hutan batugamping pegunungan bawah | 3 | 1 | 4 | 3 | 3 | 4 |
| **24** | Vegetasi hutan batugamping pegunungan bawah monsun | 2 | 1 | 2 | 2 | 2 | 4 |
| **25** | Vegetasi hutan batugamping pegunungan bawah monsun pada bentangalam karst | 4 | 2 | 2 | 3 | 2 | 4 |
| **26** | Vegetasi hutan batugamping pegunungan bawah pada bentangalam karst | 4 | 2 | 2 | 3 | 3 | 4 |
| **27** | Vegetasi hutan batugamping pegunungan monsun pada bentangalam karst | 4 | 2 | 2 | 2 | 2 | 4 |
| **28** | Vegetasi hutan batugamping pegunungan pada bentangalam karst | 4 | 2 | 2 | 3 | 3 | 4 |
| **29** | Vegetasi hutan batugamping pegunungan subalpin | 3 | 1 | 1 | 1 | 1 | 4 |
| **30** | Vegetasi hutan batugamping pegunungan subalpin monsun pada bentangalam karst | 4 | 1 | 1 | 1 | 1 | 4 |
| **31** | Vegetasi hutan batugamping pegunungan subalpin pada bentangalam karst | 4 | 1 | 1 | 2 | 1 | 4 |
| **32** | Vegetasi hutan danau | 4 | 4 | 4 | 3 | 3 | 4 |
| **33** | Vegetasi hutan danau gambut | 4 | 3 | 4 | 2 | 2 | 5 |
| **34** | Vegetasi hutan dipterokarpa pamah | 5 | 5 | 5 | 4 | 5 | 5 |
| **35** | Vegetasi hutan gambut | 4 | 3 | 4 | 2 | 3 | 5 |
| **36** | Vegetasi hutan kerangas | 3 | 3 | 2 | 2 | 2 | 4 |
| **37** | Vegetasi hutan kerangas monsun | 2 | 2 | 1 | 1 | 2 | 5 |
| **38** | Vegetasi hutan pamah (non dipterokarpa) | 5 | 5 | 5 | 4 | 5 | 4 |
| **39** | Vegetasi hutan pamah monsun malar hijau | 4 | 4 | 2 | 3 | 3 | 5 |
| **40** | Vegetasi hutan pamah monsun merangas | 4 | 3 | 1 | 2 | 2 | 4 |
| **41** | Vegetasi hutan pantai | 4 | 4 | 2 | 3 | 3 | 4 |
| **42** | Vegetasi hutan pantai monsun | 4 | 2 | 1 | 2 | 2 | 5 |
| **43** | Vegetasi hutan pegunungan atas | 2 | 1 | 2 | 3 | 3 | 4 |
| **44** | Vegetasi hutan pegunungan atas monsun | 3 | 1 | 1 | 2 | 2 | 5 |
| **45** | Vegetasi hutan pegunungan bawah | 2 | 2 | 4 | 3 | 4 | 4 |
| **46** | Vegetasi hutan pegunungan bawah monsun | 3 | 1 | 1 | 2 | 2 | 4 |
| **47** | Vegetasi hutan pegunungan monsun merangas pada bukit tinggi | 2 | 1 | 1 | 2 | 2 | 5 |
| **48** | Vegetasi hutan pegunungan subalpin | 2 | 1 | 1 | 1 | 1 | 5 |
| **49** | Vegetasi hutan pegunungan subalpin monsun | 2 | 1 | 1 | 1 | 1 | 4 |
| **50** | Vegetasi hutan rawa air payau | 2 | 2 | 2 | 2 | 3 | 5 |
| **51** | Vegetasi hutan rawa air payau monsun pada bentangalam karst | 3 | 2 | 2 | 3 | 2 | 5 |
| **52** | Vegetasi hutan rawa air payau pada bentangalam karst | 4 | 2 | 2 | 3 | 3 | 5 |
| **53** | Vegetasi hutan rawa air tawar | 4 | 4 | 4 | 3 | 5 | 5 |
| **54** | Vegetasi hutan rawa air tawar monsun | 4 | 3 | 2 | 2 | 4 | 5 |
| **55** | Vegetasi hutan rawa air tawar monsun pada bentangalam karst | 4 | 2 | 2 | 3 | 2 | 5 |
| **56** | Vegetasi hutan rawa air tawar pada bentangalam karst | 4 | 3 | 4 | 3 | 4 | 5 |
| **57** | Vegetasi hutan tepian sungai air payau | 2 | 2 | 1 | 2 | 2 | 4 |
| **58** | Vegetasi hutan tepian sungai air tawar | 4 | 2 | 2 | 3 | 3 | 5 |
| **59** | Vegetasi hutan tepian sungai air tawar monsun malar hijau | 4 | 3 | 2 | 3 | 3 | 5 |
| **60** | Vegetasi litoral | 1 | 1 | 1 | 1 | 4 | 5 |
| **61** | Vegetasi mangrove | 4 | 3 | 5 | 3 | 5 | 5 |
| **62** | Vegetasi mangrove monsun | 4 | 4 | 4 | 2 | 4 | 5 |
| **63** | Vegetasi nipah | 4 | 3 | 4 | 2 | 4 | 4 |
| **64** | Vegetasi nipah monsun | 4 | 3 | 2 | 2 | 3 | 4 |
| **65** | Vegetasi padang rumput lahan kering pamah | 3 | 3 | 2 | 2 | 3 | 3 |
| **66** | Vegetasi padang rumput pamah monsun | 2 | 2 | 1 | 1 | 2 | 4 |
| **67** | Vegetasi padang rumput rawa air payau | 2 | 2 | 1 | 1 | 2 | 4 |
| **68** | Vegetasi padang rumput rawa air payau monsun | 2 | 2 | 1 | 1 | 1 | 4 |
| **69** | Vegetasi padang rumput rawa air tawar | 3 | 3 | 2 | 2 | 3 | 4 |
| **70** | Vegetasi padang rumput rawa air tawar monsun | 3 | 3 | 2 | 2 | 4 | 4 |
| **71** | Vegetasi padang rumput rawa gambut | 3 | 3 | 2 | 1 | 2 | 5 |
| **72** | Vegetasi padang rumput tepian sungai air payau | 2 | 2 | 1 | 3 | 3 | 4 |
| **73** | Vegetasi sagu | 3 | 3 | 4 | 3 | 5 | 4 |
| **74** | Vegetasi sagu monsun | 4 | 4 | 2 | 3 | 5 | 4 |
| **75** | Vegetasi salju batugamping pegunungan alpin | 2 | 1 | 1 | 2 | 1 | 5 |
| **76** | Vegetasi savana lahan kering pamah | 2 | 2 | 2 | 2 | 2 | 3 |
| **77** | Vegetasi savana pamah monsun | 3 | 3 | 2 | 2 | 2 | 4 |
| **78** | Vegetasi savana pegunungan monsun | 2 | 1 | 1 | 2 | 2 | 4 |
| **79** | Vegetasi savana rawa air payau | 2 | 2 | 1 | 2 | 2 | 4 |
| **80** | Vegetasi savana rawa air tawar | 3 | 3 | 2 | 3 | 3 | 4 |
| **81** | Vegetasi savana rawa gambut | 3 | 2 | 2 | 2 | 2 | 5 |
| **82** | Vegetasi savana tepian danau | 4 | 3 | 4 | 3 | 3 | 4 |
| **83** | Vegetasi terna rawa air payau | 2 | 2 | 1 | 2 | 3 | 4 |
| **84** | Vegetasi terna rawa air payau monsun | 2 | 2 | 1 | 2 | 2 | 4 |
| **85** | Vegetasi terna rawa air payau monsun pada bentangalam karst | 3 | 2 | 1 | 3 | 2 | 4 |
| **86** | Vegetasi terna rawa air payau pada bentangalam karst | 3 | 2 | 2 | 3 | 3 | 4 |
| **87** | Vegetasi terna rawa air tawar | 3 | 3 | 4 | 3 | 4 | 4 |
| **88** | Vegetasi terna rawa air tawar monsun | 3 | 2 | 2 | 2 | 3 | 4 |
| **89** | Vegetasi terna rawa gambut | 3 | 2 | 2 | 2 | 3 | 5 |
| **90** | Vegetasi terna savana rawa gambut | 2 | 2 | 2 | 2 | 2 | 5 |
| **91** | Vegetasi terna tepian danau | 3 | 2 | 2 | 3 | 3 | 4 |
| **92** | Vegetasi terna tepian danau pegunungan | 4 | 2 | 2 | 3 | 3 | 4 |
| **93** | Vegetasi terna tepian sungai air payau | 3 | 2 | 1 | 2 | 3 | 4 |
| **94** | Vegetasi terna tepian sungai air tawar | 3 | 2 | 2 | 3 | 4 | 4 |
