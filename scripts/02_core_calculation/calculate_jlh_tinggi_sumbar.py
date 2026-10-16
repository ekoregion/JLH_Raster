#!/usr/bin/env python3
"""
Skrip Pemetaan dan Penggabungan Jasa Lingkungan Hidup Tinggi (JLH Tinggi)
Provinsi Sumatera Barat (Resolusi 0.5 Meter Seamless)

Komponen Penyusun (Ambang Batas Nilai >= 4.2 / Kelas Sangat Tinggi):
1. PGA : JLH Pengatur Air (Water Regulation)
2. PHK : JLH Pendukung Habitat & Keanekaragaman Hayati (Biodiversity & Habitat)
3. PPK : JLH Penyerap & Penyimpan Karbon (Carbon Sequestration & Storage)

Metode Penggabungan:
Menggunakan Aljabar Bitwise 3-Bit (4*b_PGA + 2*b_PHK + 1*b_PPK) yang dipetakan ke
Kode Hierarkis 2-Digit (UInt8) agar Kategori Utama (A, B, C) dan JLH Penyusunnya
(B1, B2, B3, C1, C2, C3) tetap terbaca secara utuh tanpa kehilangan informasi.
"""

import os
import sys
import json
import time
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import rasterio
from rasterio.windows import Window
from rasterio.enums import Resampling

os.environ["GDAL_NUM_THREADS"] = "ALL_CPUS"
os.environ["GDAL_CACHEMAX"] = "2048"

# ==============================================================================
# 1. DEFINISI SKEMA KODEFIKASI HIERARKIS 2-DIGIT & PALET WARNA DIAGRAM VENN
# ==============================================================================
THRESHOLD_TINGGI = 4.2

# Lookup Table dari Bitmask 3-Bit (4*PGA + 2*PHK + 1*PPK) + index 8 untuk NoData:
# Index 0 (000) ->  1 : Non-JLHT (Daratan dengan Ketiga JLH < 4.2)
# Index 1 (001) -> 33 : C3 (JLH Tinggi Penyerap & Penyimpan Karbon)
# Index 2 (010) -> 32 : C2 (JLH Tinggi Pendukung Habitat & Kehati)
# Index 3 (011) -> 22 : B2 (JLH Tinggi Kehati & Karbon)
# Index 4 (100) -> 31 : C1 (JLH Tinggi Pengatur Air)
# Index 5 (101) -> 23 : B3 (JLH Tinggi Pengatur Air & Karbon)
# Index 6 (110) -> 21 : B1 (JLH Tinggi Pengatur Air & Kehati)
# Index 7 (111) -> 10 : A  (JLH Tinggi Pengatur Air, Kehati & Karbon)
# Index 8       ->  0 : NoData (Laut / Di Luar Area Sumatera Barat)
BITMASK_TO_CODE = np.array([1, 33, 32, 22, 31, 23, 21, 10, 0], dtype=np.uint8)

