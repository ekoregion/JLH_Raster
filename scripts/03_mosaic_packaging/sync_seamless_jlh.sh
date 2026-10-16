#!/usr/bin/env bash
# Script sinkronisasi otomatis file JLH seamless dari VPS ke laptop

DEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/data/jlh_seamless" && pwd)"
mkdir -p "$DEST_DIR"

echo "=== Auto-Sync JLH Seamless dari VPS ==="
echo "Target Folder: $DEST_DIR"

# Loop sinkronisasi rsync berkala
while true; do
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Memeriksa file seamless baru di VPS..."
    rsync -avz -e "ssh -p 52222" --include="*_seamless.tif" --exclude="*" \
        kemenlh@182.23.160.75:/home/kemenlh/jlh/output/jlh_sumbar_2025/ "$DEST_DIR/"
    
    # Hitung jumlah file yang sudah terunduh
    COUNT=$(ls -1 "$DEST_DIR"/*_seamless.tif 2>/dev/null | wc -l | tr -d ' ')
    echo "Total file seamless terunduh: $COUNT / 6"
    
    if [ "$COUNT" -ge 6 ]; then
        echo "[SUKSES] Seluruh 6 file JLH seamless telah selesai diunduh!"
        break
    fi
    
    sleep 300 # Cek setiap 5 menit
done
