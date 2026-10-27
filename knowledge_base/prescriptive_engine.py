"""
Prescriptive Decision Engine for Spatial Decision Support System (SDSS).
Menggabungkan:
1. Deterministic Rule Engine (PP 26/2025, KBA/KVA/UE Matrix)
2. Contextual Document Directives (Dokumen IG JLH Tinggi 2025 Bab 5)
3. Quantitative Zonal Stats Thresholds
"""

import os
import sqlite3
import json
from typing import Dict, Any, List

class PrescriptiveEngine:
    def __init__(self, db_path: str = None):
        if db_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(base_dir, 'db', 'ekoregion_jlh.db')
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def lookup_ue(self, nama_ue: str) -> Dict[str, Any]:
        """Lookup Unit Ekoregion by partial name or keyword."""
        conn = self._get_connection()
        c = conn.cursor()
        c.execute("""
            SELECT no, nama_ue, definisi, fungsi, keterangan 
            FROM unit_ekoregion 
            WHERE nama_ue LIKE ? LIMIT 1
        """, (f"%{nama_ue}%",))
        row = c.fetchone()
        conn.close()
        if row:
            return {
                "id": row[0],
                "nama_ue": row[1],
                "definisi": row[2],
                "fungsi": row[3],
                "keterangan": row[4]
            }
        return {}

    def lookup_kba(self, kba_keyword: str) -> Dict[str, Any]:
        """Lookup Bentang Alam (KBA) by keyword."""
        conn = self._get_connection()
        c = conn.cursor()
        c.execute("""
            SELECT id, nama_kba, produksi_primer, produksi_hewan, ket_lahan_prima,
                   pembentukan_tanah, mencegah_erosi, ket_tanah, karbon_hutan, 
                   karbon_gambut, infiltrasi_air_hujan, air_tanah, air_sungai,
                   ket_hidrologi, kualitas_habitat, ket_karbon
            FROM kba_bentangalam 
            WHERE nama_kba LIKE ? LIMIT 1
        """, (f"%{kba_keyword}%",))
        row = c.fetchone()
        conn.close()
        if row:
            return {
                "id": row[0],
                "nama_kba": row[1],
                "produksi_primer": row[2],
                "produksi_hewan": row[3],
                "ket_lahan_prima": row[4],
                "pembentukan_tanah": row[5],
                "mencegah_erosi": row[6],
                "ket_tanah": row[7],
                "karbon_hutan": row[8],
                "karbon_gambut": row[9],
                "infiltrasi_air_hujan": row[10],
                "air_tanah": row[11],
                "air_sungai": row[12],
                "ket_hidrologi": row[13],
                "kualitas_habitat": row[14],
                "ket_karbon": row[15]
            }
        return {}

    def lookup_arahan_ekoregion(self, pulau: str, tipe_bentang: str = None) -> List[Dict[str, Any]]:
        """Mengambil arahan operasional resmi KLH berdasarkan pulau & tipe bentangalam."""
        conn = self._get_connection()
        c = conn.cursor()
        query = "SELECT pulau, wilayah_ekoregion, tipe_bentangalam, peran_ekologis, ancaman_spasial, arahan_operasional, mitigasi_wajib FROM arahan_ekoregion WHERE pulau LIKE ?"
        params = [f"%{pulau}%"]
        if tipe_bentang:
            query += " AND tipe_bentangalam LIKE ?"
            params.append(f"%{tipe_bentang}%")
        
        c.execute(query, tuple(params))
        rows = c.fetchall()
        conn.close()
        
        results = []
        for r in rows:
            results.append({
                "pulau": r[0],
                "wilayah_ekoregion": r[1],
                "tipe_bentangalam": r[2],
                "peran_ekologis": r[3],
                "ancaman_spasial": r[4],
                "arahan_operasional": r[5],
                "mitigasi_wajib": r[6]
            })
        return results

    def evaluate_site(self, assessment_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mengevaluasi tapak proyek berdasarkan metrik spasial, aturan PP 26/2025,
        dan arahan Dokumen IG JLH Tinggi 2025.
        
        Parameter assessment_input:
        - pulau: 'Sumatera' | 'Kalimantan'
        - provinsi: str
        - nama_kba: str (opsional, misal 'Pegunungan Vulkanik', 'Dataran Aluvium')
        - nama_ue: str (opsional)
        - luas_tapak_ha: float
        - jenis_kegiatan: str
        - pct_jlh_tinggi: float (% luas tapak yang berada di JLH Tinggi)
        - kategori_jlh: 'A' | 'B' | 'C' | 'Tidak Tinggi'
        - delta_pga: float (perubahan indeks pengatur air, misal -0.20)
        - delta_tta: float (perubahan indeks air tanah, misal -0.15)
        - delta_erosi: float (perubahan indeks pencegahan erosi, misal -0.25)
        - delta_karbon: float (perubahan indeks karbon, misal -0.30)
        - jarak_sungai_m: float
        - kelerengan_pct: float
        - is_gambut: bool
        """
        pulau = assessment_input.get('pulau', 'Sumatera')
        provinsi = assessment_input.get('provinsi', 'Sumatera Barat')
        luas_ha = assessment_input.get('luas_tapak_ha', 10.0)
        kegiatan = assessment_input.get('jenis_kegiatan', 'Pembangunan Infrastruktur / Kawasan')
        pct_jlh_tinggi = assessment_input.get('pct_jlh_tinggi', 0.0)
        kategori_jlh = assessment_input.get('kategori_jlh', 'Tidak Tinggi')
        delta_pga = assessment_input.get('delta_pga', 0.0)
        delta_tta = assessment_input.get('delta_tta', 0.0)
        delta_erosi = assessment_input.get('delta_erosi', 0.0)
        delta_karbon = assessment_input.get('delta_karbon', 0.0)
        jarak_sungai = assessment_input.get('jarak_sungai_m', 200.0)
        kelerengan = assessment_input.get('kelerengan_pct', 5.0)
        is_gambut = assessment_input.get('is_gambut', False)

        # 1. Tentukan Status Daya Dukung Lingkungan (D3TLH) sesuai PP 26/2025 Pasal 22
        triggers = []
        is_terlampaui = False
        is_rawan = False

        if kategori_jlh == 'A' and pct_jlh_tinggi > 15.0:
            is_terlampaui = True
            triggers.append(f"Tapak proyek tumpang tindih {pct_jlh_tinggi:.1f}% dengan JLH Kategori A (Tinggi pada Air, Karbon, dan Kehati).")
        elif kategori_jlh == 'B' and pct_jlh_tinggi > 25.0:
            is_terlampaui = True
            triggers.append(f"Tapak proyek tumpang tindih {pct_jlh_tinggi:.1f}% dengan JLH Kategori B (Tinggi pada 2 fungsi esensial).")
        elif is_gambut and pct_jlh_tinggi > 10.0:
            is_terlampaui = True
            triggers.append("Tapak proyek berada pada zona ekosistem gambut dengan fungsi penyimpanan karbon & hidrologi sensitif.")
        
        if delta_pga < -0.20 or delta_tta < -0.20:
            is_rawan = True
            triggers.append(f"Penurunan fungsi regulasi air signifikan (ΔPGA: {delta_pga:.2f}, ΔTTA: {delta_tta:.2f}).")
        
        if delta_erosi < -0.20 or kelerengan > 25.0:
            is_rawan = True
            triggers.append(f"Kerentanan erosi tinggi (Kelerengan: {kelerengan:.1f}%, ΔErosi: {delta_erosi:.2f}).")

        if jarak_sungai < 100.0:
            is_rawan = True
            triggers.append(f"Tapak berjarak {jarak_sungai:.0f} m dari sempadan sungai/badan air (< 100m).")

        if is_terlampaui:
            status_d3tlh = "TERLAMPAUI"
            badge_color = "red"
            status_desc = "Kapasitas daya dukung lingkungan terlampaui. Proyek berisiko tinggi mengganggu fungsi penyangga kehidupan pulau."
        elif is_rawan or pct_jlh_tinggi > 10.0:
            status_d3tlh = "RAWAN / BERSYARAT KETAT"
            badge_color = "orange"
            status_desc = "Daya dukung lingkungan mendekati ambang batas. Proyek wajib menerapkan mitigasi teknis ketat."
        else:
            status_d3tlh = "BELUM TERLAMPAUI"
            badge_color = "green"
            status_desc = "Daya dukung lingkungan masih dalam batas aman dengan pengelolaan standar."

        # 2. Ambil arahan operasional dokumen resmi
        arahan_list = self.lookup_arahan_ekoregion(pulau)
        arahan_terpilih = arahan_list[0] if arahan_list else {}

        # 3. Rumuskan Rekomendasi Preskriptif Terukur
        preskripsi_items = []
        
        # Aturan KDH
        if is_terlampaui:
            kdh_min = 60
        elif is_rawan:
            kdh_min = 40
        else:
            kdh_min = 30
        preskripsi_items.append({
            "kategori": "Koefisien Dasar Hijau (KDH)",
            "spesifikasi": f"KDH minimal {kdh_min}% dari total luas tapak ({luas_ha * kdh_min / 100:.2f} ha wajib berupa ruang terbuka hijau bervegetasi alami).",
            "tujuan": "Mempertahankan kapasitas evapotranspirasi dan infiltrasi air alami."
        })

        # Aturan Tata Air & Retensi Limpasan
        if delta_pga < -0.10 or delta_tta < -0.10 or is_rawan:
            volume_retensi = round(luas_ha * 10000 * (1 - kdh_min/100) * 0.05, 1) # est 50mm hujan ekstrem
            preskripsi_items.append({
                "kategori": "Pengendalian Limpasan & Kolam Retensi",
                "spesifikasi": f"Wajib membangun kolam retensi (retarding basin) berkapasitas minimal {volume_retensi} m³ dan sumur resapan rasio 1 unit per 50 m² atap/perkerasan kedap air.",
                "tujuan": "Zero run-off: mencegah limpasan permukaan berlebih yang memicu banjir hilir."
            })

        # Aturan Sempadan Riparian
        if jarak_sungai < 100.0:
            preskripsi_items.append({
                "kategori": "Zona Penyangga Riparian (Sempadan Sungai)",
                "spesifikasi": f"Delineasi zona sempadan hijau selebar minimal {'100 m' if luas_ha > 20 else '50 m'} dari bibir badan air. Dilarang mendirikan perkerasan/bangunan permanen di zona sempadan.",
                "tujuan": "Menjaga stabilitas bantaran sungai dan mencegah sedimentasi langsung."
            })

        # Aturan Kelerengan & Erosi
        if kelerengan > 15.0 or delta_erosi < -0.15:
            preskripsi_items.append({
                "kategori": "Pengendalian Erosi & Gerakan Tanah",
                "spesifikasi": "Wajib terasering bangku diperkuat tanaman akar wangi (vetiver) dan penahan dinding tanah (retaining wall), dilengkapi bak pengendap sedimen (sediment trap) berkala.",
                "tujuan": "Mencegah longsor lokal dan erosi tanah pada lereng sensitif."
            })

        # Aturan Gambut & Karbon
        if is_gambut:
            preskripsi_items.append({
                "kategori": "Perlindungan Gambut & Emisi Karbon",
                "spesifikasi": "Wajib membangun sekat kanal (canal blocking) untuk mempertahankan muka air tanah gambut minimal -0.4 meter. Larangan total pembakaran lahan (zero burning).",
                "tujuan": "Mencegah kebakaran gambut bawah tanah dan subsidensi lahan."
            })

        # Aturan Reforestasi & Kompensasi Karbon
        if delta_karbon < -0.15 or (kategori_jlh in ['A', 'B'] and pct_jlh_tinggi > 10.0):
            luas_kompensasi = round(luas_ha * (pct_jlh_tinggi / 100.0) * 1.25, 2)
            preskripsi_items.append({
                "kategori": "Kompensasi Ekologis & Reforestasi Karbon",
                "spesifikasi": f"Kewajiban penanaman reforestasi seluas minimal {luas_kompensasi} ha (rasio 1:1.25) pada DAS yang sama menggunakan jenis pohon lokal endemik (Dipterocarpaceae / Shorea spp).",
                "tujuan": "Pemulihan stok karbon dan pemeliharaan konektivitas koridor keanekaragaman hayati."
            })

        # 4. Format Laporan Penapisan AMDAL/KKPR
        report = {
            "ringkasan_proyek": {
                "jenis_kegiatan": kegiatan,
                "lokasi": f"{provinsi}, Pulau {pulau}",
                "luas_tapak_ha": luas_ha,
                "status_jlh_tapak": f"Kategori {kategori_jlh} ({pct_jlh_tinggi:.1f}% dari tapak)"
            },
            "status_d3tlh": {
                "status": status_d3tlh,
                "badge_color": badge_color,
                "deskripsi": status_desc,
                "faktor_pemicu": triggers,
                "dasar_hukum": "PP No. 26 Tahun 2025 Pasal 21 & 22 tentang Status Daya Dukung Lingkungan Hidup"
            },
            "tindakan_preskriptif_wajib": preskripsi_items,
            "referensi_hukum_dan_kebijakan": [
                {
                    "dasar": "PP No. 26 Tahun 2025 Pasal 21 & 22",
                    "mandat": "Evaluasi daya dukung berbasis Kinerja Jasa Lingkungan Hidup dan penetapan status Terlampaui vs Belum Terlampaui."
                },
                {
                    "dasar": "PP No. 26 Tahun 2025 Pasal 33 ayat (1)",
                    "mandat": "Mandat perlindungan mutlak bagi wilayah penyangga kehidupan dengan kinerja JLH Tinggi."
                },
                {
                    "dasar": "Dokumen Informasi Geospasial JLH Tinggi 2025 (KLH/BPLH)",
                    "mandat": f"Arahan Operasional untuk Wilayah Ekoregion Pulau {pulau} (Bab 5)."
                }
            ],
            "narasi_eksekutif_amdal": (
                f"Berdasarkan penapisan lingkungan hidup mengacu pada PP Nomor 26 Tahun 2025 dan Informasi Geospasial JLH Tinggi 2025, "
                f"rencana kegiatan '{kegiatan}' seluas {luas_ha} ha di {provinsi} memiliki status Daya Dukung Lingkungan Hidup (D3TLH) "
                f"'{status_d3tlh}'. Area tapak mencakup {pct_jlh_tinggi:.1f}% kawasan JLH Tinggi (Kategori {kategori_jlh}). "
                f"Untuk memitigasi dampak terhadap tata air dan cadangan karbon regional, pemrakarsa diwajibkan memenuhi standar preskriptif: "
                f"KDH minimal {kdh_min}%, integrasi sistem retensi air terpadu, dan kompensasi vegetasi pada DAS terkait."
            )
        }
        return report

if __name__ == '__main__':
    # Test drive
    engine = PrescriptiveEngine()
    test_assessment = {
        "pulau": "Sumatera",
        "provinsi": "Sumatera Barat",
        "luas_tapak_ha": 35.5,
        "jenis_kegiatan": "Pembangunan Kawasan Logistik & Akses Bandara",
        "pct_jlh_tinggi": 28.5,
        "kategori_jlh": "A",
        "delta_pga": -0.24,
        "delta_tta": -0.19,
        "delta_erosi": -0.12,
        "delta_karbon": -0.22,
        "jarak_sungai_m": 45.0,
        "kelerengan_pct": 8.0,
        "is_gambut": False
    }
    hasil = engine.evaluate_site(test_assessment)
    print("=== HASIL EVALUASI PRESKRIPTIF ENGINE ===")
    print(json.dumps(hasil, indent=2, ensure_ascii=False))
