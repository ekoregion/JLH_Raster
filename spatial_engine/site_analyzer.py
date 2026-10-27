"""
Site Analyzer Engine for Environmental Screening (AMDAL / KKPR / RTRW).
Melakukan Zonal Statistics berkinerja tinggi pada GeoTIFF 0.5m / 10m:
1. Memotong raster penutupan lahan & 6 layer JLH sesuai poligon GeoJSON.
2. Menghitung luas (ha), komposisi tutupan lahan, skor baseline (PGA, PHK, PPK, PYA, PGN, PKU).
3. Menghitung proporsi kategori JLH Tinggi (A, B, C, Tidak Tinggi).
4. Menghubungkan ke PrescriptiveEngine untuk evaluasi hukum PP 26/2025 dan rekomendasi teknis.
"""

import os
import sys
import json
import numpy as np
import rasterio
from rasterio.mask import mask
import geopandas as gpd
from shapely.geometry import shape
from typing import Dict, Any, List

# Tambahkan root directory ke sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from knowledge_base.prescriptive_engine import PrescriptiveEngine

PL_NAMES = {
    1: "Tubuh Air",
    2: "Hutan Lahan Kering Primer",
    3: "Hutan Lahan Kering Sekunder",
    4: "Hutan Mangrove Primer",
    5: "Hutan Mangrove Sekunder",
    6: "Hutan Rawa Primer",
    7: "Semak Belukar",
    8: "Perkebunan",
    9: "Pertanian Lahan Kering",
    10: "Pertanian Campur Semak",
    11: "Sawah",
    12: "Tambak",
    13: "Pemukiman / Terbangun",
    14: "Jalan / Infrastruktur",
    15: "Tanah Terbuka"
}

JLH_TINGGI_NAMES = {
    1: "Tidak Tinggi",
    10: "Kategori A (Air, Karbon, Kehati)",
    21: "Kategori B1 (Air + Karbon)",
    22: "Kategori B2 (Air + Kehati)",
    23: "Kategori B3 (Karbon + Kehati)",
    31: "Kategori C1 (Air)",
    32: "Kategori C2 (Karbon)",
    33: "Kategori C3 (Kehati)"
}

