import os
from pathlib import Path

# Workspace Root
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data" / "jlh_seamless"
CACHE_DIR = BASE_DIR / "WebGIS" / "cache" / "tiles"

# Layer mapping to TIF files in data/jlh_seamless/
LAYERS = {
    "pga": {
        "id": "pga",
        "name": "Pengaturan Tata Aliran Air (PGA)",
        "short_name": "Pengaturan Air",
        "code": "PGA",
        "file": DATA_DIR / "sumbar_2025_jlh_pga_seamless.tif",
        "weight_kba": 0.28,
        "weight_kva": 0.12,
        "weight_pl": 0.60,
        "color": "#0284c7",
        "desc": "Kapasitas ekosistem dalam menahan, meresapkan, dan mengatur debit tata air DAS serta mereduksi risiko banjir."
    },
    "phk": {
        "id": "phk",
        "name": "Pendukung Habitat & Kehati (PHK)",
        "short_name": "Habitat & Kehati",
        "code": "PHK",
        "file": DATA_DIR / "sumbar_2025_jlh_phk_seamless.tif",
        "weight_kba": 0.24,
        "weight_kva": 0.16,
        "weight_pl": 0.60,
        "color": "#059669",
        "desc": "Perlindungan keanekaragaman flora/fauna endemik, koridor jelajah satwa, dan cadangan plasma nutfah hutan alami."
    },
    "ppk": {
        "id": "ppk",
        "name": "Penyerap & Penyimpan Karbon (PPK)",
        "short_name": "Simpanan Karbon",
        "code": "PPK",
        "file": DATA_DIR / "sumbar_2025_jlh_ppk_seamless.tif",
        "weight_kba": 0.20,
        "weight_kva": 0.20,
        "weight_pl": 0.60,
        "color": "#16a34a",
        "desc": "Kapasitas rosot karbon biomasa atas tanah (kanopi) dan simpanan karbon organik tanah dalam mitigasi iklim."
    },
    "pya": {
        "id": "pya",
        "name": "Penyedia Air Bersih (PYA)",
        "short_name": "Penyedia Air",
        "code": "PYA",
        "file": DATA_DIR / "sumbar_2025_jlh_pya_seamless.tif",
        "weight_kba": 0.32,
        "weight_kva": 0.08,
        "weight_pl": 0.60,
        "color": "#06b6d4",
        "desc": "Ketersediaan kuantitas air permukaan, mata air alami, dan zona imbuhan air tanah hidrogeologis."
    },
    "pgn": {
        "id": "pgn",
        "name": "Penyedia Pangan Regio Sumatera (PGN)",
        "short_name": "Penyedia Pangan",
        "code": "PGN",
        "file": DATA_DIR / "sumbar_2025_jlh_pgn_seamless.tif",
        "weight_kba": 0.28,
        "weight_kva": 0.12,
        "weight_pl": 0.60,
        "color": "#d97706",
        "desc": "Daya dukung kesuburan tanah dataran fluvial/vulkanik untuk produksi komoditas pangan nabati dan perikanan darat."
    },
    "pku": {
        "id": "pku",
        "name": "Pengatur Kualitas Udara (PKU)",
        "short_name": "Kualitas Udara",
        "code": "PKU",
        "file": DATA_DIR / "sumbar_2025_jlh_pku_seamless.tif",
        "weight_kba": 0.15,
        "weight_kva": 0.25,
        "weight_pl": 0.60,
        "color": "#7c3aed",
        "desc": "Kemampuan tutupan vegetasi tajuk rapat dalam menyerap polutan, debu partikulat, dan suplai oksigen bersih."
    },
    "kba": {
        "id": "kba",
        "name": "Kawasan Bentang Alam (KBA)",
        "short_name": "Bentang Alam (KBA)",
        "code": "KBA",
        "file": DATA_DIR / "sumbar_2025_kba_seamless.tif",
        "color": "#8b5cf6",
        "desc": "Satuan morfogenesa fisik bentang alam, litologi geologi, dan kemiringan lereng."
    },
    "kva": {
        "id": "kva",
        "name": "Kawasan Vegetasi Alami (KVA)",
        "short_name": "Vegetasi Alami (KVA)",
        "code": "KVA",
        "file": DATA_DIR / "sumbar_2025_kva_seamless.tif",
        "color": "#10b981",
        "desc": "Zonasi integritas vegetasi asli alami penyangga ekologis setempat."
    }
}

# 5 Klasifikasi Nilai D3TLH
D3TLH_CLASSES = [
    {"class": "Sangat Tinggi", "min": 4.21, "max": 5.00, "color": "#15803d", "rgb": (21, 128, 61), "desc": "Kawasan Lindung Mutlak / Konservasi Utama"},
    {"class": "Tinggi", "min": 3.41, "max": 4.20, "color": "#65a30d", "rgb": (101, 163, 13), "desc": "Kawasan Penyangga Terbatas / Konservasi Air"},
    {"class": "Sedang", "min": 2.61, "max": 3.40, "color": "#ca8a04", "rgb": (202, 138, 4), "desc": "Kawasan Budidaya Terkendali & Berkelanjutan"},
    {"class": "Rendah", "min": 1.81, "max": 2.60, "color": "#ea580c", "rgb": (234, 88, 12), "desc": "Kawasan Terbangun Intensif / Butuh RTH"},
    {"class": "Sangat Rendah", "min": 1.00, "max": 1.80, "color": "#dc2626", "rgb": (220, 38, 38), "desc": "Kawasan Kritis Ekologis / Moratorium Alih Fungsi"}
]

# Bounds Sumatera Barat (WGS84 EPSG:4326)
SUMBAR_BOUNDS_WGS84 = [98.60, -3.50, 101.90, 0.95]
SUMBAR_CENTER = [100.65, -0.78]
