#!/usr/bin/env python3
"""
Pemodelan Raster KBA & KVA Seamless Provinsi Kalimantan Barat
Resolusi 10 x 10 meter, 8-bit unsigned integer (uint8), kompresi LZW, Tiled 512x512.
Format 1 file tunggal utuh (seamless tanpa pemotongan tile) mencakup seluruh Kalimantan Barat.
Nilai piksel KBA & KVA disesuaikan dengan kolom 'Value' pada Skor_JLH_2026.xlsx.
"""

import os
import time
import openpyxl
import numpy as np
import rasterio
from rasterio.windows import Window
from rasterio.transform import from_origin
from rasterio.features import rasterize
from shapely.geometry import box
import pyogrio
import geopandas as gpd
import pandas as pd

def load_scoring_maps(excel_path):
    wb = openpyxl.load_workbook(excel_path, data_only=True)
    
    # 1. Sheet Skor KBA
    ws_kba = wb['Skor KBA']
    kba_dict = {}
    kba_names = {}
    for r in ws_kba.iter_rows(values_only=True):
        if r[0] is not None and str(r[0]).strip().isdigit() and r[1] is not None:
            val = int(r[0])
            name = str(r[1]).strip()
            kba_dict[name.lower()] = val
            kba_names[val] = name

    # 2. Sheet Skor KVA
    ws_kva = wb['Skor KVA']
    kva_dict = {}
    kva_names = {}
    for r in ws_kva.iter_rows(values_only=True):
        if r[0] is not None and str(r[0]).strip().isdigit() and r[1] is not None:
            val = int(r[0])
            name = str(r[1]).strip()
            kva_dict[name.lower()] = val
            kva_names[val] = name

    return kba_dict, kba_names, kva_dict, kva_names

def parse_ue(ue_str):
    if not ue_str:
        return "", ""
    s = str(ue_str).strip()
    if ' bervegetasi ' in s:
        kba, kva = s.split(' bervegetasi ', 1)
        return kba.strip(), kva.strip()
    return s, ""

def get_kba_value(kba_str, kba_dict):
    clean = kba_str.strip().lower()
    return kba_dict.get(clean, 0)

def get_kva_value(kva_str, kva_dict):
    clean = kva_str.strip().lower()
    # Sheet Skor KVA uses 'vegetasi ...'
    if not clean.startswith('vegetasi '):
        cand = 'vegetasi ' + clean
    else:
        cand = clean
    return kva_dict.get(cand, 0)

