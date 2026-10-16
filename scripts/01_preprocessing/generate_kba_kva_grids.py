#!/usr/bin/env python3
"""
Pemodelan Raster KBA & KVA Sumatera Barat (Format COG, 8-bit unsigned, kompresi LZW)
Resolusi 0.5 x 0.5 meter, CRS EPSG:3857, Tiled 512x512.
Nilai piksel KBA & KVA disesuaikan dengan kolom 'Value' pada Skor_JLH_2026.xlsx.
Mendukung:
  1. Mode 'lulc': Memproses grid sesuai file tutupan lahan di folder class/ (80 tile)
  2. Mode 'all' : Men-generate seluruh grid se-Sumatera Barat (~3.126 tile daratan)
  3. Pembuatan otomatis Virtual Raster (.vrt) untuk QGIS / ArcGIS
"""

import os
import glob
import time
import argparse
import openpyxl
import numpy as np
import rasterio
from rasterio.features import rasterize
from rasterio.transform import from_origin
from shapely.geometry import box
import pyogrio
import geopandas as gpd
import xml.etree.ElementTree as ET

# Konfigurasi Grid LULC Acuan
REF_X = 11110809.99449189      # Origin X (Top-Left) dari sumbar_50cm_0001
REF_Y = 101049.75140393605     # Origin Y (Top-Left) dari sumbar_50cm_0001
STEP_M = 3974.7246             # Ukuran grid per tile (meter)
TILE_W = 7949                  # Lebar piksel (7949 * 0.5m = 3974.5m)
TILE_H = 7949                  # Tinggi piksel
RES = 0.5                      # Resolusi 0.5 meter

def load_scoring_maps(excel_path):
    wb = openpyxl.load_workbook(excel_path, data_only=True)
    
    # 1. KBA Map
    ws_kba = wb['Skor KBA']
    kba_dict = {}
    for r in ws_kba.iter_rows(values_only=True):
        if r[0] is not None and str(r[0]).strip().isdigit() and r[1] is not None:
            kba_dict[str(r[1]).strip().lower()] = int(r[0])
            
    # 2. KVA Map
    ws_kva = wb['Skor KVA']
    kva_dict = {}
    for r in ws_kva.iter_rows(values_only=True):
        if r[0] is not None and str(r[0]).strip().isdigit() and r[1] is not None:
            kva_dict[str(r[1]).strip().lower()] = int(r[0])
            
    return kba_dict, kva_dict

def normalize_kba(name, kba_dict):
    if not name:
        return 0
    clean = str(name).strip().lower()
    if clean in kba_dict:
        return kba_dict[clean]
    if 'danau' in clean or 'sungai' in clean:
        return 1  # Danau / Tubuh Air (Value 1)
    if 'fluvial bermaterial aluvium' in clean:
        return 2  # Dataran fluvial bermaterial aluvium (Value 2)
    return 0

def normalize_kva(name, kva_dict):
    if not name:
        return 0
    clean = str(name).strip().lower().replace('bentang alam', 'bentangalam')
    if clean in kva_dict:
        return kva_dict[clean]
    if 'danau' in clean:
        return 32  # Vegetasi hutan danau (Value 32)
    if 'sungai' in clean:
        return 58  # Vegetasi hutan tepian sungai air tawar (Value 58)
    return 0

def create_mosaic_vrt(tif_list, output_vrt_path):
    if not tif_list:
        return
    
    meta_list = []
    min_x, max_x = float('inf'), float('-inf')
    min_y, max_y = float('inf'), float('-inf')
    crs_wkt = None
    res_x, res_y = RES, RES

    for p in tif_list:
        with rasterio.open(p) as src:
            b = src.bounds
            min_x = min(min_x, b.left)
            max_x = max(max_x, b.right)
            min_y = min(min_y, b.bottom)
            max_y = max(max_y, b.top)
            if crs_wkt is None:
                crs_wkt = src.crs.to_wkt()
                res_x = src.transform.a
                res_y = abs(src.transform.e)
            meta_list.append({
                'path': p,
                'rel_path': os.path.relpath(p, os.path.dirname(output_vrt_path)),
                'bounds': b,
                'width': src.width,
                'height': src.height
            })
            
    vrt_width = int(round((max_x - min_x) / res_x))
    vrt_height = int(round((max_y - min_y) / res_y))
    geotransform = f'{min_x}, {res_x}, 0.0, {max_y}, 0.0, {-res_y}'

    root = ET.Element('VRTDataset', rasterXSize=str(vrt_width), rasterYSize=str(vrt_height))
    srs = ET.SubElement(root, 'SRS', dataAxisToSRSAxisMapping='1,2')
    srs.text = crs_wkt
    gt = ET.SubElement(root, 'GeoTransform')
    gt.text = geotransform

    band = ET.SubElement(root, 'VRTRasterBand', dataType='Byte', band='1')
    nodata = ET.SubElement(band, 'NoDataValue')
    nodata.text = '0'
    color = ET.SubElement(band, 'ColorInterp')
    color.text = 'Gray'

    for m in meta_list:
        dst_x = int(round((m['bounds'].left - min_x) / res_x))
        dst_y = int(round((max_y - m['bounds'].top) / res_y))
        w = m['width']
        h = m['height']

        cs = ET.SubElement(band, 'ComplexSource')
        sf = ET.SubElement(cs, 'SourceFilename', relativeToVRT='1')
        sf.text = m['rel_path']
        sb = ET.SubElement(cs, 'SourceBand')
        sb.text = '1'
        sp = ET.SubElement(cs, 'SourceProperties', RasterXSize=str(w), RasterYSize=str(h), DataType='Byte', BlockXSize='512', BlockYSize='512')
        sr = ET.SubElement(cs, 'SrcRect', xOff='0', yOff='0', xSize=str(w), ySize=str(h))
        dr = ET.SubElement(cs, 'DstRect', xOff=str(dst_x), yOff=str(dst_y), xSize=str(w), ySize=str(h))
        nd = ET.SubElement(cs, 'NODATA')
        nd.text = '0'

    tree = ET.ElementTree(root)
    tree.write(output_vrt_path, encoding='utf-8', xml_declaration=False)
    print(f"🗺️  VRT Terbuat: {output_vrt_path} ({vrt_width:,} x {vrt_height:,} piksel)")

