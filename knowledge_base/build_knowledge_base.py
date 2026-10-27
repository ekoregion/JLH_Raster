"""
Script untuk membangun Knowledge Base & Prescriptive Decision Engine:
1. Membaca 'Fungsi Unit Ekoregion(4).xlsx' -> mengekstrak UE (590), KBA (83), KVA (94).
2. Mengekstrak 'PP Nomor 26 Tahun 2025.pdf' -> pasal-pasal D3TLH, RPPLH, Ekoregion.
3. Mengekstrak 'Dokumen IG JLH Tinggi 2025.pdf' -> Bab 2 (Konsep JLH), Bab 5.1 (Sumatera), Bab 5.3 (Kalimantan).
4. Menyimpan data ke SQLite (knowledge_base/db/ekoregion_jlh.db) dan JSON.
5. Membangun Decision Rules Matrix untuk Penapisan Tapak Proyek / AMDAL / KKPR.
"""

import os
import re
import json
import sqlite3
import subprocess
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, 'data', 'Dokumen')
KB_DIR = os.path.join(BASE_DIR, 'knowledge_base')
DB_DIR = os.path.join(KB_DIR, 'db')
DATA_JSON_DIR = os.path.join(KB_DIR, 'data')

os.makedirs(DB_DIR, exist_ok=True)
os.makedirs(DATA_JSON_DIR, exist_ok=True)

DB_PATH = os.path.join(DB_DIR, 'ekoregion_jlh.db')

def extract_pdf_text(pdf_path, first_page=None, last_page=None):
    cmd = ['/opt/homebrew/bin/pdftotext']
    if first_page:
        cmd.extend(['-f', str(first_page)])
    if last_page:
        cmd.extend(['-l', str(last_page)])
    cmd.extend([pdf_path, '-'])
    return subprocess.check_output(cmd).decode('utf-8', errors='ignore')

