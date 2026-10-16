#!/usr/bin/env python3
"""
Script Python untuk Mengunduh Otomatis Data OSM (OpenStreetMap) Khusus Provinsi Sumatera Barat:
1. POI Fasilitas Umum: Rumah Sakit, Puskesmas, Sekolah, Pasar, Kantor Desa, Tempat Ibadah
2. Jaringan Jalan Utama & Pemukiman (untuk analisis aksesibilitas/isochrone)
"""

import os
import json
import requests
import geopandas as gpd
from shapely.geometry import Point, LineString

# Bounding box Sumatera Barat [South, West, North, East]
BBOX_SUMBAR = [-3.50, 98.60, 0.95, 101.90]

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

def fetch_poi_facilities(output_gpkg="data/poi_fasilitas_sumbar.gpkg"):
    print("=======================================================")
    print("Mengunduh POI Fasilitas Dasar se-Sumatera Barat via OSM")
    print("=======================================================")
    
    s, w, n, e = BBOX_SUMBAR
    query = f"""
    [out:json][timeout:180];
    (
      // Fasilitas Kesehatan
      node["amenity"~"hospital|clinic|doctors|pharmacy"]({s},{w},{n},{e});
      way["amenity"~"hospital|clinic|doctors|pharmacy"]({s},{w},{n},{e});
      
      // Fasilitas Pendidikan
      node["amenity"~"school|college|university|kindergarten"]({s},{w},{n},{e});
      way["amenity"~"school|college|university|kindergarten"]({s},{w},{n},{e});
      
      // Fasilitas Umum & Ekonomi
      node["amenity"~"marketplace|townhall|police|fire_station|place_of_worship"]({s},{w},{n},{e});
      way["amenity"~"marketplace|townhall|police|fire_station|place_of_worship"]({s},{w},{n},{e});
    );
    out center tags;
    """
    
    headers = {
        "User-Agent": "JLH_Spatial_Research_Sumbar/1.0 (contact: danang@kemenlh.go.id)"
    }
    
    print("Mengirim query ke Overpass API...", flush=True)
    endpoints = [
        "https://overpass-api.de/api/interpreter",
        "https://lz4.overpass-api.de/api/interpreter",
        "https://overpass.kumi.systems/api/interpreter"
    ]
    
    resp = None
    for ep in endpoints:
        try:
            print(f"Mencoba endpoint: {ep}...", flush=True)
            resp = requests.post(ep, data={"data": query}, headers=headers, timeout=120)
            if resp.status_code == 200:
                break
        except Exception as e:
            print(f"Gagal ke {ep}: {e}")
            
    if not resp or resp.status_code != 200:
        print(f"Error Overpass: {resp.status_code if resp else 'No response'}")
        return False
        
    data = resp.json()
    elements = data.get("elements", [])
    print(f"Total elemen ditemukan: {len(elements)}")
    
    records = []
    for el in elements:
        tags = el.get("tags", {})
        # Ambil koordinat titik (bisa dari node langsung atau center dari way)
        lat = el.get("lat") or el.get("center", {}).get("lat")
        lon = el.get("lon") or el.get("center", {}).get("lon")
        
        if not lat or not lon:
            continue
            
        amenity = tags.get("amenity", "other")
        category = "Lainnya"
        if amenity in ["hospital", "clinic", "doctors", "pharmacy"]:
            category = "Kesehatan"
        elif amenity in ["school", "college", "university", "kindergarten"]:
            category = "Pendidikan"
        elif amenity in ["marketplace"]:
            category = "Perekonomian/Pasar"
        elif amenity in ["townhall", "police", "fire_station"]:
            category = "Pemerintahan/Keamanan"
        elif amenity in ["place_of_worship"]:
            category = "Ibadah"
            
        records.append({
            "osm_id": el.get("id"),
            "osm_type": el.get("type"),
            "nama": tags.get("name", "Tanpa Nama"),
            "kategori": category,
            "tipe_fasilitas": amenity,
            "geometry": Point(lon, lat)
        })
        
    if not records:
        print("Tidak ada data yang diparsing.")
        return False
        
    gdf = gpd.GeoDataFrame(records, crs="EPSG:4326")
    os.makedirs(os.path.dirname(os.path.abspath(output_gpkg)), exist_ok=True)
    gdf.to_file(output_gpkg, driver="GPKG", layer="poi_fasilitas")
    print(f"[SUKSES] Tersimpan {len(gdf)} titik fasilitas ke: {output_gpkg}")
    return True

if __name__ == "__main__":
    fetch_poi_facilities()