def rasterize_single_tile(out_kba_path, out_kva_path, bounds, transform, width, height, crs, gdf_tree, gdf_3857, kba_dict, kva_dict):
    if os.path.exists(out_kba_path) and os.path.exists(out_kva_path):
        return 'skip'

    tile_geom = box(bounds[0], bounds[1], bounds[2], bounds[3])
    candidate_idx = gdf_tree.query(tile_geom, predicate='intersects')

    profile = {
        'driver': 'GTiff',
        'dtype': rasterio.uint8,
        'nodata': 0,
        'width': width,
        'height': height,
        'count': 1,
        'crs': crs,
        'transform': transform,
        'compress': 'lzw',
        'tiled': True,
        'blockxsize': 512,
        'blockysize': 512
    }

    if len(candidate_idx) == 0:
        empty_arr = np.zeros((height, width), dtype=np.uint8)
        with rasterio.open(out_kba_path, 'w', **profile) as dst:
            dst.write(empty_arr, 1)
        with rasterio.open(out_kva_path, 'w', **profile) as dst:
            dst.write(empty_arr, 1)
        return 'empty'

    sub_gdf = gdf_3857.iloc[candidate_idx]

    kba_shapes = [(geom, normalize_kba(row['KBA_250'], kba_dict)) 
                  for geom, (_, row) in zip(sub_gdf.geometry, sub_gdf.iterrows())]
    kva_shapes = [(geom, normalize_kva(row['KVA_250'], kva_dict)) 
                  for geom, (_, row) in zip(sub_gdf.geometry, sub_gdf.iterrows())]

    kba_arr = rasterize(kba_shapes, out_shape=(height, width), transform=transform, fill=0, dtype=np.uint8)
    kva_arr = rasterize(kva_shapes, out_shape=(height, width), transform=transform, fill=0, dtype=np.uint8)

    with rasterio.open(out_kba_path, 'w', **profile) as dst:
        dst.write(kba_arr, 1)
    with rasterio.open(out_kva_path, 'w', **profile) as dst:
        dst.write(kva_arr, 1)

    return 'processed'