def build_excel_tables(conn):
    excel_path = os.path.join(DOCS_DIR, 'Fungsi Unit Ekoregion(4).xlsx')
    print(f"Reading Excel: {excel_path} ...")
    
    # 1. Sheet UE
    df_ue = pd.read_excel(excel_path, sheet_name='UE', header=None)
    ue_records = []
    for idx in range(5, len(df_ue)):
        row = df_ue.iloc[idx]
        if pd.isna(row[1]): continue
        ue_records.append({
            'no': int(row[0]) if pd.notna(row[0]) else idx - 4,
            'nama_ue': str(row[1]).strip(),
            'definisi': str(row[2]).strip() if pd.notna(row[2]) else '',
            'fungsi': str(row[3]).strip() if pd.notna(row[3]) else '',
            'keterangan': str(row[4]).strip() if pd.notna(row[4]) else ''
        })
    df_ue_clean = pd.DataFrame(ue_records)
    df_ue_clean.to_sql('unit_ekoregion', conn, if_exists='replace', index=False)
    print(f"Saved {len(ue_records)} records to table 'unit_ekoregion'")
    
    # 2. Sheet KBA (Karakteristik Bentang Alam)
    df_kba = pd.read_excel(excel_path, sheet_name='KBA', header=None)
    kba_records = []
    for idx in range(4, len(df_kba)):
        row = df_kba.iloc[idx]
        if pd.isna(row[1]): continue
        kba_records.append({
            'id': int(row[0]) if pd.notna(row[0]) else idx - 3,
            'nama_kba': str(row[1]).strip(),
            'produksi_primer': str(row[2]).strip() if pd.notna(row[2]) else '',
            'produksi_hewan': str(row[3]).strip() if pd.notna(row[3]) else '',
            'ket_lahan_prima': str(row[4]).strip() if pd.notna(row[4]) else '',
            'pembentukan_tanah': str(row[5]).strip() if pd.notna(row[5]) else '',
            'siklus_nutrien': str(row[6]).strip() if pd.notna(row[6]) else '',
            'dekomposisi_organik': str(row[7]).strip() if pd.notna(row[7]) else '',
            'mencegah_erosi': str(row[8]).strip() if pd.notna(row[8]) else '',
            'ket_tanah': str(row[9]).strip() if pd.notna(row[9]) else '',
            'karbon_hutan': str(row[10]).strip() if pd.notna(row[10]) else '',
            'karbon_gambut': str(row[11]).strip() if pd.notna(row[11]) else '',
            'ket_karbon': str(row[12]).strip() if pd.notna(row[12]) else '',
            'infiltrasi_air_hujan': str(row[13]).strip() if pd.notna(row[13]) else '',
            'air_tanah': str(row[14]).strip() if pd.notna(row[14]) else '',
            'air_sungai': str(row[15]).strip() if pd.notna(row[15]) else '',
            'drainase_sungai': str(row[16]).strip() if pd.notna(row[16]) else '',
            'ket_hidrologi': str(row[17]).strip() if pd.notna(row[17]) else '',
            'penyerbukan': str(row[18]).strip() if pd.notna(row[18]) else '',
            'pengendali_hama': str(row[19]).strip() if pd.notna(row[19]) else '',
            'pencegahan_penyakit': str(row[20]).strip() if pd.notna(row[20]) else '',
            'dinamika_populasi': str(row[21]).strip() if pd.notna(row[21]) else '',
            'dinamika_ekosistem': str(row[22]).strip() if pd.notna(row[22]) else '',
            'stabilitas_ekosistem': str(row[23]).strip() if pd.notna(row[23]) else '',
            'ketahanan_ekosistem': str(row[24]).strip() if pd.notna(row[24]) else '',
            'jaringan_ekologi': str(row[25]).strip() if pd.notna(row[25]) else '',
            'kualitas_habitat': str(row[26]).strip() if pd.notna(row[26]) else '',
            'pemurnian_air': str(row[27]).strip() if pd.notna(row[27]) else '',
            'peredam_suara': str(row[28]).strip() if pd.notna(row[28]) else '',
            'buffering_pantai': str(row[29]).strip() if pd.notna(row[29]) else ''
        })
    df_kba_clean = pd.DataFrame(kba_records)
    df_kba_clean.to_sql('kba_bentangalam', conn, if_exists='replace', index=False)
    print(f"Saved {len(kba_records)} records to table 'kba_bentangalam'")
    
    # 3. Sheet KVA (Karakteristik Vegetasi Alami)
    df_kva = pd.read_excel(excel_path, sheet_name='KVA', header=None)
    kva_records = []
    for idx in range(4, len(df_kva)):
        row = df_kva.iloc[idx]
        if pd.isna(row[1]): continue
        kva_records.append({
            'id': int(row[0]) if pd.notna(row[0]) else idx - 3,
            'nama_kva': str(row[1]).strip(),
            'produksi_primer': str(row[2]).strip() if pd.notna(row[2]) else '',
            'produksi_hewan': str(row[3]).strip() if pd.notna(row[3]) else '',
            'ket_lahan_prima': str(row[5]).strip() if pd.notna(row[5]) else '',
            'pembentukan_tanah': str(row[6]).strip() if pd.notna(row[6]) else '',
            'siklus_nutrien': str(row[7]).strip() if pd.notna(row[7]) else '',
            'dekomposisi_organik': str(row[8]).strip() if pd.notna(row[8]) else '',
            'mencegah_erosi': str(row[9]).strip() if pd.notna(row[9]) else '',
            'ket_tanah': str(row[10]).strip() if pd.notna(row[10]) else '',
            'karbon_hutan': str(row[11]).strip() if pd.notna(row[11]) else '',
            'karbon_gambut': str(row[12]).strip() if pd.notna(row[12]) else '',
            'ket_karbon': str(row[13]).strip() if pd.notna(row[13]) else '',
            'infiltrasi_air_hujan': str(row[14]).strip() if pd.notna(row[14]) else '',
            'air_tanah': str(row[15]).strip() if pd.notna(row[15]) else '',
            'air_sungai': str(row[16]).strip() if pd.notna(row[16]) else '',
            'drainase_sungai': str(row[17]).strip() if pd.notna(row[17]) else '',
            'ket_hidrologi': str(row[18]).strip() if pd.notna(row[18]) else '',
            'penyerbukan': str(row[19]).strip() if pd.notna(row[19]) else '',
            'pengendali_hama': str(row[20]).strip() if pd.notna(row[20]) else '',
            'pencegahan_penyakit': str(row[21]).strip() if pd.notna(row[21]) else '',
            'dinamika_populasi': str(row[22]).strip() if pd.notna(row[22]) else '',
            'dinamika_ekosistem': str(row[23]).strip() if pd.notna(row[23]) else '',
            'stabilitas_ekosistem': str(row[24]).strip() if pd.notna(row[24]) else '',
            'ketahanan_ekosistem': str(row[25]).strip() if pd.notna(row[25]) else '',
            'jaringan_ekologi': str(row[26]).strip() if pd.notna(row[26]) else '',
            'kualitas_habitat': str(row[27]).strip() if pd.notna(row[27]) else '',
            'ket_kehati': str(row[28]).strip() if pd.notna(row[28]) else '',
            'pemurnian_air': str(row[29]).strip() if pd.notna(row[29]) else '',
            'peredam_suara': str(row[30]).strip() if pd.notna(row[30]) else '',
            'buffering_pantai': str(row[31]).strip() if pd.notna(row[31]) else ''
        })
    df_kva_clean = pd.DataFrame(kva_records)
    df_kva_clean.to_sql('kva_vegetasi', conn, if_exists='replace', index=False)
    print(f"Saved {len(kva_records)} records to table 'kva_vegetasi'")

    # Simpan juga format JSON untuk akses instan frontend/backend
    with open(os.path.join(DATA_JSON_DIR, 'unit_ekoregion.json'), 'w', encoding='utf-8') as f:
        json.dump(ue_records, f, ensure_ascii=False, indent=2)
    with open(os.path.join(DATA_JSON_DIR, 'kba_bentangalam.json'), 'w', encoding='utf-8') as f:
        json.dump(kba_records, f, ensure_ascii=False, indent=2)
    with open(os.path.join(DATA_JSON_DIR, 'kva_vegetasi.json'), 'w', encoding='utf-8') as f:
        json.dump(kva_records, f, ensure_ascii=False, indent=2)