JLHT_CLASSES = {
    10: {
        "bitmask": 7,
        "kode": "A",
        "kategori": "Kategori A (3 JLH Tinggi)",
        "label": "A - JLH Tinggi: Pengatur Air, Kehati & Karbon",
        "penyusun": "PGA + PHK + PPK",
        "rgb": (154, 112, 41, 255),   # Coklat Emas (#9A7029)
        "hex": "#9A7029"
    },
    21: {
        "bitmask": 6,
        "kode": "B1",
        "kategori": "Kategori B (2 JLH Tinggi)",
        "label": "B1 - JLH Tinggi: Pengatur Air & Kehati",
        "penyusun": "PGA + PHK",
        "rgb": (99, 197, 218, 255),   # Biru Muda / Cyan (#63C5DA)
        "hex": "#63C5DA"
    },
    22: {
        "bitmask": 3,
        "kode": "B2",
        "kategori": "Kategori B (2 JLH Tinggi)",
        "label": "B2 - JLH Tinggi: Kehati & Karbon",
        "penyusun": "PHK + PPK",
        "rgb": (242, 234, 59, 255),   # Kuning (#F2EA3B)
        "hex": "#F2EA3B"
    },
    23: {
        "bitmask": 5,
        "kode": "B3",
        "kategori": "Kategori B (2 JLH Tinggi)",
        "label": "B3 - JLH Tinggi: Pengatur Air & Karbon",
        "penyusun": "PGA + PPK",
        "rgb": (174, 82, 154, 255),   # Ungu / Magenta (#AE529A)
        "hex": "#AE529A"
    },
    31: {
        "bitmask": 4,
        "kode": "C1",
        "kategori": "Kategori C (1 JLH Tinggi)",
        "label": "C1 - JLH Tinggi: Pengatur Air",
        "penyusun": "PGA",
        "rgb": (48, 84, 150, 255),    # Biru Tua (#305496)
        "hex": "#305496"
    },
    32: {
        "bitmask": 2,
        "kode": "C2",
        "kategori": "Kategori C (1 JLH Tinggi)",
        "label": "C2 - JLH Tinggi: Pendukung Habitat & Kehati",
        "penyusun": "PHK",
        "rgb": (84, 185, 72, 255),    # Hijau (#54B948)
        "hex": "#54B948"
    },
    33: {
        "bitmask": 1,
        "kode": "C3",
        "kategori": "Kategori C (1 JLH Tinggi)",
        "label": "C3 - JLH Tinggi: Penyerap & Penyimpan Karbon",
        "penyusun": "PPK",
        "rgb": (237, 28, 36, 255),    # Merah (#ED1C24)
        "hex": "#ED1C24"
    },
    1: {
        "bitmask": 0,
        "kode": "Non-JLHT",
        "kategori": "Di Luar JLH Tinggi (< 4.2)",
        "label": "Non-JLH Tinggi (Ketiga JLH < 4.2)",
        "penyusun": "Tidak Ada (< 4.2)",
        "rgb": (226, 232, 240, 180),  # Abu-abu Terang (#E2E8F0)
        "hex": "#E2E8F0"
    }
}


