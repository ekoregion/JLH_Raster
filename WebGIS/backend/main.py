import shutil
from typing import Optional, Dict, Any
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Response, Query
from fastapi.middleware.cors import CORSMiddleware
from .config import LAYERS, D3TLH_CLASSES, SUMBAR_BOUNDS_WGS84, SUMBAR_CENTER, CACHE_DIR
from .tile_renderer import render_tile
from .inspector import inspect_point
from spatial_engine.site_analyzer import SiteAnalyzer
from spatial_engine.trajectory_simulator import TrajectorySimulator

site_analyzer = SiteAnalyzer()
trajectory_simulator = TrajectorySimulator()

class SiteAnalysisRequest(BaseModel):
    geojson: Dict[str, Any]
    jenis_kegiatan: Optional[str] = "Pembangunan Kawasan & Fasilitas"

class TrajectorySimulationRequest(BaseModel):
    geojson: Dict[str, Any]
    jenis_kegiatan: Optional[str] = "Pembangunan Kawasan & Fasilitas"
    custom_params: Optional[Dict[str, Any]] = None

app = FastAPI(
    title="WebGIS JLH Sumatera Barat API",
    description="High-performance backend for Jasa Lingkungan Hidup (JLH) 0.5m GeoTIFF visualization",
    version="2.0.0"
)

# Enable CORS for frontend Vite dev server & production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 19 Kabupaten / Kota Sumatera Barat Reference Data
REGENCIES_DATA = [
    {"name": "Kab. Agam", "lat": -0.25, "lng": 100.18, "area_ha": 180430, "pga": 3.72, "phk": 3.95, "ppk": 3.81, "pya": 3.65, "pgn": 3.30, "pku": 3.88},
    {"name": "Kab. Tanah Datar", "lat": -0.45, "lng": 100.58, "area_ha": 133600, "pga": 3.55, "phk": 3.60, "ppk": 3.48, "pya": 3.40, "pgn": 3.52, "pku": 3.66},
    {"name": "Kab. Pesisir Selatan", "lat": -1.35, "lng": 100.57, "area_ha": 574989, "pga": 3.68, "phk": 4.12, "ppk": 3.94, "pya": 3.70, "pgn": 3.12, "pku": 3.95},
    {"name": "Kab. Pasaman", "lat": 0.35, "lng": 100.12, "area_ha": 394763, "pga": 3.80, "phk": 4.05, "ppk": 3.88, "pya": 3.75, "pgn": 3.08, "pku": 3.92},
    {"name": "Kab. Pasaman Barat", "lat": 0.18, "lng": 99.80, "area_ha": 388777, "pga": 3.35, "phk": 3.52, "ppk": 3.41, "pya": 3.30, "pgn": 3.45, "pku": 3.60},
    {"name": "Kab. Solok", "lat": -0.95, "lng": 100.75, "area_ha": 373800, "pga": 3.60, "phk": 3.85, "ppk": 3.72, "pya": 3.55, "pgn": 3.40, "pku": 3.78},
    {"name": "Kab. Solok Selatan", "lat": -1.40, "lng": 101.18, "area_ha": 334620, "pga": 3.75, "phk": 4.10, "ppk": 3.96, "pya": 3.68, "pgn": 2.95, "pku": 3.98},
    {"name": "Kab. Sijunjung", "lat": -0.68, "lng": 101.32, "area_ha": 313080, "pga": 3.42, "phk": 3.70, "ppk": 3.58, "pya": 3.32, "pgn": 3.20, "pku": 3.65},
    {"name": "Kab. Dharmasraya", "lat": -1.05, "lng": 101.62, "area_ha": 296113, "pga": 3.10, "phk": 3.25, "ppk": 3.18, "pya": 3.05, "pgn": 3.38, "pku": 3.42},
    {"name": "Kab. Lima Puluh Kota", "lat": -0.05, "lng": 100.65, "area_ha": 335430, "pga": 3.65, "phk": 3.90, "ppk": 3.76, "pya": 3.58, "pgn": 3.25, "pku": 3.82},
    {"name": "Kab. Padang Pariaman", "lat": -0.60, "lng": 100.25, "area_ha": 132870, "pga": 3.28, "phk": 3.35, "ppk": 3.26, "pya": 3.20, "pgn": 3.60, "pku": 3.50},
    {"name": "Kab. Kepulauan Mentawai", "lat": -1.95, "lng": 99.45, "area_ha": 601135, "pga": 3.85, "phk": 4.35, "ppk": 4.15, "pya": 3.80, "pgn": 2.80, "pku": 4.20},
    {"name": "Kota Padang", "lat": -0.95, "lng": 100.35, "area_ha": 69496, "pga": 2.85, "phk": 2.90, "ppk": 2.75, "pya": 2.70, "pgn": 2.50, "pku": 2.95},
    {"name": "Kota Bukittinggi", "lat": -0.30, "lng": 100.37, "area_ha": 2524, "pga": 2.45, "phk": 2.30, "ppk": 2.20, "pya": 2.40, "pgn": 2.10, "pku": 2.60},
    {"name": "Kota Payakumbuh", "lat": -0.22, "lng": 100.63, "area_ha": 8043, "pga": 2.70, "phk": 2.60, "ppk": 2.50, "pya": 2.65, "pgn": 2.80, "pku": 2.85},
    {"name": "Kota Pariaman", "lat": -0.62, "lng": 100.12, "area_ha": 7336, "pga": 2.60, "phk": 2.45, "ppk": 2.40, "pya": 2.50, "pgn": 2.90, "pku": 2.75},
    {"name": "Kota Solok", "lat": -0.80, "lng": 100.65, "area_ha": 5764, "pga": 2.65, "phk": 2.55, "ppk": 2.45, "pya": 2.60, "pgn": 2.95, "pku": 2.80},
    {"name": "Kota Sawahlunto", "lat": -0.68, "lng": 100.78, "area_ha": 27345, "pga": 3.20, "phk": 3.30, "ppk": 3.15, "pya": 3.10, "pgn": 2.75, "pku": 3.35},
    {"name": "Kota Padang Panjang", "lat": -0.47, "lng": 100.40, "area_ha": 2300, "pga": 2.90, "phk": 2.80, "ppk": 2.65, "pya": 2.85, "pgn": 2.40, "pku": 3.05}
]