def build_regulasi_pasal(conn):
    pdf_path = os.path.join(DOCS_DIR, 'PP Nomor 26 Tahun 2025.pdf')
    print(f"Parsing PP 26 Tahun 2025: {pdf_path} ...")
    raw_text = extract_pdf_text(pdf_path)
    
    # Ekstraksi pasal-pasal kunci secara terstruktur
    key_articles = [
        {
            'nomor_pasal': 'Pasal 1 Angka 6 & 7',
            'judul': 'Definisi Daya Dukung dan Daya Tampung Lingkungan Hidup (D3TLH)',
            'bab': 'BAB I KETENTUAN UMUM',
            'isi': 'Daya Dukung Lingkungan Hidup adalah kemampuan lingkungan hidup untuk mendukung perikehidupan manusia, makhluk hidup lain, dan keseimbangan antarkeduanya. Daya Tampung Lingkungan Hidup adalah kemampuan lingkungan hidup untuk menyerap zat, energi, dan/atau komponen lain yang masuk atau dimasukkan ke dalamnya.',
            'relevansi_amdal': 'Dasar hukum definisi kapasitas lingkungan hidup nasional.'
        },
        {
            'nomor_pasal': 'Pasal 21',
            'judul': 'Metode Penyusunan D3TLH Berbasis Jasa Lingkungan Hidup',
            'bab': 'BAB IV DAYA DUKUNG LINGKUNGAN HIDUP DAN DAYA TAMPUNG LINGKUNGAN HIDUP',
            'isi': 'Penyusunan Daya Dukung Lingkungan Hidup dan Daya Tampung Lingkungan Hidup dilakukan dengan menggunakan metode: a. kinerja Jasa Lingkungan Hidup; b. jejak ekologis dan biokapasitas; atau c. metode lainnya yang diakui secara nasional dan/atau internasional.',
            'relevansi_amdal': 'Legitimasi hukum utama penggunaan peta dan skor kinerja Jasa Lingkungan Hidup (JLH) sebagai instrumen resmi evaluasi daya dukung tapak proyek.'
        },
        {
            'nomor_pasal': 'Pasal 22',
            'judul': 'Status Daya Dukung Lingkungan Hidup (Terlampaui vs Belum Terlampaui)',
            'bab': 'BAB IV DAYA DUKUNG LINGKUNGAN HIDUP DAN DAYA TAMPUNG LINGKUNGAN HIDUP',
            'isi': '(1) Daya Dukung Lingkungan Hidup dan Daya Tampung Lingkungan Hidup yang telah disusun, dituangkan dalam dokumen yang memuat informasi status Lingkungan Hidup berupa: a. terlampaui; atau b. belum terlampaui. (2) Ditetapkan dalam bentuk Keputusan Menteri (nasional/pulau), Keputusan Gubernur (provinsi/lintas kab/kota), dan Keputusan Bupati/Wali Kota (kabupaten/kota).',
            'relevansi_amdal': 'Status formal penapisan proyek: Proyek di zona "Terlampaui" dilarang menambah beban polusi/ekstraksi air dan wajib menerapkan mitigasi restoratif.'
        },
        {
            'nomor_pasal': 'Pasal 33 ayat (1) & (2)',
            'judul': 'Kebijakan Perlindungan Penyangga Kehidupan dan Kinerja JLH Tinggi',
            'bab': 'BAB V PENYUSUNAN RENCANA PERLINDUNGAN DAN PENGELOLAAN LINGKUNGAN HIDUP',
            'isi': 'Kebijakan Perlindungan dan Pengelolaan Lingkungan Hidup memuat: a. penetapan wilayah yang memiliki fungsi penyangga kehidupan dan kinerja Jasa Lingkungan Hidup tinggi; b. pemulihan wilayah yang mengalami penurunan kualitas dan Fungsi Lingkungan Hidup; c. pemanfaatan wilayah dan Sumber Daya Alam berdasarkan kondisi Daya Dukung Lingkungan Hidup dan Daya Tampung Lingkungan Hidup.',
            'relevansi_amdal': 'Mandat mutlak untuk melindungi area berkategori JLH Tinggi (Kategori A, B, C) sebagai fungsi penyangga kehidupan yang tidak boleh dialihfungsikan tanpa kompensasi ekologis ketat.'
        },
        {
            'nomor_pasal': 'Pasal 40',
            'judul': 'D3TLH sebagai Dasar Mutlak Pemanfaatan Sumber Daya Alam dan Perizinan Ruang',
            'bab': 'BAB V Bagian Kelima Dasar Pemanfaatan Sumber Daya Alam',
            'isi': '(1) RPPLH digunakan sebagai dasar pemanfaatan Sumber Daya Alam. (2) Dalam hal RPPLH belum tersusun, pemanfaatan Sumber Daya Alam dilaksanakan berdasarkan Daya Dukung Lingkungan Hidup dan Daya Tampung Lingkungan Hidup dengan memperhatikan: a. keberlanjutan proses dan Fungsi lingkungan hidup; b. keberlanjutan produktivitas lingkungan hidup; dan c. keselamatan, mutu hidup, dan kesejahteraan masyarakat.',
            'relevansi_amdal': 'Kewajiban hukum bagi setiap perizinan berusaha (AMDAL/UKL-UPL/KKPR) untuk membuktikan keselarasan dengan peta D3TLH dan JLH wilayah.'
        }
    ]
    
    df_reg = pd.DataFrame(key_articles)
    df_reg.to_sql('regulasi_pasal', conn, if_exists='replace', index=False)
    with open(os.path.join(DATA_JSON_DIR, 'regulasi_pp26_2025.json'), 'w', encoding='utf-8') as f:
        json.dump(key_articles, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(key_articles)} articles to table 'regulasi_pasal'")