def write_rat_and_qml(output_tif_path, stats_dict=None):
    """
    Membuat file Raster Attribute Table (.tif.aux.xml) dan file Symbology QGIS (.qml)
    agar kode A, B1, B2, B3, C1, C2, C3 beserta penyusunnya langsung terbaca di GIS.
    """
    aux_xml_path = output_tif_path + ".aux.xml"
    qml_path = os.path.splitext(output_tif_path)[0] + ".qml"

    # 1. Buat .tif.aux.xml (GDAL Raster Attribute Table)
    rows_xml = []
    for idx, code_val in enumerate([10, 21, 22, 23, 31, 32, 33, 1]):
        info = JLHT_CLASSES[code_val]
        r, g, b, a = info["rgb"]
        count_val = int(stats_dict.get(str(code_val), {}).get("pixels", 0)) if stats_dict else 0
        luas_ha = float(stats_dict.get(str(code_val), {}).get("luas_ha", 0.0)) if stats_dict else 0.0
        rows_xml.append(f"""      <Row index="{idx}">
        <F>{code_val}</F>
        <F>{count_val}</F>
        <F>{info['kode']}</F>
        <F>{info['kategori'].replace('&', '&amp;').replace('<', '&lt;')}</F>
        <F>{info['penyusun'].replace('<', '&lt;')}</F>
        <F>{info['label'].replace('&', '&amp;').replace('<', '&lt;')}</F>
        <F>{luas_ha:.2f}</F>
        <F>{r}</F>
        <F>{g}</F>
        <F>{b}</F>
        <F>{a}</F>
      </Row>""")

    rat_content = f"""<PAMDataset>
  <PAMRasterBand band="1">
    <Description>Klasifikasi Jasa Lingkungan Hidup Tinggi (PGA, PHK, PPK &gt;= 4.2)</Description>
    <GDALRasterAttributeTable tableType="thematic">
      <FieldDefn index="0"><Name>VALUE</Name><Type>0</Type><Usage>5</Usage></FieldDefn>
      <FieldDefn index="1"><Name>COUNT</Name><Type>0</Type><Usage>1</Usage></FieldDefn>
      <FieldDefn index="2"><Name>KODE_KELAS</Name><Type>2</Type><Usage>2</Usage></FieldDefn>
      <FieldDefn index="3"><Name>KATEGORI_UTAMA</Name><Type>2</Type><Usage>0</Usage></FieldDefn>
      <FieldDefn index="4"><Name>PENYUSUN_JLH</Name><Type>2</Type><Usage>0</Usage></FieldDefn>
      <FieldDefn index="5"><Name>KETERANGAN_LENGKAP</Name><Type>2</Type><Usage>0</Usage></FieldDefn>
      <FieldDefn index="6"><Name>LUAS_HA</Name><Type>1</Type><Usage>0</Usage></FieldDefn>
      <FieldDefn index="7"><Name>Red</Name><Type>0</Type><Usage>6</Usage></FieldDefn>
      <FieldDefn index="8"><Name>Green</Name><Type>0</Type><Usage>7</Usage></FieldDefn>
      <FieldDefn index="9"><Name>Blue</Name><Type>0</Type><Usage>8</Usage></FieldDefn>
      <FieldDefn index="10"><Name>Alpha</Name><Type>0</Type><Usage>9</Usage></FieldDefn>
{chr(10).join(rows_xml)}
    </GDALRasterAttributeTable>
  </PAMRasterBand>
</PAMDataset>
"""
    with open(aux_xml_path, "w", encoding="utf-8") as f:
        f.write(rat_content)

    # 2. Buat file .qml (QGIS Paletted Symbology)
    palette_entries = []
    for code_val in [10, 21, 22, 23, 31, 32, 33, 1]:
        info = JLHT_CLASSES[code_val]
        alpha = info["rgb"][3]
        label_xml = info["label"].replace("&", "&amp;").replace("<", "&lt;")
        palette_entries.append(
            f'        <paletteEntry value="{code_val}" color="{info["hex"]}" alpha="{alpha}" label="{label_xml}"/>'
        )

    qml_content = f"""<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.34.0" styleCategories="Symbology">
  <pipe>
    <rasterrenderer band="1" type="paletted" opacity="1" alphaBand="-1" nodataColor="">
      <colorPalette>
{chr(10).join(palette_entries)}
      </colorPalette>
    </rasterrenderer>
  </pipe>
</qgis>
"""
    with open(qml_path, "w", encoding="utf-8") as f:
        f.write(qml_content)

    print(f"[INFO] RAT (.aux.xml) tersimpan di: {aux_xml_path}", flush=True)
    print(f"[INFO] Simbologi QGIS (.qml) tersimpan di: {qml_path}", flush=True)


