import mercantile
from .config import LAYERS, D3TLH_CLASSES
from .tile_renderer import get_dataset

def get_d3tlh_class(score: float):
    if score >= 4.21:
        return D3TLH_CLASSES[0]
    elif score >= 3.41:
        return D3TLH_CLASSES[1]
    elif score >= 2.61:
        return D3TLH_CLASSES[2]
    elif score >= 1.81:
        return D3TLH_CLASSES[3]
    else:
        return D3TLH_CLASSES[4]

def inspect_point(lng: float, lat: float, active_layer: str = "pga") -> dict:
    """Inspect exact pixel values from 0.5m GeoTIFF rasters at (lng, lat)."""
    # Convert WGS84 (lng, lat) to EPSG:3857 Web Mercator (x, y)
    x, y = mercantile.xy(lng, lat)

    results = {}
    for lid, linfo in LAYERS.items():
        ds = get_dataset(lid)
        if ds is not None:
            try:
                # Sample returns a generator of arrays
                sample_gen = ds.sample([(x, y)])
                val = float(next(sample_gen)[0])
                results[lid] = round(val, 2)
            except Exception as e:
                results[lid] = 0.0
        else:
            results[lid] = 0.0

    active_score = results.get(active_layer, results.get("pga", 0.0))
    cls_obj = get_d3tlh_class(active_score)

    # Estimate land cover score from JLH formula: JLH = (KBA*W_KBA) + (KVA*W_KVA) + (PL*0.6)
    kba_val = results.get("kba", 0.0)
    kva_val = results.get("kva", 0.0)
    w_kba = LAYERS.get(active_layer, {}).get("weight_kba", 0.28)
    w_kva = LAYERS.get(active_layer, {}).get("weight_kva", 0.12)
    w_pl = LAYERS.get(active_layer, {}).get("weight_pl", 0.60)

    pl_calc = 0.0
    if w_pl > 0 and active_score > 0:
        pl_calc = max(1.0, min(5.0, (active_score - (kba_val * w_kba) - (kva_val * w_kva)) / w_pl))

    pl_desc = "Vegetasi / Kanopi Rapat" if pl_calc >= 4.0 else "Pertanian / Perkebunan" if pl_calc >= 2.5 else "Pemukiman / Ruang Terbuka"

    return {
        "coords": {
            "lng": round(lng, 5),
            "lat": round(lat, 5),
            "x_mercator": round(x, 2),
            "y_mercator": round(y, 2)
        },
        "active_layer": active_layer,
        "score": active_score,
        "class_name": cls_obj["class"],
        "class_color": cls_obj["color"],
        "class_desc": cls_obj["desc"],
        "components": {
            "kba": round(kba_val, 2),
            "kva": round(kva_val, 2),
            "pl_calculated": round(pl_calc, 2),
            "land_cover_est": pl_desc
        },
        "all_indicators": {
            "pga": results.get("pga", 0.0),
            "phk": results.get("phk", 0.0),
            "ppk": results.get("ppk", 0.0),
            "pya": results.get("pya", 0.0),
            "pgn": results.get("pgn", 0.0),
            "pku": results.get("pku", 0.0)
        }
    }
