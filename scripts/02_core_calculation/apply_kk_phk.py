#!/usr/bin/env python3
"""
Script untuk Meng-override Nilai Raster PHK Sumatera Barat Berdasarkan KK.gpkg (Kriteria Khusus):
- Kriteria Khusus 1 -> Value = 5.0
- Kriteria Khusus 2 & 3 -> Value = 4.0
- Area lainnya -> Mempertahankan nilai asli PHK Float32
- Format Output -> LERC_ZSTD (max_z_error: 0.005, ukuran kompak <400 MB)
"""

import os
import sys
import time
import geopandas as gpd
from shapely.geometry import box
from shapely.strtree import STRtree
import rasterio
from rasterio.windows import Window
from rasterio.features import rasterize
import numpy as np

def apply_kriteria_khusus():
    phk_tif_in = "/home/kemenlh/jlh/output/jlh_sumbar_2025/sumbar_2025_jlh_phk_seamless.tif"
    kk_gpkg = "/home/kemenlh/jlh/data/KK.gpkg"
    phk_tif_out = "/home/kemenlh/jlh/output/jlh_sumbar_2025/sumbar_2025_jlh_phk_kk_seamless.tif"

    print("=======================================================", flush=True)
    print("Mulai Pembaruan Nilai PHK dengan Kriteria Khusus (KK)", flush=True)
    print(f"Input PHK TIF : {phk_tif_in}", flush=True)
    print(f"Input KK GPKG : {kk_gpkg}", flush=True)
    print(f"Output TIF    : {phk_tif_out}", flush=True)
    print("Aturan Override:", flush=True)
    print("  - Kriteria Khusus 1        -> 5.0", flush=True)
    print("  - Kriteria Khusus 2 & 3    -> 4.0", flush=True)
    print("  - Luar KK                  -> Nilai Asli PHK", flush=True)
    print("=======================================================", flush=True)

    t0 = time.time()

    # 1. Baca GeoPackage dan Reproject ke EPSG:3857
    print("[1/4] Membaca KK.gpkg dan me-reproject ke EPSG:3857...", flush=True)
    gdf = gpd.read_file(kk_gpkg, layer="jlh")
    print(f"Total poligon KK dibaca: {len(gdf)}", flush=True)
    
    if gdf.crs != "EPSG:3857":
        gdf = gdf.to_crs(epsg=3857)

    # Filter poligon KK1 dan KK2_3
    gdf_kk1 = gdf[gdf["KK_PHK25"] == "Kriteria Khusus 1"].copy()
    gdf_kk23 = gdf[gdf["KK_PHK25"].isin(["Kriteria Khusus 2", "Kriteria Khusus 3"])].copy()

    print(f"Poligon KK 1   (Nilai -> 5.0): {len(gdf_kk1)}", flush=True)
    print(f"Poligon KK 2/3 (Nilai -> 4.0): {len(gdf_kk23)}", flush=True)

    # Bangun Spatial Index (STRtree)
    print("[2/4] Membangun Spatial Index STRtree...", flush=True)
    tree_kk1 = STRtree(gdf_kk1.geometry.values) if len(gdf_kk1) > 0 else None
    tree_kk23 = STRtree(gdf_kk23.geometry.values) if len(gdf_kk23) > 0 else None

    # Simpan array geometri untuk indexing cepat
    geoms_kk1 = gdf_kk1.geometry.values
    geoms_kk23 = gdf_kk23.geometry.values

    # 2. Buka Raster Sumber PHK
    print("[3/4] Menyiapkan raster sumber PHK dan target output...", flush=True)
    with rasterio.open(phk_tif_in) as src:
        meta = src.meta.copy()
        width = src.width
        height = src.height
        transform = src.transform

        print(f"Dimensi Raster: {width} x {height} piksel", flush=True)
        print(f"Resolusi      : {src.res}", flush=True)
        print(f"CRS           : {src.crs}", flush=True)

        meta.update({
            "driver": "GTiff",
            "dtype": "float32",
            "count": 1,
            "tiled": True,
            "blockxsize": 512,
            "blockysize": 512,
            "compress": "lerc_zstd",
            "max_z_error": 0.005,
            "zstd_level": 9,
            "nodata": 0.0,
            "bigtiff": "YES",
            "num_threads": "ALL_CPUS"
        })

        chunk_size = 4096
        total_chunks = (height + chunk_size - 1) // chunk_size
        print(f"Total Chunks: {total_chunks} (Chunk Size: {chunk_size} baris)", flush=True)

        # 3. Proses Chunk per Chunk
        print("[4/4] Memproses override piksel per chunk...", flush=True)
        with rasterio.open(phk_tif_out, "w", **meta) as dst:
            for chunk_idx, y_start in enumerate(range(0, height, chunk_size)):
                actual_chunk_height = min(chunk_size, height - y_start)
                window = Window(0, y_start, width, actual_chunk_height)
                win_transform = rasterio.windows.transform(window, transform)

                # Bounding box chunk ini dalam EPSG:3857
                win_bounds = rasterio.windows.bounds(window, transform)
                chunk_box = box(*win_bounds)

                # Baca data asli chunk
                chunk_data = src.read(1, window=window)

                # Cek perpotongan KK 2 & 3 (Nilai -> 4.0)
                if tree_kk23 is not None:
                    inter_indices_23 = tree_kk23.query(chunk_box)
                    if len(inter_indices_23) > 0:
                        matched_geoms_23 = [geoms_kk23[i] for i in inter_indices_23]
                        mask_23 = rasterize(
                            matched_geoms_23,
                            out_shape=(actual_chunk_height, width),
                            transform=win_transform,
                            fill=0,
                            default_value=1,
                            dtype=np.uint8
                        )
                        # Terapkan nilai 4.0 hanya pada area daratan valid (bukan nodata 0.0)
                        valid_mask = (chunk_data > 0) & (mask_23 == 1)
                        chunk_data[valid_mask] = 4.0

                # Cek perpotongan KK 1 (Nilai -> 5.0) - prioritas tertinggi
                if tree_kk1 is not None:
                    inter_indices_1 = tree_kk1.query(chunk_box)
                    if len(inter_indices_1) > 0:
                        matched_geoms_1 = [geoms_kk1[i] for i in inter_indices_1]
                        mask_1 = rasterize(
                            matched_geoms_1,
                            out_shape=(actual_chunk_height, width),
                            transform=win_transform,
                            fill=0,
                            default_value=1,
                            dtype=np.uint8
                        )
                        valid_mask_1 = (chunk_data > 0) & (mask_1 == 1)
                        chunk_data[valid_mask_1] = 5.0

                # Tulis chunk hasil ke output
                dst.write(chunk_data, 1, window=window)

                if (chunk_idx + 1) % 10 == 0 or (chunk_idx + 1) == total_chunks:
                    pct = (chunk_idx + 1) / total_chunks * 100
                    elapsed = time.time() - t0
                    eta = (elapsed / (chunk_idx + 1)) * (total_chunks - (chunk_idx + 1))
                    print(f"[{pct:5.1f}%] Chunk {chunk_idx + 1}/{total_chunks} selesai | "
                          f"Elapsed: {elapsed/60:.1f}m | ETA: {eta/60:.1f}m", flush=True)

    total_time = time.time() - t0
    filesize_mb = os.path.getsize(phk_tif_out) / (1024 * 1024)
    print(f"\n[SUKSES] Override Selesai dalam {total_time/60:.2f} menit!", flush=True)
    print(f"Ukuran File Hasil: {filesize_mb:.2f} MB", flush=True)
    print(f"File Output: {phk_tif_out}", flush=True)

if __name__ == "__main__":
    apply_kriteria_khusus()