def main():
    parser = argparse.ArgumentParser(description="Rasterize KBA and KVA to COG tiles")
    parser.add_argument('--mode', choices=['lulc', 'all'], default='lulc',
                        help="'lulc' untuk 80 grid LULC di class/, 'all' untuk seluruh Sumatera Barat (~3.126 grid)")
    parser.add_argument('--limit', type=int, default=None,
                        help="Batasan jumlah grid yang diproses (opsional untuk testing)")
    args = parser.parse_args()

    excel_path = 'data/Skor_JLH_2026.xlsx'
    gdb_path = 'data/UE_Verlap_Sumbar.gdb'
    out_dir_kba = 'data/01_raster/kba'
    out_dir_kva = 'data/01_raster/kva'

    os.makedirs(out_dir_kba, exist_ok=True)
    os.makedirs(out_dir_kva, exist_ok=True)

    print("=" * 60)
    print("🌲 GENERATOR RASTER KBA & KVA SUMATERA BARAT (COG 0.5M)")
    print("=" * 60)

    print("📖 Membaca tabel skor dari Skor_JLH_2026.xlsx...")
    kba_dict, kva_dict = load_scoring_maps(excel_path)
    print(f"  • Kelas KBA terpetakan: {len(kba_dict)}")
    print(f"  • Kelas KVA terpetakan: {len(kva_dict)}")

    print("\n🗺️  Membaca dan mereprojeksi poligon UE_Hasil_Verlap_V7 ke EPSG:3857...")
    gdf = pyogrio.read_dataframe(gdb_path, layer='UE_Hasil_Verlap_V7')
    gdf_3857 = gdf.to_crs('EPSG:3857')
    print(f"  • Total poligon: {len(gdf_3857):,}")

    print("🌲 Membangun spatial index (STRtree)...")
    gdf_tree = gdf_3857.sindex
    crs_3857 = gdf_3857.crs

    t0 = time.time()
    processed, skipped = 0, 0

    if args.mode == 'lulc':
        grid_files = sorted(glob.glob('class/sumbar_50cm_*_multiscale_lulc.tif'))
        if args.limit:
            grid_files = grid_files[:args.limit]
            
        print(f"\n🚀 Memproses {len(grid_files)} grid LULC dari folder class/...")
        for i, gf in enumerate(grid_files, 1):
            bname = os.path.basename(gf)
            kba_name = bname.replace('_multiscale_lulc.tif', '_kba.tif')
            kva_name = bname.replace('_multiscale_lulc.tif', '_kva.tif')
            kba_out = os.path.join(out_dir_kba, kba_name)
            kva_out = os.path.join(out_dir_kva, kva_name)

            with rasterio.open(gf) as src:
                b = (src.bounds.left, src.bounds.bottom, src.bounds.right, src.bounds.top)
                tf = src.transform
                w, h = src.width, src.height

            st = rasterize_single_tile(kba_out, kva_out, b, tf, w, h, crs_3857, gdf_tree, gdf_3857, kba_dict, kva_dict)
            if st == 'skip':
                skipped += 1
            else:
                processed += 1

            if i % 10 == 0 or i == len(grid_files):
                print(f"  [{i}/{len(grid_files)}] {bname} -> Done ({time.time() - t0:.1f}s)")

    elif args.mode == 'all':
        total_bounds = gdf_3857.total_bounds
        col_min = int(np.floor((total_bounds[0] - REF_X) / STEP_M))
        col_max = int(np.ceil((total_bounds[2] - REF_X) / STEP_M))
        row_min = int(np.floor((REF_Y - total_bounds[3]) / STEP_M))
        row_max = int(np.ceil((REF_Y - total_bounds[1]) / STEP_M))

        print(f"\n🌐 Menemukan grid yang bersinggungan dengan daratan Sumbar (Cols {col_min}..{col_max}, Rows {row_min}..{row_max})...")
        active_tiles = []
        for r in range(row_min, row_max + 1):
            y_top = REF_Y - r * STEP_M
            y_bot = y_top - STEP_M
            for c in range(col_min, col_max + 1):
                x_left = REF_X + c * STEP_M
                x_right = x_left + STEP_M
                tile_box = box(x_left, y_bot, x_right, y_top)
                candidates = gdf_tree.query(tile_box, predicate='intersects')
                if len(candidates) > 0:
                    active_tiles.append((c, r, x_left, y_top, y_bot, x_right))

        if args.limit:
            active_tiles = active_tiles[:args.limit]

        print(f"  • Total grid aktif yang akan diproses: {len(active_tiles):,} tile")
        print("\n🚀 Memulai pemrosesan grid se-Sumatera Barat...")

        for i, (c, r, x0, y0, y1, x1) in enumerate(active_tiles, 1):
            # Penamaan berbasis indeks baris-kolom terstandar
            tile_tag = f"r{r:+04d}_c{c:+04d}".replace("+", "p").replace("-", "m")
            kba_name = f"sumbar_50cm_{tile_tag}_kba.tif"
            kva_name = f"sumbar_50cm_{tile_tag}_kva.tif"
            kba_out = os.path.join(out_dir_kba, kba_name)
            kva_out = os.path.join(out_dir_kva, kva_name)

            tf = from_origin(x0, y0, RES, RES)
            bounds = (x0, y1, x0 + TILE_W * RES, y0)

            st = rasterize_single_tile(kba_out, kva_out, bounds, tf, TILE_W, TILE_H, crs_3857, gdf_tree, gdf_3857, kba_dict, kva_dict)
            if st == 'skip':
                skipped += 1
            else:
                processed += 1

            if i % 100 == 0 or i == len(active_tiles):
                elapsed = time.time() - t0
                speed = i / elapsed if elapsed > 0 else 0
                remaining = (len(active_tiles) - i) / speed if speed > 0 else 0
                print(f"  [{i:,}/{len(active_tiles):,}] Grid {tile_tag} -> Selesai ({elapsed:.1f}s, est sisa: {remaining/60:.1f} mnt)")

    print(f"\n✅ Pemrosesan raster selesai!")
    print(f"  • Baru diproses: {processed:,} tile")
    print(f"  • Dilewati (ada) : {skipped:,} tile")
    print(f"  • Waktu total  : {time.time() - t0:.2f} detik")

    print("\n📦 Membangun Virtual Raster (VRT)...")
    all_kba = sorted(glob.glob(os.path.join(out_dir_kba, '*.tif')))
    all_kva = sorted(glob.glob(os.path.join(out_dir_kva, '*.tif')))
    vrt_kba_path = os.path.join('data/01_raster', 'kba_sumbar_mosaic.vrt')
    vrt_kva_path = os.path.join('data/01_raster', 'kva_sumbar_mosaic.vrt')

    create_mosaic_vrt(all_kba, vrt_kba_path)
    create_mosaic_vrt(all_kva, vrt_kva_path)
    print("🎉 SEMUA PROSES SELESAI DENGAN SUKSES!")

if __name__ == '__main__':
    main()
