#!/usr/bin/env python3
"""
Script untuk Mengonversi VRT KBA dan KVA Sumatera Barat menjadi GeoTIFF Seamless uint8
dengan Kompresi ZSTD (Ukuran sangat kecil ~80-120 MB se-Sumatera Barat, 0.5 meter).
"""

import os
import sys
import time
import rasterio
from rasterio.windows import Window
import numpy as np

def convert_vrt_to_seamless_uint8(vrt_path, output_path, chunk_size=8192):
    print(f"\n=======================================================", flush=True)
    print(f"Mulai Konversi VRT -> Seamless UInt8 ZSTD", flush=True)
    print(f"Input VRT   : {vrt_path}", flush=True)
    print(f"Output TIF  : {output_path}", flush=True)
    print(f"Chunk Size  : {chunk_size} baris", flush=True)
    print(f"=======================================================", flush=True)

    if not os.path.exists(vrt_path):
        print(f"[ERROR] File VRT tidak ditemukan: {vrt_path}", flush=True)
        return False

    t0 = time.time()

    with rasterio.open(vrt_path) as src:
        meta = src.meta.copy()
        width = src.width
        height = src.height

        print(f"Dimensi : {width} x {height} piksel", flush=True)
        print(f"Resolusi: {src.res}", flush=True)
        print(f"CRS     : {src.crs}", flush=True)

        meta.update({
            "driver": "GTiff",
            "dtype": "uint8",
            "count": 1,
            "tiled": True,
            "blockxsize": 512,
            "blockysize": 512,
            "compress": "zstd",
            "zstd_level": 9,
            "nodata": 0,
            "bigtiff": "YES",
            "num_threads": "ALL_CPUS"
        })

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        total_chunks = (height + chunk_size - 1) // chunk_size
        print(f"Total Chunks: {total_chunks}", flush=True)

        with rasterio.open(output_path, "w", **meta) as dst:
            for chunk_idx, y_start in enumerate(range(0, height, chunk_size)):
                actual_chunk_height = min(chunk_size, height - y_start)
                window = Window(0, y_start, width, actual_chunk_height)

                chunk_data = src.read(1, window=window)
                if np.isnan(chunk_data).any():
                    chunk_data = np.nan_to_num(chunk_data, nan=0)

                dst.write(chunk_data.astype(np.uint8), 1, window=window)

                if (chunk_idx + 1) % 5 == 0 or (chunk_idx + 1) == total_chunks:
                    pct = (chunk_idx + 1) / total_chunks * 100
                    elapsed = time.time() - t0
                    eta = (elapsed / (chunk_idx + 1)) * (total_chunks - (chunk_idx + 1))
                    print(f"[{pct:5.1f}%] Chunk {chunk_idx + 1}/{total_chunks} | "
                          f"Elapsed: {elapsed/60:.1f}m | ETA: {eta/60:.1f}m", flush=True)

    total_time = time.time() - t0
    filesize_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"\n[SUKSES] Selesai dalam {total_time/60:.2f} menit!", flush=True)
    print(f"Ukuran File: {filesize_mb:.2f} MB ({filesize_mb/1024:.2f} GB)", flush=True)
    print(f"Path: {output_path}", flush=True)
    return True

if __name__ == "__main__":
    base_dir = "/home/kemenlh/jlh/data"
    out_dir = "/home/kemenlh/jlh/output/jlh_sumbar_2025"

    tasks = [
        ("kba", os.path.join(base_dir, "kba_sumbar_mosaic.vrt"), os.path.join(out_dir, "sumbar_2025_kba_seamless.tif")),
        ("kva", os.path.join(base_dir, "kva_sumbar_mosaic.vrt"), os.path.join(out_dir, "sumbar_2025_kva_seamless.tif"))
    ]

    for name, vrt, out_tif in tasks:
        print(f"\n>>> Memproses Seamless {name.upper()} <<<", flush=True)
        convert_vrt_to_seamless_uint8(vrt, out_tif)