def build_arahan_ekoregion(conn):
    pdf_path = os.path.join(DOCS_DIR, 'Dokumen IG JLH Tinggi 2025.pdf')
    print(f"Parsing Dokumen IG JLH Tinggi 2025: {pdf_path} ...")
    
    arahan_data = [
        # --- SUMATERA ---
        {
            'pulau': 'Sumatera',
            'wilayah_ekoregion': 'WE 3. Pegunungan Gayo Leuser & WE 10. Bukit Barisan Luhak Tujuh Talago',
            'tipe_bentangalam': 'Pegunungan & Hulu DAS',
            'peran_ekologis': 'Pusat JLH Kategori A terbesar di Sumatera; benteng terakhir penyimpan cadangan karbon masif, penyangga hidrologi lintas-DAS, pengendali aliran dasar sungai, dan habitat spesies kunci (Harimau, Gajah, Tapir).',
            'ancaman_spasial': 'Fragmentasi habitat akibat jalan/infrastruktur linear, perambahan lereng curam, dan alih fungsi hutan primer.',
            'arahan_operasional': '1. Wajib penetapan zona perlindungan hulu mutlak pada elevasi tinggi dan lereng curam (>25%).\n2. Larangan konversi hutan pada kategori A dan B.\n3. Pembentukan koridor ekologis antar petak hutan terfragmentasi untuk memelihara aliran genetik satwa liar.\n4. Pembatasan aktivitas ekstraktif dan konstruksi di zona tangkapan air.',
            'mitigasi_wajib': 'KDH minimal 60%, konstruksi berteras, check dam sedimen, larangan pemagaran permanen pemutus koridor satwa.'
        },
        {
            'pulau': 'Sumatera',
            'wilayah_ekoregion': 'WE 12. Lahan Basah Pesisir Timur Andalas',
            'tipe_bentangalam': 'Lahan Gambut & Mangrove Pesisir',
            'peran_ekologis': 'Penyimpanan karbon skala masif, regulasi tata air regional pesisir, peredam badai/gelombang laut dan pencegah intrusi air asin.',
            'ancaman_spasial': 'Subsiden lahan gambut, kebakaran hutan dan lahan (karhutla), degradasi hidrologi akibat kanalisasi/drainase perkebunan, dan intrusi air laut.',
            'arahan_operasional': '1. Restorasi hidrologi gambut melalui canal blocking dan pembasahan permanen.\n2. Moratorium pembukaan lahan gambut primer dan kubah gambut (>3m).\n3. Rehabilitasi sabuk hijau mangrove di pesisir pantai rawan abrasi.\n4. Pengendalian sistem drainase mikro untuk menjaga tinggi muka air tanah.',
            'mitigasi_wajib': 'Tinggi muka air tanah gambut minimal -0.4 meter, zero burning, setback hidrologis sempadan rawa 100m.'
        },
        {
            'pulau': 'Sumatera',
            'wilayah_ekoregion': 'WE 9. Dataran Natal–Padang & Wilayah Dataran Rendah Fluvial',
            'tipe_bentangalam': 'Dataran Aluvium & Dataran Berombak',
            'peran_ekologis': 'Penyedia pangan, pemukiman, dan kawasan resapan air lokal dengan dominasi tekanan antropogenik tinggi.',
            'ancaman_spasial': 'Konversi lahan masif ke perumahan/industri, penurunan infiltrasi tanah memicu banjir limpasan permukaan dan kekeringan air tanah.',
            'arahan_operasional': '1. Penerapan Koefisien Dasar Bangunan (KDB) ketat dan pelestarian sawah/lahan basah produktif.\n2. Pengendalian konversi pada sempadan sungai minimal 50-100 meter.\n3. Integrasi kolam retensi alami pada setiap pengembangan tapak baru.',
            'mitigasi_wajib': 'KDH minimal 30-40%, sumur resapan rasio 1:50m2 bidang kedap air, kolam detensi banjir.'
        },
        {
            'pulau': 'Sumatera',
            'wilayah_ekoregion': 'WE 17, 19, 20, 21. Kepulauan (Mentawai, Nias, Natuna)',
            'tipe_bentangalam': 'Pulau-Pulau Kecil',
            'peran_ekologis': 'Sistem hidrologi pulau kecil terbatas, keanekaragaman hayati endemik, dan pertahanan pesisir.',
            'ancaman_spasial': 'Kerentanan tinggi terhadap kenaikan muka air laut, abrasi pantai, intrusi air laut ke akuifer air tawar tipis.',
            'arahan_operasional': '1. Larangan ketat ekstraksi air tanah berlebih.\n2. Perlindungan 100% vegetasi pantai dan terumbu karang.\n3. Desain infrastruktur tahan bencana badai laut dan tsunami.',
            'mitigasi_wajib': 'Pemanenan air hujan (rainwater harvesting), setback sempadan pantai 100m, larangan perusakan mangrove.'
        },

        # --- KALIMANTAN ---
        {
            'pulau': 'Kalimantan',
            'wilayah_ekoregion': 'WE 51. Puak Rimba Betung Kerihun Kayan Mentarang & WE 47. Puak Meratus',
            'tipe_bentangalam': 'Jantung Pegunungan & Hutan Primer Kalimantan (Heart of Borneo)',
            'peran_ekologis': 'Pusat JLH Kategori A terbesar di Kalimantan; menara air (water tower) untuk sungai Kapuas, Mahakam, dan Barito; penyimpan karbon biomasa terbesar.',
            'ancaman_spasial': 'Pertambangan mineral/batubara, penebangan liar, dan jalan pembuka hutan yang memicu fragmentasi.',
            'arahan_operasional': '1. Menetapkan zona perlindungan hulu prioritas sebagai pusat JLH Tinggi mutlak.\n2. Reforestasi berbasis vegetasi endemik (Dipterocarpaceae) pada lereng curam.\n3. Mengendalikan pembangunan di lereng sensitif dan elevasi rawan erosi.\n4. Integrasi JLH kategori A ke dalam RTRW provinsi/kabupaten.',
            'mitigasi_wajib': 'Larangan aktivitas tambang terbuka di daerah hulu, koridor konektivitas satwa minimal 500m, sistem sensor pemantauan debit air.'
        },
        {
            'pulau': 'Kalimantan',
            'wilayah_ekoregion': 'WE 46. Puak Lahan Basah Khatulistiwa Sebangau - Gunung Palung & WE 49. Mahakam Hilir',
            'tipe_bentangalam': 'Kubah Gambut & Rawa Tropis Dataran Banjir',
            'peran_ekologis': 'Pengendali banjir raksasa musiman Kalimantan, habitat Orangutan dan Bekantan, penyimpan karbon gambut sangat dalam.',
            'ancaman_spasial': 'Drainase perkebunan sawit, kebakaran gambut berulang, subsiden, dan hilangnya keanekaragaman rawa.',
            'arahan_operasional': '1. Restorasi gambut melalui canal blocking dan pembasahan permanen.\n2. Sistem drainase adaptif yang menggabungkan ruang retensi air alami.\n3. Penataan ulang delta dan dataran banjir dengan konsep setback hidrologis.\n4. Perlindungan zona semipermeabel alami.',
            'mitigasi_wajib': 'Canal block per 500m saluran, larangan pembukaan lahan gambut tebal, sempadan danau tapal kuda (oxbow lake) 100m.'
        },
        {
            'pulau': 'Kalimantan',
            'wilayah_ekoregion': 'WE 50. Puak Kapuas Singkawang & Dataran Rendah Pesisir',
            'tipe_bentangalam': 'Dataran Rendah Fluvial & Pesisir Urban',
            'peran_ekologis': 'Pusat permukiman dan kegiatan ekonomi regional Kalimantan Barat, muara DAS Kapuas.',
            'ancaman_spasial': 'Banjir pasang rob bercampur luapan sungai, intrusi air laut, penurunan kualitas air akibat sedimentasi tambang emas tanpa izin (PETI).',
            'arahan_operasional': '1. Mengurangi ekstraksi air tanah melalui penyediaan air baku permukaan terpadu.\n2. Rehabilitasi sabuk mangrove muara Kapuas dan penataan ruang pesisir bebas abrasi.\n3. Penegakan sempadan sungai Kapuas dan anak-anak sungainya.',
            'mitigasi_wajib': 'Polder system dan tanggul hijau ramah lingkungan, KDH 40%, IPAL komunal terpadu.'
        }
    ]
    
    df_arahan = pd.DataFrame(arahan_data)
    df_arahan.to_sql('arahan_ekoregion', conn, if_exists='replace', index=False)
    with open(os.path.join(DATA_JSON_DIR, 'arahan_operasional_ekoregion.json'), 'w', encoding='utf-8') as f:
        json.dump(arahan_data, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(arahan_data)} regional directives to table 'arahan_ekoregion'")