@app.get("/")
def root():
    return {
        "status": "online",
        "service": "WebGIS JLH Sumatera Barat API (FastAPI + MapLibre GL)",
        "resolution": "0.5m",
        "tile_endpoint": "/tiles/{layer}/{z}/{x}/{y}.png",
        "inspect_endpoint": "/api/inspect?lng={lng}&lat={lat}&layer={layer}"
    }

@app.get("/api/config")
def get_config():
    layers_clean = {}
    for lid, linfo in LAYERS.items():
        layers_clean[lid] = {
            "id": linfo["id"],
            "name": linfo["name"],
            "short_name": linfo["short_name"],
            "code": linfo["code"],
            "color": linfo["color"],
            "desc": linfo["desc"],
            "weight_kba": linfo.get("weight_kba", 0),
            "weight_kva": linfo.get("weight_kva", 0),
            "weight_pl": linfo.get("weight_pl", 0)
        }

    return {
        "bounds": SUMBAR_BOUNDS_WGS84,
        "center": SUMBAR_CENTER,
        "layers": layers_clean,
        "d3tlh_classes": D3TLH_CLASSES
    }

@app.get("/api/regencies")
def get_regencies():
    return REGENCIES_DATA

@app.get("/api/inspect")
def inspect_coordinates(
    lng: float = Query(..., description="Longitude in decimal degrees (e.g. 100.5)"),
    lat: float = Query(..., description="Latitude in decimal degrees (e.g. -0.78)"),
    layer: str = Query("pga", description="Active layer ID (pga, phk, ppk, pya, pgn, pku, kba, kva)")
):
    """Query exact pixel value at 0.5m GeoTIFF for all JLH indicators."""
    return inspect_point(lng, lat, layer)

@app.get("/tiles/{layer_id}/{z}/{x}/{y}.png")
def get_tile(layer_id: str, z: int, x: int, y: int):
    """Dynamic XYZ Tile Service for MapLibre GL."""
    if layer_id not in LAYERS:
        raise HTTPException(status_code=404, detail=f"Layer {layer_id} not found")

    png_bytes = render_tile(layer_id, z, x, y)
    return Response(
        content=png_bytes,
        media_type="image/png",
        headers={
            "Cache-Control": "public, max-age=86400",
            "Access-Control-Allow-Origin": "*"
        }
    )

@app.post("/api/cache/clear")
def clear_cache():
    if CACHE_DIR.exists():
        shutil.rmtree(CACHE_DIR)
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
    return {"message": "Tile cache cleared successfully"}

@app.post("/api/screening/analyze")
def analyze_site_screening(payload: SiteAnalysisRequest):
    """
    Penapisan Lingkungan Hidup Cepat Berbasis Geometri Tapak (AMDAL / KKPR).
    Mengekstrak statistik raster LULC & JLH, mengevaluasi status D3TLH per PP 26/2025,
    dan menghasilkan preskripsi mitigasi wajib.
    """
    try:
        result = site_analyzer.analyze_geojson(
            payload.geojson,
            jenis_kegiatan=payload.jenis_kegiatan or "Pembangunan Kawasan & Fasilitas"
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Gagal menganalisis tapak: {str(e)}")

@app.post("/api/screening/simulate")
def simulate_site_trajectory(payload: TrajectorySimulationRequest):
    """
    Simulasi Dinamika Spasial Multi-Temporal (2025, 2027, 2035).
    Memproyeksikan trajektori kinerja JLH dan status D3TLH di bawah 3 skenario:
    1. Business-As-Usual (BAU)
    2. Unmitigated Development (Tanpa Mitigasi Ketat)
    3. Prescriptive / Sustainable Mitigation (Mitigasi Penuh PP 26/2025)
    """
    try:
        analysis = site_analyzer.analyze_geojson(
            payload.geojson,
            jenis_kegiatan=payload.jenis_kegiatan or "Pembangunan Kawasan & Fasilitas"
        )
        trajectory = trajectory_simulator.simulate(analysis, payload.custom_params)
        return {
            "analisis_tapak": analysis,
            "simulasi_trajektori": trajectory
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Gagal melakukan simulasi trajektori: {str(e)}")
