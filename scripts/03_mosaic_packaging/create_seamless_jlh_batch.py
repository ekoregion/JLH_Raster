#!/usr/bin/env python3
"""
Script Batch untuk Mengonversi 6 VRT JLH Sumatera Barat ke GeoTIFF Seamless Float32
dengan Kompresi LERC_ZSTD (Opsi 2: Presisi Float32 murni, ukuran file kecil <1 GB).
"""

import os
import sys
import time
import rasterio
from rasterio.windows import Window
import numpy as np

INDICATORS = ["pga", "phk", "ppk", "pya", "pgn", "pku"]

def convert_single_vrt(vrt_path, output_path, max_z_error=0.005, chunk_size=4096):
    print(f"\n=======================================================", flush=True)
    print(f"Mulai Konversi VRT -> Seamless Float32 LERC_ZSTD", flush=True)
    print(f"Input VRT   : {vrt_path}", flush=True)
    print(f"Output TIF  : {output_path}", flush=True)
    print(f"Max Z Error : {max_z_error} (toleransi error desimal)", flush=True)
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
            "dtype": "float32",
            "count": 1,
            "tiled": True,
            "blockxsize": 512,
            "blockysize": 512,
            "compress": "lerc_zstd",
            "max_z_error": max_z_error,
            "zstd_level": 9,
            "nodata": 0.0,
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
                    chunk_data = np.nan_to_num(chunk_data, nan=0.0)

                dst.write(chunk_data, 1, window=window)

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

def run_batch(base_dir, max_z_error=0.005):
    print(f"=== BATCH PROCESSING 6 INDIKATOR JLH SEAMLESS ===", flush=True)
    for ind in INDICATORS:
        vrt_in = os.path.join(base_dir, f"sumbar_2025_jlh_{ind}.vrt")
        tif_out = os.path.join(base_dir, f"sumbar_2025_jlh_{ind}_seamless.tif")

        # Jika sudah ada dan ukuran > 50 MB, lewati (misal PGA yang sedang diproses)
        if os.path.exists(tif_out) and os.path.getsize(tif_out) > 50 * 1024 * 1024:
            # Periksa apakah ada proses yang sedang menulisnya
            print(f"\n[SKIP/CHECK] {tif_out} sudah ada ({os.path.getsize(tif_out)/(1024*1024):.1f} MB).", flush=True)
            continue

        print(f"\n>>> Memproses Indikator: {ind.upper()} <<<", flush=True)
        convert_single_vrt(vrt_in, tif_out, max_z_error=max_z_error)

if __name__ == "__main__":
    base_dir = "/home/kemenlh/jlh/output/jlh_sumbar_2025"
    if len(sys.argv) > 1 and sys.argv[1] in INDICATORS:
        # Proses 1 indikator spesifik
        ind = sys.argv[1]
        vrt = os.path.join(base_dir, f"sumbar_2025_jlh_{ind}.vrt")
        out = os.path.join(base_dir, f"sumbar_2025_jlh_{ind}_seamless.tif")
        convert_single_vrt(vrt, out)
    else:
        # Batch seluruh indikator
        run_batch(base_dir)