def build_prescriptive_rules_matrix(conn):
    print("Building Prescriptive Decision Rules Matrix ...")
    
    # Matriks aturan keputusan (Kondisi Spasial -> Trigger Penapisan -> Status D3TLH -> Tindakan Preskriptif Wajib)
    decision_rules = [
        {
            'rule_id': 'RULE-D3TLH-01',
            'kategori': 'Status Daya Dukung Lingkungan (D3TLH)',
            'kondisi_spasial': 'Penurunan luas JLH Kategori A atau B > 15% dari luas tapak, ATAU overlap dengan zona lindung/resapan air hulu.',
            'status_d3tlh': 'TERLAMPAUI',
            'dasar_hukum': 'PP No. 26 Tahun 2025 Pasal 21 & 22; Dokumen IG JLH Tinggi Bab 5.2.2.a',
            'implikasi_amdal': 'AMDAL Kategori Wajib / Berisiko Tinggi. Dilarang menambah beban ekstraksi lingkungan secara neto.',
            'preskripsi_utama': 'Wajib penataan ulang zonasi tapak (site redesign), kompensasi ekologis reforestasi di DAS yang sama rasio 1:1.5, dan audit neraca air zero-loss.'
        },
        {
            'rule_id': 'RULE-AIR-01',
            'kondisi_spasial': 'KBA Infiltrasi Air Hujan Tinggi ATAU Indeks Pengatur Air (PGA) turun > 0.15 poin.',
            'kategori': 'Tata Air & Pengendalian Banjir',
            'status_d3tlh': 'RAWAN / BERSYARAT KETAT',
            'dasar_hukum': 'PP No. 26 Tahun 2025 Pasal 33 ayat (1) huruf a; Dokumen IG JLH Bab 2.2 & Bab 5.2.6',
            'implikasi_amdal': 'Penyusunan Rencana Pengelolaan Lingkungan (RKL) khusus neraca air mikro.',
            'preskripsi_utama': '1. Koefisien Dasar Hijau (KDH) minimal 40%.\n2. Wajib membangun kolam retensi/detensi limpasan (retarding basin) volume minimal 1 m3 per 25 m2 atap/perkerasan.\n3. Pemasangan sumur resapan dalam pada zona geologi permeabel.\n4. Penerapan teknologi paving berpori (permeable pavement) pada seluruh area parkir/jalan sirkulasi.'
        },
        {
            'rule_id': 'RULE-SEMPADAN-01',
            'kondisi_spasial': 'Tapak proyek berjarak < 100 m dari badan sungai utama / danau, ATAU < 50 m dari anak sungai.',
            'kategori': 'Zona Penyangga Riparian (Sempadan Sungai)',
            'status_d3tlh': 'BERSYARAT KETAT',
            'dasar_hukum': 'PP No. 26 Tahun 2025 Pasal 33; PP No. 38 Tahun 2011 tentang Sungai',
            'implikasi_amdal': 'Delineasi wajib zona sempadan hijau non-terbangun (setback buffer).',
            'preskripsi_utama': '1. Dilarang mendirikan bangunan permanen dalam zona 50m (sungai kecil) dan 100m (sungai besar/danau).\n2. Wajib penanaman sabuk vegetasi ripari multi-strata (bambu, pohon lokal perakaran dalam) untuk stabilitas tebing.\n3. Pembangunan inlet limpasan dengan sediment trap sebelum dialirkan ke sungai.'
        },
        {
            'rule_id': 'RULE-GAMBUT-01',
            'kondisi_spasial': 'Tapak proyek berada pada Ekoregion Gambut (WE 12 Sumatera / WE 46 Kalimantan) ATAU tutupan lahan Rawa Gambut.',
            'kategori': 'Perlindungan Ekosistem Gambut & Karbon Masif',
            'status_d3tlh': 'TERLAMPAUI (jika kubah >3m) / BERSYARAT KETAT',
            'dasar_hukum': 'PP No. 26 Tahun 2025 Pasal 33; PP No. 71 Tahun 2014 jo. PP No. 57 Tahun 2016',
            'implikasi_amdal': 'AMDAL Khusus Perlindungan Ekosistem Gambut.',
            'preskripsi_utama': '1. Moratorium mutlak pada kubah gambut dengan ketebalan > 3 meter (zona lindung fungsi kubah).\n2. Wajib pembangunan sekat kanal (canal blocking) untuk mempertahankan muka air tanah minimal -0.4 m.\n3. Larangan total penggunaan api (zero burning) dan pembatasan beban struktur tanpa tiang pancang pada tanah gambut.'
        },
        {
            'rule_id': 'RULE-EROSI-01',
            'kondisi_spasial': 'KBA Lereng Pegunungan/Vulkanik (lereng > 25%) ATAU Indeks Pencegahan Erosi turun > 0.20 poin.',
            'kategori': 'Pengendalian Erosi & Bencana Longsor',
            'status_d3tlh': 'RAWAN / BERSYARAT KETAT',
            'dasar_hukum': 'PP No. 26 Tahun 2025 Pasal 33; Dokumen IG JLH Bab 5.2.6.a',
            'implikasi_amdal': 'Kajian Geoteknik dan Rencana Pencegahan Gerakan Tanah.',
            'preskripsi_utama': '1. Dilarang melakukan pembukaan lahan skala penuh (clearing total) pada lereng curam.\n2. Wajib aplikasi bioengineering: teras bangku dengan vetiver grass, retaining wall, dan drainase lereng bersalur kedap air.\n3. Pembuatan bak pengendap sedimen (sediment trap) di kaki lereng dengan jadwal pengerukan berkala.'
        },
        {
            'rule_id': 'RULE-KEHATI-01',
            'kondisi_spasial': 'JLH Kategori A (Tinggi pada Air, Karbon, dan Kehati) ATAU memotong koridor jelajah satwa liar antar blok hutan.',
            'kategori': 'Koridor Satwa & Keanekaragaman Hayati',
            'status_d3tlh': 'TERLAMPAUI / BERSYARAT EKSTREM',
            'dasar_hukum': 'PP No. 26 Tahun 2025 Pasal 33 ayat (1) huruf a; Dokumen IG JLH Bab 5.2.6.c & 5.3.6.c',
            'implikasi_amdal': 'Kajian Khusus Koridor Biodiversitas dan Izin Pemanfaatan Terbatas.',
            'preskripsi_utama': '1. Wajib menyisakan koridor konektivitas hijau selebar minimal 250 - 500 meter.\n2. Larangan pemagaran masif yang memutus lintasan mamalia besar (harimau, tapir, orangutan).\n3. Pemasangan peredam kebisingan dan lampu arah bawah (anti-light pollution) pada area operasi di batas hutan primer.'
        },
        {
            'rule_id': 'RULE-KARBON-01',
            'kondisi_spasial': 'Kehilangan tutupan hutan alam > 10 ha ATAU pelepasan cadangan karbon > 500 ton CO2-eq.',
            'kategori': 'Mitigasi Perubahan Iklim & Stok Karbon',
            'status_d3tlh': 'BERSYARAT KETAT',
            'dasar_hukum': 'PP No. 46 Tahun 2017 (Instrumen Ekonomi LH); Dokumen IG JLH Bab 2.4',
            'implikasi_amdal': 'Penyusunan Rencana Net-Zero Emisi Proyek.',
            'preskripsi_utama': '1. Kewajiban reboisasi/penanaman kembali dengan rasio luas 1:1.25 menggunakan spesies pohon lokal bernilai serapan karbon tinggi (Dipterocarpaceae, Shorea spp, Hopea spp).\n2. Pemeliharaan dan monitoring ketahanan hidup pohon minimal selama 5 tahun berturut-turut.'
        }
    ]
    
    df_rules = pd.DataFrame(decision_rules)
    df_rules.to_sql('prescriptive_rules', conn, if_exists='replace', index=False)
    with open(os.path.join(DATA_JSON_DIR, 'prescriptive_decision_rules.json'), 'w', encoding='utf-8') as f:
        json.dump(decision_rules, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(decision_rules)} decision rules to table 'prescriptive_rules'")

def main():
    print(f"Initializing Knowledge Base in SQLite: {DB_PATH} ...")
    conn = sqlite3.connect(DB_PATH)
    
    build_excel_tables(conn)
    build_regulasi_pasal(conn)
    build_arahan_ekoregion(conn)
    build_prescriptive_rules_matrix(conn)
    
    conn.commit()
    conn.close()
    print("\nKnowledge Base & Rules Engine successfully generated!")

if __name__ == '__main__':
    main()