def main():
    t_start = time.time()
    print("=" * 65)
    print("🌲 RASTERISASI KBA & KVA SEAMLESS KALIMANTAN BARAT (10M)")
    print("=" * 65)

    excel_path = 'data/Skor_JLH_2026.xlsx'
    gpkg_path = 'data/UE_Kalbar.gpkg'
    out_kba = 'data/kba_kalbar_10m.tif'
    out_kva = 'data/kva_kalbar_10m.tif'

    print("📖 Membaca tabel skor dari Skor_JLH_2026.xlsx...")
    kba_dict, kba_names, kva_dict, kva_names = load_scoring_maps(excel_path)
    print(f"  • Master Skor KBA: {len(kba_dict)} kelas")
    print(f"  • Master Skor KVA: {len(kva_dict)} kelas")

    print("\n🗺️  Membaca dan mereprojeksi UE_Kalbar.gpkg ke EPSG:3857...")
    gdf = pyogrio.read_dataframe(gpkg_path, layer='ue_250k')
    gdf_3857 = gdf.to_crs('EPSG:3857')
    print(f"  • Total poligon: {len(gdf_3857):,}")

    # Ekstrak nilai KBA & KVA untuk setiap fitur
    kba_vals = []
    kva_vals = []
    legend_kba = {}
    legend_kva = {}

    for ue in gdf_3857['UE_250']:
        kba_s, kva_s = parse_ue(ue)
        v_kba = get_kba_value(kba_s, kba_dict)
        v_kva = get_kva_value(kva_s, kva_dict)
        kba_vals.append(v_kba)
        kva_vals.append(v_kva)
        if v_kba > 0 and v_kba not in legend_kba:
            legend_kba[v_kba] = kba_names.get(v_kba, kba_s)
        if v_kva > 0 and v_kva not in legend_kva:
            legend_kva[v_kva] = kva_names.get(v_kva, kva_s)

    gdf_3857['VAL_KBA'] = kba_vals
    gdf_3857['VAL_KVA'] = kva_vals

    print(f"  • Kelas KBA teridentifikasi di Kalbar: {len(legend_kba)} kelas (Value: {sorted(legend_kba.keys())})")
    print(f"  • Kelas KVA teridentifikasi di Kalbar: {len(legend_kva)} kelas (Value: {sorted(legend_kva.keys())})")

    # Hitung Bounding Box & Dimensi Raster pada resolusi 10m
    res = 10.0
    bounds = gdf_3857.total_bounds
    minx = float(int(bounds[0] // res) * res)
    maxx = float(int(bounds[2] // res + 1) * res)
    miny = float(int(bounds[1] // res) * res)
    maxy = float(int(bounds[3] // res + 1) * res)

    total_w = int(round((maxx - minx) / res))
    total_h = int(round((maxy - miny) / res))
    total_tf = from_origin(minx, maxy, res, res)

    print(f"\n📐 Parameter Raster Seamless:")
    print(f"  • Resolusi     : {res} m x {res} m")
    print(f"  • Dimensi Citra: {total_w:,} x {total_h:,} piksel ({total_w * total_h / 1e6:.1f} Miliar Piksel)")
    print(f"  • Bounding Box : minX={minx:.1f}, minY={miny:.1f}, maxX={maxx:.1f}, maxY={maxy:.1f}")
    print(f"  • Sistem CRS   : EPSG:3857 (WGS 84 / Pseudo-Mercator)")

    # Profile GeoTIFF
    profile = {
        'driver': 'GTiff',
        'dtype': rasterio.uint8,
        'nodata': 0,
        'width': total_w,
        'height': total_h,
        'count': 1,
        'crs': gdf_3857.crs,
        'transform': total_tf,
        'compress': 'lzw',
        'tiled': True,
        'blockxsize': 512,
        'blockysize': 512
    }

    # Bangun spatial index untuk kueri cepat
    print("\n🌲 Membangun spatial index...")
    tree = gdf_3857.sindex

    # Chunk processing (strips of 5,120 rows)
    chunk_h = 5120
    num_chunks = int(np.ceil(total_h / chunk_h))
    print(f"⚙️  Memulai rasterisasi windowed ({num_chunks} strips @ {chunk_h} baris)...")

    with rasterio.open(out_kba, 'w', **profile) as dst_kba, \
         rasterio.open(out_kva, 'w', **profile) as dst_kva:

        for c_idx in range(num_chunks):
            r_start = c_idx * chunk_h
            r_len = min(chunk_h, total_h - r_start)
            
            top_y = maxy - r_start * res
            bot_y = top_y - r_len * res
            
            strip_box = box(minx, bot_y, maxx, top_y)
            matches = tree.query(strip_box, predicate='intersects')
            
            win = Window(col_off=0, row_off=r_start, width=total_w, height=r_len)
            strip_tf = from_origin(minx, top_y, res, res)
            
            if len(matches) == 0:
                empty = np.zeros((r_len, total_w), dtype=np.uint8)
                dst_kba.write(empty, 1, window=win)
                dst_kva.write(empty, 1, window=win)
            else:
                sub = gdf_3857.iloc[matches]
                shapes_kba = [(geom, val) for geom, val in zip(sub.geometry, sub['VAL_KBA']) if val > 0]
                shapes_kva = [(geom, val) for geom, val in zip(sub.geometry, sub['VAL_KVA']) if val > 0]
                
                arr_kba = rasterize(shapes_kba, out_shape=(r_len, total_w), transform=strip_tf, fill=0, dtype=np.uint8)
                arr_kva = rasterize(shapes_kva, out_shape=(r_len, total_w), transform=strip_tf, fill=0, dtype=np.uint8)
                
                dst_kba.write(arr_kba, 1, window=win)
                dst_kva.write(arr_kva, 1, window=win)

            print(f"  • Strip [{c_idx + 1:2d}/{num_chunks}] (Baris {r_start:,} s/d {r_start + r_len:,}) -> Selesai")

    # Simpan file legenda CSV
    df_leg_kba = pd.DataFrame(list(sorted(legend_kba.items())), columns=['Value', 'Keterangan_KBA'])
    df_leg_kva = pd.DataFrame(list(sorted(legend_kva.items())), columns=['Value', 'Keterangan_KVA'])
    df_leg_kba.to_csv('data/kba_kalbar_legend.csv', index=False)
    df_leg_kva.to_csv('data/kva_kalbar_legend.csv', index=False)

    size_kba_mb = os.path.getsize(out_kba) / (1024 * 1024)
    size_kva_mb = os.path.getsize(out_kva) / (1024 * 1024)

    print("\n" + "=" * 65)
    print("🎉 RASTERISASI KALIMANTAN BARAT SELESAI DENGAN SUKSES!")
    print(f"  • File Raster KBA : {out_kba} ({size_kba_mb:.2f} MB)")
    print(f"  • File Raster KVA : {out_kva} ({size_kva_mb:.2f} MB)")
    print(f"  • File Legenda KBA: data/kba_kalbar_legend.csv")
    print(f"  • File Legenda KVA: data/kva_kalbar_legend.csv")
    print(f"  • Waktu Pemrosesan: {time.time() - t_start:.2f} detik")
    print("=" * 65)

if __name__ == '__main__':
    main()
