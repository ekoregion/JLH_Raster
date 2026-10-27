"""
Spatial Dynamic Trajectory Simulator for Environmental Screening & Decision Support.
Memproyeksikan trajektori kuantitatif penutupan lahan dan 6 indikator JLH dari waktu ke waktu:
- T0 (Baseline 2025)
- T1 (Konstruksi / Operasi Awal 2027)
- T2 (Keseimbangan Jangka Panjang 2035)

Membandingkan 3 Skenario Spasial:
1. Skenario BAU (Business-As-Usual)
2. Skenario Unmitigated Development (Tanpa Mitigasi Ketat)
3. Skenario Prescriptive / Sustainable Mitigation (Mitigasi Penuh Sesuai PP 26/2025)
"""

import os
import sys
import json
from typing import Dict, Any, List

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

class TrajectorySimulator:
    def __init__(self):
        pass

    def simulate(self, site_analysis: Dict[str, Any], custom_params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Menghasilkan proyeksi trajektori multi-temporal berbasis metrik zonal tapak.
        """
        if custom_params is None:
            custom_params = {}

        t0_scores = site_analysis.get("skor_jlh_baseline_t0", {})
        meta = site_analysis.get("metadata_tapak", {})
        preskripsi = site_analysis.get("evaluasi_preskriptif", {})
        
        luas_ha = meta.get("luas_ha", 10.0)
        pct_jlh_tinggi = site_analysis.get("jlh_tinggi_eksisting", {}).get("kategori_a_persen", 0.0) + \
                         site_analysis.get("jlh_tinggi_eksisting", {}).get("kategori_b_persen", 0.0)

        # Nilai dasar T0 (2025)
        pga_0 = t0_scores.get("pga", {}).get("mean", 3.5)
        phk_0 = t0_scores.get("phk", {}).get("mean", 3.5)
        ppk_0 = t0_scores.get("ppk", {}).get("mean", 3.5)
        pya_0 = t0_scores.get("pya", {}).get("mean", 3.5)
        pgn_0 = t0_scores.get("pgn", {}).get("mean", 3.0)
        pku_0 = t0_scores.get("pku", {}).get("mean", 3.5)
        comp_0 = round((pga_0 + phk_0 + ppk_0 + pya_0 + pgn_0 + pku_0) / 6.0, 2)

        # KDH preskriptif vs unmitigated
        kdh_preskriptif = 60 if pct_jlh_tinggi > 20 else 40
        kdh_unmitigated = custom_params.get("kdh_unmitigated", 15)

        # -------------------------------------------------------------------------
        # 1. SKENARIO BAU (Business-As-Usual)
        # Tren degradasi historis tanpa proyek baru: laju penurunan ~0.4% per tahun
        # -------------------------------------------------------------------------
        bau_t0 = {"tahun": 2025, "pga": pga_0, "phk": phk_0, "ppk": ppk_0, "pya": pya_0, "pgn": pgn_0, "pku": pku_0, "komposit": comp_0}
        bau_t1 = {
            "tahun": 2027,
            "pga": round(pga_0 * 0.992, 2),
            "phk": round(phk_0 * 0.990, 2),
            "ppk": round(ppk_0 * 0.991, 2),
            "pya": round(pya_0 * 0.993, 2),
            "pgn": round(pgn_0 * 0.995, 2),
            "pku": round(pku_0 * 0.992, 2),
            "komposit": round(comp_0 * 0.992, 2)
        }
        bau_t2 = {
            "tahun": 2035,
            "pga": round(pga_0 * 0.960, 2),
            "phk": round(phk_0 * 0.945, 2),
            "ppk": round(ppk_0 * 0.952, 2),
            "pya": round(pya_0 * 0.965, 2),
            "pgn": round(pgn_0 * 0.970, 2),
            "pku": round(pku_0 * 0.958, 2),
            "komposit": round(comp_0 * 0.958, 2)
        }

        # -------------------------------------------------------------------------
        # 2. SKENARIO UNMITIGATED (Pembangunan Tanpa Mitigasi Ketat)
        # Footprint terbangun 85%, tanpa kolam retensi, tanpa reforestasi kompensasi
        # -------------------------------------------------------------------------
        unmit_loss_factor_t1 = (100.0 - kdh_unmitigated) / 100.0 * 0.60 # bobot tutupan lahan 0.60
        unmit_t0 = {"tahun": 2025, "pga": pga_0, "phk": phk_0, "ppk": ppk_0, "pya": pya_0, "pgn": pgn_0, "pku": pku_0, "komposit": comp_0}
        unmit_t1 = {
            "tahun": 2027,
            "pga": round(max(1.0, pga_0 - unmit_loss_factor_t1 * 1.8), 2),
            "phk": round(max(1.0, phk_0 - unmit_loss_factor_t1 * 2.2), 2),
            "ppk": round(max(1.0, ppk_0 - unmit_loss_factor_t1 * 2.0), 2),
            "pya": round(max(1.0, pya_0 - unmit_loss_factor_t1 * 1.5), 2),
            "pgn": round(max(1.0, pgn_0 - unmit_loss_factor_t1 * 1.2), 2),
            "pku": round(max(1.0, pku_0 - unmit_loss_factor_t1 * 1.6), 2),
        }
        unmit_t1["komposit"] = round((unmit_t1["pga"] + unmit_t1["phk"] + unmit_t1["ppk"] + unmit_t1["pya"] + unmit_t1["pgn"] + unmit_t1["pku"]) / 6.0, 2)

        # Pada T2 (2035), terjadi degradasi sekunder di luar batas tapak (banjir musiman, erosi tebing sungai)
        unmit_t2 = {
            "tahun": 2035,
            "pga": round(max(1.0, unmit_t1["pga"] * 0.92), 2),
            "phk": round(max(1.0, unmit_t1["phk"] * 0.90), 2),
            "ppk": round(max(1.0, unmit_t1["ppk"] * 0.93), 2),
            "pya": round(max(1.0, unmit_t1["pya"] * 0.91), 2),
            "pgn": round(max(1.0, unmit_t1["pgn"] * 0.94), 2),
            "pku": round(max(1.0, unmit_t1["pku"] * 0.93), 2),
        }
        unmit_t2["komposit"] = round((unmit_t2["pga"] + unmit_t2["phk"] + unmit_t2["ppk"] + unmit_t2["pya"] + unmit_t2["pgn"] + unmit_t2["pku"]) / 6.0, 2)

        # -------------------------------------------------------------------------
        # 3. SKENARIO PRESKRIPTIF (Sustainable / Mitigated Development)
        # KDH 60%, Kolam retensi zero run-off, sempadan riparian 100m, reforestasi 1:1.25
        # -------------------------------------------------------------------------
        presc_loss_factor_t1 = (100.0 - kdh_preskriptif) / 100.0 * 0.60
        presc_t0 = {"tahun": 2025, "pga": pga_0, "phk": phk_0, "ppk": ppk_0, "pya": pya_0, "pgn": pgn_0, "pku": pku_0, "komposit": comp_0}
        presc_t1 = {
            "tahun": 2027,
            # Penurunan sangat terkontrol hanya pada footprint bangunan (40% tapak)
            "pga": round(max(1.0, pga_0 - presc_loss_factor_t1 * 0.7), 2),
            "phk": round(max(1.0, phk_0 - presc_loss_factor_t1 * 0.9), 2),
            "ppk": round(max(1.0, ppk_0 - presc_loss_factor_t1 * 0.8), 2),
            "pya": round(max(1.0, pya_0 - presc_loss_factor_t1 * 0.5), 2),
            "pgn": round(max(1.0, pgn_0 - presc_loss_factor_t1 * 0.6), 2),
            "pku": round(max(1.0, pku_0 - presc_loss_factor_t1 * 0.6), 2),
        }
        presc_t1["komposit"] = round((presc_t1["pga"] + presc_t1["phk"] + presc_t1["ppk"] + presc_t1["pya"] + presc_t1["pgn"] + presc_t1["pku"]) / 6.0, 2)

        # Pada T2 (2035), reforestasi kompensasi 1:1.25 matang, kolam retensi berfungsi stabil, koridor pulih
        presc_t2 = {
            "tahun": 2035,
            # Net recovery: nilai naik kembali mendekati atau melampaui T0 berkat reboisasi 1.25x
            "pga": round(min(5.0, presc_t1["pga"] + 0.35), 2),
            "phk": round(min(5.0, presc_t1["phk"] + 0.45), 2),
            "ppk": round(min(5.0, presc_t1["ppk"] + 0.50), 2), # simpanan karbon hutan kompensasi tumbuh
            "pya": round(min(5.0, presc_t1["pya"] + 0.30), 2),
            "pgn": round(min(5.0, presc_t1["pgn"] + 0.20), 2),
            "pku": round(min(5.0, presc_t1["pku"] + 0.40), 2),
        }
        presc_t2["komposit"] = round((presc_t2["pga"] + presc_t2["phk"] + presc_t2["ppk"] + presc_t2["pya"] + presc_t2["pgn"] + presc_t2["pku"]) / 6.0, 2)

        # -------------------------------------------------------------------------
        # Format Data Deret Waktu untuk Visualisasi Grafik WebGIS (Chart.js / ECharts)
        # -------------------------------------------------------------------------
        years = [2025, 2027, 2035]
        chart_series = {
            "years": years,
            "komposit": {
                "bau": [bau_t0["komposit"], bau_t1["komposit"], bau_t2["komposit"]],
                "unmitigated": [unmit_t0["komposit"], unmit_t1["komposit"], unmit_t2["komposit"]],
                "prescriptive": [presc_t0["komposit"], presc_t1["komposit"], presc_t2["komposit"]]
            },
            "pga_air": {
                "bau": [bau_t0["pga"], bau_t1["pga"], bau_t2["pga"]],
                "unmitigated": [unmit_t0["pga"], unmit_t1["pga"], unmit_t2["pga"]],
                "prescriptive": [presc_t0["pga"], presc_t1["pga"], presc_t2["pga"]]
            },
            "ppk_karbon": {
                "bau": [bau_t0["ppk"], bau_t1["ppk"], bau_t2["ppk"]],
                "unmitigated": [unmit_t0["ppk"], unmit_t1["ppk"], unmit_t2["ppk"]],
                "prescriptive": [presc_t0["ppk"], presc_t1["ppk"], presc_t2["ppk"]]
            },
            "phk_kehati": {
                "bau": [bau_t0["phk"], bau_t1["phk"], bau_t2["phk"]],
                "unmitigated": [unmit_t0["phk"], unmit_t1["phk"], unmit_t2["phk"]],
                "prescriptive": [presc_t0["phk"], presc_t1["phk"], presc_t2["phk"]]
            }
        }

        # Matriks Perbandingan Ringkasan (Delta T2 - T0)
        comparison_table = [
            {
                "indikator": "Pengaturan Tata Air (PGA)",
                "baseline_t0": pga_0,
                "bau_t2": bau_t2["pga"],
                "unmitigated_t2": unmit_t2["pga"],
                "prescriptive_t2": presc_t2["pga"],
                "delta_unmitigated": round(unmit_t2["pga"] - pga_0, 2),
                "delta_prescriptive": round(presc_t2["pga"] - pga_0, 2)
            },
            {
                "indikator": "Penyimpan Karbon (PPK)",
                "baseline_t0": ppk_0,
                "bau_t2": bau_t2["ppk"],
                "unmitigated_t2": unmit_t2["ppk"],
                "prescriptive_t2": presc_t2["ppk"],
                "delta_unmitigated": round(unmit_t2["ppk"] - ppk_0, 2),
                "delta_prescriptive": round(presc_t2["ppk"] - ppk_0, 2)
            },
            {
                "indikator": "Habitat & Kehati (PHK)",
                "baseline_t0": phk_0,
                "bau_t2": bau_t2["phk"],
                "unmitigated_t2": unmit_t2["phk"],
                "prescriptive_t2": presc_t2["phk"],
                "delta_unmitigated": round(unmit_t2["phk"] - phk_0, 2),
                "delta_prescriptive": round(presc_t2["phk"] - phk_0, 2)
            },
            {
                "indikator": "Indeks Komposit Keseluruhan",
                "baseline_t0": comp_0,
                "bau_t2": bau_t2["komposit"],
                "unmitigated_t2": unmit_t2["komposit"],
                "prescriptive_t2": presc_t2["komposit"],
                "delta_unmitigated": round(unmit_t2["komposit"] - comp_0, 2),
                "delta_prescriptive": round(presc_t2["komposit"] - comp_0, 2)
            }
        ]

        # Status D3TLH Trajektori
        status_trajectory = {
            "bau": {"t0": "AMAN", "t1": "AMAN", "t2": "RAWAN"},
            "unmitigated": {"t0": "RAWAN", "t1": "TERLAMPAUI (MERAH)", "t2": "KRITIS PARAH (HITAM)"},
            "prescriptive": {"t0": "RAWAN", "t1": "TERKENDALI (ORANYE)", "t2": "PULIH BERKELANJUTAN (HIJAU)"}
        }

        output = {
            "metadata_simulasi": {
                "luas_tapak_ha": luas_ha,
                "kdh_diterapkan_persen": kdh_preskriptif,
                "kdh_unmitigated_persen": kdh_unmitigated,
                "horizon_waktu": ["2025 (T0)", "2027 (T1)", "2035 (T2)"]
            },
            "chart_series": chart_series,
            "tabel_perbandingan": comparison_table,
            "status_d3tlh_trajektori": status_trajectory,
            "analisis_narasi_trajektori": (
                f"Simulasi dinamika spasial menunjukkan divergensi drastis pada horizon 2035 (T2). "
                f"Jika kegiatan seluas {luas_ha} ha dijalankan tanpa mitigasi ketat (Unmitigated), indeks komposit JLH "
                f"anjlok dari {comp_0} menjadi {unmit_t2['komposit']} (penurunan bersih {round(unmit_t2['komposit'] - comp_0, 2)} poin), "
                f"memicu status D3TLH 'KRITIS PARAH'. Sebaliknya, dengan pemenuhan paket preskriptif PP 26/2025 "
                f"(KDH {kdh_preskriptif}%, kolam retensi air, dan reforestasi 1:1.25), indeks komposit JLH pada 2035 dapat "
                f"stabil di angka {presc_t2['komposit']}, mengembalikan status wilayah menjadi 'PULIH BERKELANJUTAN'."
            )
        }
        return output

if __name__ == '__main__':
    from spatial_engine.site_analyzer import SiteAnalyzer
    sample_path = os.path.join(BASE_DIR, 'git_upload', 'sample_data', 'aoi_sample.geojson')
    analyzer = SiteAnalyzer()
    site_res = analyzer.analyze_geojson(sample_path)
    
    sim = TrajectorySimulator()
    traj_res = sim.simulate(site_res)
    print("\n=== HASIL SIMULASI TRAJEKTORI SPASIAL (2025 - 2035) ===")
    print("Chart Series Komposit:")
    print(" - BAU:", traj_res['chart_series']['komposit']['bau'])
    print(" - Unmitigated:", traj_res['chart_series']['komposit']['unmitigated'])
    print(" - Prescriptive:", traj_res['chart_series']['komposit']['prescriptive'])
    print("\nStatus D3TLH Trajektori:")
    print(" - Unmitigated:", traj_res['status_d3tlh_trajektori']['unmitigated'])
    print(" - Prescriptive:", traj_res['status_d3tlh_trajektori']['prescriptive'])
    print("\nNarasi Analisis:")
    print(traj_res['analisis_narasi_trajektori'])
