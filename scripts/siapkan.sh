#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
echo "[SETUP] Instalasi Node-RED + palet dashboard (hanya di cloud Codespace)..."
npm install --no-audit --no-fund
echo "[SETUP] Instalasi Python venv + paho-mqtt (hanya di cloud Codespace)..."
python3 -m venv .venv
.venv/bin/python -m pip install --disable-pip-version-check -r requirements.txt
if [[ ! -f .nim ]]; then
  echo "[SETUP] Mengisi topik contoh DEMO10 dahulu. WAJIB ganti ke NIM sendiri sebelum pengumpulan."
  python3 scripts/atur_nim.py DEMO10
fi
python3 scripts/cek_berkas.py
echo "[SETUP] Selesai. Saat Codespace hidup, dashboard tersedia lewat tab PORTS -> 1880 -> /ui"
