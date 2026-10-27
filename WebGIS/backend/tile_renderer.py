import io
import os
from pathlib import Path
import rasterio
from rasterio.windows import from_bounds
import mercantile
import numpy as np
from PIL import Image
from .config import LAYERS, CACHE_DIR

# Keep open dataset handles for performance
_DATASETS = {}

def get_dataset(layer_id: str):
    if layer_id not in LAYERS:
        return None
    if layer_id not in _DATASETS:
        file_path = LAYERS[layer_id]["file"]
        if not file_path.exists():
            return None
        _DATASETS[layer_id] = rasterio.open(str(file_path))
    return _DATASETS[layer_id]

# Transparent 256x256 PNG for empty/out-of-bound tiles
_EMPTY_TILE = None
def get_empty_tile() -> bytes:
    global _EMPTY_TILE
    if _EMPTY_TILE is None:
        img = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        _EMPTY_TILE = buf.getvalue()
    return _EMPTY_TILE

def render_tile(layer_id: str, z: int, x: int, y: int) -> bytes:
    """Render a 256x256 PNG tile for the given layer and XYZ coordinates."""
    # Check disk cache first
    cache_path = CACHE_DIR / layer_id / str(z) / str(x) / f"{y}.png"
    if cache_path.exists():
        with open(cache_path, "rb") as f:
            return f.read()

    ds = get_dataset(layer_id)
    if ds is None:
        return get_empty_tile()

    # Get Web Mercator bounds for the XYZ tile (EPSG:3857)
    tile = mercantile.Tile(x, y, z)
    bounds = mercantile.xy_bounds(tile)

    # Check intersection with raster bounds
    rb = ds.bounds
    if (bounds.right < rb.left or bounds.left > rb.right or
        bounds.top < rb.bottom or bounds.bottom > rb.top):
        return get_empty_tile()

    # Calculate window in raster coordinates
    window = from_bounds(bounds.left, bounds.bottom, bounds.right, bounds.top, ds.transform)

    try:
        data = ds.read(1, window=window, out_shape=(256, 256), boundless=True, fill_value=0.0)
    except Exception as e:
        print(f"Error reading window for {layer_id} {z}/{x}/{y}: {e}")
        return get_empty_tile()

    # If all pixels are nodata / 0, return empty
    if np.all(data == 0):
        return get_empty_tile()

    # Create RGBA image array
    rgba = np.zeros((256, 256, 4), dtype=np.uint8)

    # Color mapping for D3TLH / JLH (1.00 - 5.00)
    # Sangat Tinggi (4.21 - 5.00): #15803d
    mask5 = (data >= 4.21)
    rgba[mask5] = [21, 128, 61, 235]

    # Tinggi (3.41 - 4.20): #65a30d
    mask4 = (data >= 3.41) & (data < 4.21)
    rgba[mask4] = [101, 163, 13, 235]

    # Sedang (2.61 - 3.40): #ca8a04
    mask3 = (data >= 2.61) & (data < 3.41)
    rgba[mask3] = [202, 138, 4, 235]

    # Rendah (1.81 - 2.60): #ea580c
    mask2 = (data >= 1.81) & (data < 2.61)
    rgba[mask2] = [234, 88, 12, 235]

    # Sangat Rendah (0.50 - 1.80): #dc2626
    mask1 = (data >= 0.50) & (data < 1.81)
    rgba[mask1] = [220, 38, 38, 235]

    # Everything else (< 0.50 or 0) remains (0, 0, 0, 0) transparent

    img = Image.fromarray(rgba, mode="RGBA")
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    png_bytes = buf.getvalue()

    # Save to disk cache
    try:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        with open(cache_path, "wb") as f:
            f.write(png_bytes)
    except Exception as e:
        print(f"Failed to cache tile {layer_id} {z}/{x}/{y}: {e}")

    return png_bytes