class SiteAnalyzer:
    def __init__(self, data_dir: str = None):
        if data_dir is None:
            data_dir = os.path.join(BASE_DIR, 'data', 'jlh_seamless')
        self.data_dir = data_dir
        self.engine = PrescriptiveEngine()
        
        # Mapping nama raster di data/jlh_seamless/
        self.raster_paths = {
            "pl": os.path.join(self.data_dir, "sumbar_2025_penutupan_lahan_seamless.tif"),
            "jlh_tinggi": os.path.join(self.data_dir, "sumbar_2025_jlh_tinggi_seamless.tif"),
            "pga": os.path.join(self.data_dir, "sumbar_2025_jlh_pga_seamless.tif"),
            "phk": os.path.join(self.data_dir, "sumbar_2025_jlh_phk_seamless.tif"),
            "ppk": os.path.join(self.data_dir, "sumbar_2025_jlh_ppk_seamless.tif"),
            "pya": os.path.join(self.data_dir, "sumbar_2025_jlh_pya_seamless.tif"),
            "pgn": os.path.join(self.data_dir, "sumbar_2025_jlh_pgn_seamless.tif"),
            "pku": os.path.join(self.data_dir, "sumbar_2025_jlh_pku_seamless.tif"),
            "kba": os.path.join(self.data_dir, "sumbar_2025_kba_seamless.tif"),
            "kva": os.path.join(self.data_dir, "sumbar_2025_kva_seamless.tif")
        }

    def _extract_zonal_stats(self, raster_key: str, gdf_proj: gpd.GeoDataFrame) -> np.ndarray:
        raster_file = self.raster_paths.get(raster_key)
        if not raster_file or not os.path.exists(raster_file):
            return np.array([])
        
        with rasterio.open(raster_file) as src:
            # Pastikan CRS cocok
            if gdf_proj.crs != src.crs:
                gdf_matched = gdf_proj.to_crs(src.crs)
            else:
                gdf_matched = gdf_proj
                
            out_img, _ = mask(src, gdf_matched.geometry, crop=True)
            valid = out_img[out_img != src.nodata]
            return valid

    def analyze_geojson(self, geojson_data: Any, jenis_kegiatan: str = "Pembangunan Kawasan & Fasilitas") -> Dict[str, Any]:
        """
        Menganalisis poligon GeoJSON tapak proyek:
        - geojson_data: dict (FeatureCollection, Feature, atau Geometry) atau path file .geojson
        """
        if isinstance(geojson_data, str) and os.path.exists(geojson_data):
            gdf = gpd.read_file(geojson_data)
        elif isinstance(geojson_data, dict):
            if geojson_data.get("type") == "FeatureCollection":
                gdf = gpd.GeoDataFrame.from_features(geojson_data["features"])
            elif geojson_data.get("type") == "Feature":
                gdf = gpd.GeoDataFrame.from_features([geojson_data])
            else:
                geom = shape(geojson_data)
                gdf = gpd.GeoDataFrame(geometry=[geom], crs="EPSG:4326")
        elif isinstance(geojson_data, gpd.GeoDataFrame):
            gdf = geojson_data
        else:
            raise ValueError("Format GeoJSON tidak didukung.")

        if gdf.crs is None:
            gdf.set_crs(epsg=4326, inplace=True)

        # Hitung luas poligon dalam meter persegi (menggunakan proyeksi UTM Zone 47S / EPSG:32747 untuk akurasi luas Sumatera)
        gdf_utm = gdf.to_crs(epsg=32747)
        total_area_m2 = gdf_utm.geometry.area.sum()
        total_area_ha = round(total_area_m2 / 10000.0, 2)

        # Bounding box untuk deteksi pulau / wilayah
        bounds = gdf.total_bounds # [minx, miny, maxx, maxy]
        center_x = (bounds[0] + bounds[2]) / 2.0
        center_y = (bounds[1] + bounds[3]) / 2.0

        if center_x > 105.0:
            pulau = "Kalimantan"
            provinsi = "Kalimantan Barat"
        else:
            pulau = "Sumatera"
            provinsi = "Sumatera Barat"

        # 1. Analisis Tutupan Lahan (PL)
        pl_pixels = self._extract_zonal_stats("pl", gdf)
        pl_summary = []
        is_gambut = False
        if len(pl_pixels) > 0:
            vals, counts = np.unique(pl_pixels, return_counts=True)
            total_px = len(pl_pixels)
            for v, c in zip(vals, counts):
                pct = round(c / total_px * 100.0, 2)
                ha = round(pct / 100.0 * total_area_ha, 2)
                name = PL_NAMES.get(int(v), f"Kelas {v}")
                if int(v) == 6: # Hutan Rawa / Gambut
                    is_gambut = True
                pl_summary.append({
                    "kode": int(v),
                    "nama": name,
                    "luas_ha": ha,
                    "persentase": pct
                })
        pl_summary.sort(key=lambda x: x["persentase"], reverse=True)

        # 2. Analisis JLH Tinggi
        jlh_tinggi_pixels = self._extract_zonal_stats("jlh_tinggi", gdf)
        jlh_tinggi_summary = []
        pct_kategori_a = 0.0
        pct_kategori_b = 0.0
        pct_kategori_c = 0.0
        pct_tidak_tinggi = 0.0

        if len(jlh_tinggi_pixels) > 0:
            vals, counts = np.unique(jlh_tinggi_pixels, return_counts=True)
            total_px = len(jlh_tinggi_pixels)
            for v, c in zip(vals, counts):
                pct = round(c / total_px * 100.0, 2)
                ha = round(pct / 100.0 * total_area_ha, 2)
                name = JLH_TINGGI_NAMES.get(int(v), f"Kelas {v}")
                if int(v) == 10:
                    pct_kategori_a += pct
                elif int(v) in [21, 22, 23]:
                    pct_kategori_b += pct
                elif int(v) in [31, 32, 33]:
                    pct_kategori_c += pct
                elif int(v) == 1:
                    pct_tidak_tinggi += pct

                jlh_tinggi_summary.append({
                    "kode": int(v),
                    "kategori": name,
                    "luas_ha": ha,
                    "persentase": pct
                })
        jlh_tinggi_summary.sort(key=lambda x: x["persentase"], reverse=True)

        # Tentukan kategori dominan untuk evaluasi preskriptif
        if pct_kategori_a > 10.0:
            kategori_eval = "A"
            pct_tinggi_eval = pct_kategori_a
        elif pct_kategori_b > 15.0:
            kategori_eval = "B"
            pct_tinggi_eval = pct_kategori_b
        elif pct_kategori_c > 20.0:
            kategori_eval = "C"
            pct_tinggi_eval = pct_kategori_c
        else:
            kategori_eval = "Tidak Tinggi"
            pct_tinggi_eval = 0.0

        # 3. Analisis Skor 6 Indikator JLH (Skor Baseline T0)
        jlh_scores = {}
        for layer_key in ["pga", "phk", "ppk", "pya", "pgn", "pku"]:
            pixels = self._extract_zonal_stats(layer_key, gdf)
            if len(pixels) > 0:
                mean_val = float(np.mean(pixels))
                min_val = float(np.min(pixels))
                max_val = float(np.max(pixels))
                std_val = float(np.std(pixels))
            else:
                mean_val, min_val, max_val, std_val = 0.0, 0.0, 0.0, 0.0
            
            jlh_scores[layer_key] = {
                "mean": round(mean_val, 2),
                "min": round(min_val, 2),
                "max": round(max_val, 2),
                "std": round(std_val, 2)
            }

        # 4. Ambil KBA & KVA Dominan
        kba_pixels = self._extract_zonal_stats("kba", gdf)
        dominant_kba_id = int(np.bincount(kba_pixels.astype(int)).argmax()) if len(kba_pixels) > 0 else 1
        kba_info = self.engine.lookup_kba(str(dominant_kba_id))

        kva_pixels = self._extract_zonal_stats("kva", gdf)
        dominant_kva_id = int(np.bincount(kva_pixels.astype(int)).argmax()) if len(kva_pixels) > 0 else 1

        # 5. Hitung Estimasi Dampak Penurunan (Proyeksi Awal Delta)
        # Jika lahan terbangun bertambah, fungsi air (PGA) dan karbon (PPK) berkurang sesuai bobot LULC (w_pl = 0.60)
        baseline_pga = jlh_scores.get("pga", {}).get("mean", 3.0)
        baseline_ppk = jlh_scores.get("ppk", {}).get("mean", 3.0)
        baseline_phk = jlh_scores.get("phk", {}).get("mean", 3.0)
        
        # Penurunan kasar tanpa mitigasi (unmitigated): tutupan alami menjadi terbangun (skor turun ~ 1.5 - 2.0 poin dengan bobot 0.6 = delta -0.25 s/d -0.35)
        est_delta_pga = -round(0.60 * (baseline_pga - 1.5) * 0.35, 2)
        est_delta_tta = -round(0.60 * (baseline_pga - 1.5) * 0.28, 2)
        est_delta_karbon = -round(0.60 * (baseline_ppk - 1.0) * 0.40, 2)
        est_delta_erosi = -round(0.18, 2)

        # 6. Panggil Prescriptive Decision Engine
        assessment_input = {
            "pulau": pulau,
            "provinsi": provinsi,
            "luas_tapak_ha": total_area_ha,
            "jenis_kegiatan": jenis_kegiatan,
            "pct_jlh_tinggi": round(pct_kategori_a + pct_kategori_b + pct_kategori_c, 1),
            "kategori_jlh": kategori_eval,
            "delta_pga": est_delta_pga,
            "delta_tta": est_delta_tta,
            "delta_erosi": est_delta_erosi,
            "delta_karbon": est_delta_karbon,
            "jarak_sungai_m": 60.0, # estimasi default
            "kelerengan_pct": 12.0,
            "is_gambut": is_gambut
        }
        prescriptive_result = self.engine.evaluate_site(assessment_input)

        # Gabungkan seluruh hasil
        analysis_output = {
            "metadata_tapak": {
                "jenis_kegiatan": jenis_kegiatan,
                "luas_ha": total_area_ha,
                "koordinat_tengah": {"lng": round(center_x, 5), "lat": round(center_y, 5)},
                "wilayah_administrasi": f"{provinsi}, Pulau {pulau}",
                "kba_dominan_id": dominant_kba_id,
                "kba_dominan_nama": kba_info.get("nama_kba", "Bentang Alam Fluvial/Vulkanik"),
                "kva_dominan_id": dominant_kva_id
            },
            "tutupan_lahan_eksisting": pl_summary,
            "jlh_tinggi_eksisting": {
                "rincian": jlh_tinggi_summary,
                "kategori_a_persen": round(pct_kategori_a, 2),
                "kategori_b_persen": round(pct_kategori_b, 2),
                "kategori_c_persen": round(pct_kategori_c, 2),
                "tidak_tinggi_persen": round(pct_tidak_tinggi, 2)
            },
            "skor_jlh_baseline_t0": jlh_scores,
            "estimasi_penurunan_unmitigated": {
                "delta_pga": est_delta_pga,
                "delta_tta": est_delta_tta,
                "delta_karbon": est_delta_karbon,
                "delta_erosi": est_delta_erosi
            },
            "evaluasi_preskriptif": prescriptive_result
        }
        return analysis_output