# ==============================================================================
# 2. FUNGSI UTAMA PENGGABUNGAN RASTER SEAMLESS 0.5 METER (OPTIMIZED SPARSE WINDOW)
# ==============================================================================
def combine_jlh_tinggi_seamless(
    pga_tif,
    phk_tif,
    ppk_tif,
    output_tif,
    stats_json_path,
    threshold=THRESHOLD_TINGGI,
    tile_h=2048,
    tile_w=65536,
    build_ovr=True
):
    print("======================================================================", flush=True)
    print("PEMETAAN JASA LINGKUNGAN HIDUP TINGGI (JLH TINGGI: KATEGORI A, B, C)", flush=True)
    print(f"Input PGA       : {pga_tif}", flush=True)
    print(f"Input PHK       : {phk_tif}", flush=True)
    print(f"Input PPK       : {ppk_tif}", flush=True)
    print(f"Output TIF      : {output_tif}", flush=True)
    print(f"Ambang Batas    : >= {threshold} (Kelas Sangat Tinggi)", flush=True)
    print("======================================================================", flush=True)

    t0 = time.time()
    bitmask_counts = np.zeros(9, dtype=np.int64)

    with rasterio.open(pga_tif) as src_pga, \
         rasterio.open(phk_tif) as src_phk, \
         rasterio.open(ppk_tif) as src_ppk:

        width, height = src_pga.width, src_pga.height
        res_x, res_y = src_pga.res
        pixel_area_ha = (abs(res_x) * abs(res_y)) / 10000.0  # 0.25 m2 = 0.000025 Ha

        meta = src_pga.meta.copy()
        meta.update({
            "driver": "GTiff",
            "dtype": "uint8",
            "count": 1,
            "nodata": 0,
            "tiled": True,
            "blockxsize": 512,
            "blockysize": 512,
            "compress": "deflate",
            "zlevel": 1,
            "predictor": 1,
            "bigtiff": "YES",
            "SPARSE_OK": "TRUE",
            "num_threads": "ALL_CPUS"
        })

        # Siapkan Embedded Color Table (0..255)
        colormap = {i: (0, 0, 0, 0) for i in range(256)}
        for code_val, info in JLHT_CLASSES.items():
            colormap[code_val] = info["rgb"]

        os.makedirs(os.path.dirname(os.path.abspath(output_tif)), exist_ok=True)
        row_strips = list(range(0, height, tile_h))
        total_strips = len(row_strips)

        with rasterio.open(output_tif, "w", **meta) as dst, \
             ThreadPoolExecutor(max_workers=2) as executor:
            dst.write_colormap(1, colormap)
            dst.set_band_description(1, "JLH_Tinggi_Kategori_A_B1_B2_B3_C1_C2_C3_PHK_KK")

            for s_idx, y_off in enumerate(row_strips):
                h = min(tile_h, height - y_off)
                for x_off in range(0, width, tile_w):
                    win = Window(x_off, y_off, min(tile_w, width - x_off), h)
                    a = src_pga.read(1, window=win)
                    if not np.any(a > 0):
                        continue

                    fb = executor.submit(src_phk.read, 1, window=win)
                    fc = executor.submit(src_ppk.read, 1, window=win)
                    b = fb.result()
                    c = fc.result()

                    bm = (
                        ((a >= threshold).astype(np.uint8) << 2)
                        | ((b >= threshold).astype(np.uint8) << 1)
                        | (c >= threshold).astype(np.uint8)
                    )
                    bm[a <= 0] = 8
                    bitmask_counts += np.bincount(bm.ravel(), minlength=9)
                    out_arr = BITMASK_TO_CODE[bm]
                    dst.write(out_arr, 1, window=win)

                if (s_idx + 1) % 20 == 0 or (s_idx + 1) == total_strips:
                    elapsed = time.time() - t0
                    pct = (s_idx + 1) / total_strips * 100
                    eta = (elapsed / (s_idx + 1)) * (total_strips - (s_idx + 1))
                    print(
                        f"[{pct:5.1f}%] Strip {s_idx+1}/{total_strips} | "
                        f"Elapsed: {elapsed/60:.1f}m | ETA: {eta/60:.1f}m",
                        flush=True
                    )

        # Bangun piramida overviews (Nearest Neighbor agar kode diskrit tidak berubah)
        if build_ovr:
            print("[INFO] Membangun internal overviews [2, 4, 8, 16, 32, 64, 128]...", flush=True)
            with rasterio.open(output_tif, "r+") as dst:
                dst.build_overviews([2, 4, 8, 16, 32, 64, 128], Resampling.nearest)
                dst.update_tags(ns="rio_overview", resampling="nearest")

    # Rekapitulasi Statistik Luasan (Hektar & Persentase)
    pixel_counts = {}
    for code_val, info in JLHT_CLASSES.items():
        pixel_counts[code_val] = int(bitmask_counts[info["bitmask"]])

    total_valid_pixels = sum(pixel_counts.values())
    total_luas_ha = total_valid_pixels * pixel_area_ha

    stats_summary = {
        "threshold": threshold,
        "inputs": {
            "pga": os.path.basename(pga_tif),
            "phk": os.path.basename(phk_tif),
            "ppk": os.path.basename(ppk_tif)
        },
        "pixel_area_ha": pixel_area_ha,
        "total_daratan_ha": round(total_luas_ha, 2),
        "classes": {},
        "categories": {
            "Kategori A": {"luas_ha": 0.0, "persen_daratan": 0.0},
            "Kategori B": {"luas_ha": 0.0, "persen_daratan": 0.0},
            "Kategori C": {"luas_ha": 0.0, "persen_daratan": 0.0},
            "Total JLH Tinggi (A+B+C)": {"luas_ha": 0.0, "persen_daratan": 0.0},
            "Non-JLH Tinggi": {"luas_ha": 0.0, "persen_daratan": 0.0}
        }
    }

    for code_val in [10, 21, 22, 23, 31, 32, 33, 1]:
        px = pixel_counts[code_val]
        ha = px * pixel_area_ha
        pct = (ha / total_luas_ha * 100.0) if total_luas_ha > 0 else 0.0
        info = JLHT_CLASSES[code_val]
        stats_summary["classes"][str(code_val)] = {
            "kode": info["kode"],
            "kategori": info["kategori"],
            "penyusun": info["penyusun"],
            "label": info["label"],
            "pixels": px,
            "luas_ha": round(ha, 2),
            "persen_daratan": round(pct, 2)
        }
        if code_val == 10:
            stats_summary["categories"]["Kategori A"]["luas_ha"] += ha
        elif code_val in (21, 22, 23):
            stats_summary["categories"]["Kategori B"]["luas_ha"] += ha
        elif code_val in (31, 32, 33):
            stats_summary["categories"]["Kategori C"]["luas_ha"] += ha
        else:
            stats_summary["categories"]["Non-JLH Tinggi"]["luas_ha"] += ha

    jlht_total_ha = (
        stats_summary["categories"]["Kategori A"]["luas_ha"]
        + stats_summary["categories"]["Kategori B"]["luas_ha"]
        + stats_summary["categories"]["Kategori C"]["luas_ha"]
    )
    stats_summary["categories"]["Total JLH Tinggi (A+B+C)"]["luas_ha"] = jlht_total_ha

    for cat_key, cat_val in stats_summary["categories"].items():
        cat_val["luas_ha"] = round(cat_val["luas_ha"], 2)
        cat_val["persen_daratan"] = round(
            (cat_val["luas_ha"] / total_luas_ha * 100.0) if total_luas_ha > 0 else 0.0, 2
        )

    with open(stats_json_path, "w", encoding="utf-8") as f:
        json.dump(stats_summary, f, indent=2, ensure_ascii=False)

    write_rat_and_qml(output_tif, stats_summary["classes"])
    total_time = time.time() - t0
    print(f"\n[SUKSES] Selesai dalam {total_time/60:.2f} menit!", flush=True)
    print(f"[SUKSES] Output TIF : {output_tif}", flush=True)
    print(f"[SUKSES] Statistik  : {stats_json_path}", flush=True)
    return stats_summary


if __name__ == "__main__":
    base_dir = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "data/jlh_seamless"
    use_alami = ("--alami" in sys.argv)

    pga_path = os.path.join(base_dir, "sumbar_2025_jlh_pga_seamless.tif")
    # Default menggunakan PHK yang sudah diintegrasikan dengan Kawasan Konservasi (phk_kk)
    phk_name = "sumbar_2025_jlh_phk_seamless.tif" if use_alami else "sumbar_2025_jlh_phk_kk_seamless.tif"
    phk_path = os.path.join(base_dir, phk_name)
    ppk_path = os.path.join(base_dir, "sumbar_2025_jlh_ppk_seamless.tif")

    suffix = "_alami" if use_alami else ""
    out_tif = os.path.join(base_dir, f"sumbar_2025_jlh_tinggi{suffix}_seamless.tif")
    out_json = os.path.join(base_dir, f"luasan_jlh_tinggi{suffix}.json")

    combine_jlh_tinggi_seamless(pga_path, phk_path, ppk_path, out_tif, out_json)
