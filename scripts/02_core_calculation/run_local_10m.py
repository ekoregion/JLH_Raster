import rasterio
from rasterio.windows import Window
from rasterio.warp import reproject, Resampling
import numpy as np
import time
import os

print("===========================================================")
print("MEMULAI MCE REALISTIS QUICK VIEW (10 METER) DI LOKAL")
print("===========================================================")

# 1. Path input lokal
f_pga = 'data/jlh_seamless/sumbar_2025_jlh_pga_seamless.tif'
f_pya = 'data/jlh_seamless/sumbar_2025_jlh_pya_seamless.tif'
f_pgn = 'data/jlh_seamless/sumbar_2025_jlh_pgn_seamless.tif'
f_pku = 'data/jlh_seamless/sumbar_2025_jlh_pku_seamless.tif'

f_longsor = 'data/jlh_seamless/Bahaya Bencana/indeks_tanah_longsor.tiff'
f_banjir = 'data/jlh_seamless/Bahaya Bencana/indeks_bahaya_banjir.tiff'
f_galodo = 'data/jlh_seamless/Bahaya Bencana/indeks_bahaya_banjir_bandang.tiff'

out_tif_10m = 'data/jlh_seamless/sumbar_2025_kesesuaian_relokasi_realistic_10m.tif'

src_pga = rasterio.open(f_pga)
src_pya = rasterio.open(f_pya)
src_pgn = rasterio.open(f_pgn)
src_pku = rasterio.open(f_pku)

src_ls = rasterio.open(f_longsor)
src_bj = rasterio.open(f_banjir)
src_gd = rasterio.open(f_galodo)

scale = 20
w_10 = src_pga.width // scale
h_10 = src_pga.height // scale
trans_10 = src_pga.transform * src_pga.transform.scale(scale, scale)

profile_10m = {
    'driver': 'GTiff',
    'dtype': 'float32',
    'nodata': 0.0,
    'width': w_10,
    'height': h_10,
    'count': 1,
    'crs': src_pga.crs,
    'transform': trans_10,
    'compress': 'lerc_zstd',
    'max_z_error': 0.005,
    'tiled': True,
    'blockxsize': 512,
    'blockysize': 512
}

print(f"Master Grid 10m: {w_10} x {h_10} piksel")

lut_pya = np.array([0.0, 0.0, 0.25, 0.50, 0.75, 1.00], dtype=np.float32)
lut_pgn = np.array([0.0, 0.0, 0.25, 0.50, 0.75, 1.00], dtype=np.float32)
lut_pga = np.array([0.0, 0.0, 0.20, 1.00, 0.50, 0.00], dtype=np.float32)
lut_pku = np.array([0.0, 0.0, 0.20, 1.00, 0.50, 0.00], dtype=np.float32)

def warp_to_10m(src_haz):
    data_10m = np.zeros((h_10, w_10), dtype=np.float32)
    reproject(
        source=rasterio.band(src_haz, 1),
        destination=data_10m,
        src_transform=src_haz.transform,
        src_crs=src_haz.crs,
        dst_transform=trans_10,
        dst_crs=src_pga.crs,
        resampling=Resampling.nearest
    )
    return np.where(data_10m >= 3.0e38, 0.0, data_10m)

print("[1/4] Menyelaraskan 3 Peta Bahaya ke Grid 10m...")
h_ls_10m = warp_to_10m(src_ls)
h_bj_10m = warp_to_10m(src_bj)
h_gd_10m = warp_to_10m(src_gd)
print("Selesai reproject 3 peta bahaya!")

def get_hazard_factor(h_arr):
    f = np.zeros_like(h_arr, dtype=np.float32)
    f[h_arr <= 0.33] = 1.0
    f[(h_arr > 0.33) & (h_arr <= 0.66)] = 0.5
    f[h_arr > 0.66] = 0.0
    return f

s_ls_10m = get_hazard_factor(h_ls_10m)
s_bj_10m = get_hazard_factor(h_bj_10m)
s_gd_10m = get_hazard_factor(h_gd_10m)
gatekeeper_safe = (h_ls_10m <= 0.66) & (h_gd_10m <= 0.66) & (h_bj_10m <= 0.66)

print("[2/4] Menghitung MCE Bobot Realistis per chunk 10m...")
start_time = time.time()
step = 512
num_steps = (h_10 + step - 1) // step

with rasterio.open(out_tif_10m, 'w', **profile_10m) as dst:
    for idx in range(num_steps):
        r_10 = idx * step
        curr_h_10 = min(step, h_10 - r_10)
        
        # Koordinat di 0.5m
        r_05 = r_10 * scale
        curr_h_05 = curr_h_10 * scale
        win_05 = Window(0, r_05, src_pga.width, curr_h_05)
        
        # Subsample piksel ke-20
        d_pga = src_pga.read(1, window=win_05)[::scale, ::scale][:curr_h_10, :w_10]
        
        mask_land = d_pga > 0
        if not np.any(mask_land):
            dst.write(np.zeros((curr_h_10, w_10), dtype=np.float32), 1, window=Window(0, r_10, w_10, curr_h_10))
            continue
            
        d_pya = src_pya.read(1, window=win_05)[::scale, ::scale][:curr_h_10, :w_10]
        d_pgn = src_pgn.read(1, window=win_05)[::scale, ::scale][:curr_h_10, :w_10]
        d_pku = src_pku.read(1, window=win_05)[::scale, ::scale][:curr_h_10, :w_10]
        
        sp_pya = lut_pya[np.clip(d_pya.astype(np.int8), 0, 5)]
        sp_pga = lut_pga[np.clip(d_pga.astype(np.int8), 0, 5)]
        sp_pgn = lut_pgn[np.clip(d_pgn.astype(np.int8), 0, 5)]
        sp_pku = lut_pku[np.clip(d_pku.astype(np.int8), 0, 5)]
        
        slice_ls = s_ls_10m[r_10:r_10+curr_h_10, :w_10]
        slice_bj = s_bj_10m[r_10:r_10+curr_h_10, :w_10]
        slice_gd = s_gd_10m[r_10:r_10+curr_h_10, :w_10]
        slice_safe = gatekeeper_safe[r_10:r_10+curr_h_10, :w_10]
        
        score_calc = (
            (0.200 * slice_ls) +
            (0.150 * slice_bj) +
            (0.150 * slice_gd) +
            (0.175 * sp_pya) +
            (0.100 * sp_pga) +
            (0.175 * sp_pgn) +
            (0.050 * sp_pku)
        )
        
        score_final = np.where(mask_land & slice_safe, score_calc, 0.0).astype(np.float32)
        dst.write(score_final, 1, window=Window(0, r_10, w_10, curr_h_10))
        
        if (idx + 1) % 10 == 0 or (idx + 1) == num_steps:
            elapsed = (time.time() - start_time) / 60.0
            print(f"[{((idx+1)/num_steps)*100:5.1f}%] Selesai chunk {idx+1}/{num_steps} | Waktu: {elapsed:.1f}m")

print("[3/4] Membangun overviews internal 10m...")
with rasterio.open(out_tif_10m, 'r+') as dst:
    dst.build_overviews([2, 4, 8, 16], Resampling.nearest)
    dst.update_tags(ns='rio_overview', resampling='nearest')

print(f"[4/4] SUKSES! File tersimpan di: {out_tif_10m}")