if __name__ == '__main__':
    # Test drive dengan aoi_sample.geojson
    sample_path = os.path.join(BASE_DIR, 'git_upload', 'sample_data', 'aoi_sample.geojson')
    analyzer = SiteAnalyzer()
    print("Testing SiteAnalyzer with aoi_sample.geojson ...")
    res = analyzer.analyze_geojson(sample_path, jenis_kegiatan="Pembangunan Kawasan Industri & Terminal Logistik")
    print("\n=== HASIL ZONAL STATS & SCREENING TAPAK ===")
    print(f"Luas Tapak: {res['metadata_tapak']['luas_ha']} ha")
    print(f"Status D3TLH: {res['evaluasi_preskriptif']['status_d3tlh']['status']}")
    print(f"Badge: {res['evaluasi_preskriptif']['status_d3tlh']['badge_color']}")
    print(f"JLH Kategori A: {res['jlh_tinggi_eksisting']['kategori_a_persen']}%")
    print(f"Skor Rata-rata Baseline T0: PGA={res['skor_jlh_baseline_t0']['pga']['mean']}, Karbon={res['skor_jlh_baseline_t0']['ppk']['mean']}")
    print("\nTindakan Preskriptif Wajib:")
    for item in res['evaluasi_preskriptif']['tindakan_preskriptif_wajib']:
        print(f" - [{item['kategori']}] {item['spesifikasi']}")
