#!/usr/bin/env python3
"""
Script untuk mengonversi VRT JLH Sumatera Barat menjadi GeoTIFF Seamless Float32
dengan kompresi LERC_ZSTD (Opsi 2: Presisi tinggi, ukuran file kecil <1 GB).
"""

import os
import sys
import time
import rasterio
from rasterio.windows import Window
import numpy as np

def convert_vrt_to_seamless_lerc(vrt_path, output_path, max_z_error=0.005, chunk_size=4096):
    print(f"\n=======================================================")
    print(f"Mulai konversi VRT -> Seamless Float32 LERC_ZSTD")
    print(f"Input VRT : {vrt_path}")
    print(f"Output TIF: {output_path}")
    print(f"Max Z Error: {max_z_error} (toleransi deviasi desimal)")
    print(f"Chunk Size : {chunk_size} baris")
    print(f"=======================================================")

    t0 = time.time()

    with rasterio.open(vrt_path) as src:
        meta = src.meta.copy()
        width = src.width
        height = src.height
        nodata_val = src.nodata if src.nodata is not None else 0.0

        print(f"Dimensi Raster: {width} x {height} piksel")
        print(f"Resolusi      : {src.res}")
        print(f"CRS           : {src.crs}")
        print(f"Bounds        : {src.bounds}")

        # Konfigurasi GeoTIFF LERC_ZSTD
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
        print(f"Total Chunks: {total_chunks}")

        with rasterio.open(output_path, "w", **meta) as dst:
            for chunk_idx, y_start in enumerate(range(0, height, chunk_size)):
                actual_chunk_height = min(chunk_size, height - y_start)
                window = Window(0, y_start, width, actual_chunk_height)

                # Baca window dari VRT
                chunk_data = src.read(1, window=window)

                # Pastikan NaN diubah ke nodata 0.0
                if np.isnan(chunk_data).any():
                    chunk_data = np.nan_to_num(chunk_data, nan=0.0)

                # Tulis window ke output
                dst.write(chunk_data, 1, window=window)

                pct = (chunk_idx + 1) / total_chunks * 100
                elapsed = time.time() - t0
                eta = (elapsed / (chunk_idx + 1)) * (total_chunks - (chunk_idx + 1))
                if (chunk_idx + 1) % 10 == 0 or (chunk_idx + 1) == total_chunks:
                    print(f"[{pct:5.1f}%] Chunk {chunk_idx + 1}/{total_chunks} selesai. "
                          f"Elapsed: {elapsed/60:.1f} m, ETA: {eta/60:.1f} m")

    total_time = time.time() - t0
    filesize_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"\n[SUKSES] Konversi Selesai dalam {total_time/60:.2f} menit!")
    print(f"Ukuran File Hasil: {filesize_mb:.2f} MB ({filesize_mb/1024:.2f} GB)")
    print(f"Lokasi: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Penggunaan: python create_seamless_jlh_lerc.py <vrt_path> <output_path> [max_z_error]")
        sys.exit(1)

    vrt_in = sys.argv[1]
    tif_out = sys.argv[2]
    max_err = float(sys.argv[3]) if len(sys.argv) > 3 else 0.005

    convert_vrt_to_seamless_lerc(vrt_in, tif_out, max_err)
