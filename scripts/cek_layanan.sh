#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
echo '[CHECK] Berkas konfigurasi'
python3 scripts/cek_berkas.py
echo '[CHECK] Node-RED HTTP port 1880'
if curl --fail --silent --show-error -o /dev/null 'http://127.0.0.1:1880/ui/'; then
  echo '  OK - dashboard merespons HTTP'
else
  echo '  GAGAL - lihat .runlogs/node-red.log'
fi
echo '[CHECK] Publish & subscribe satu data MQTT'
TOPIC="iot/$(cat .nim)/sensor/suhu"
mosquitto_sub -h 127.0.0.1 -t "$TOPIC" -C 1 -W 10 -v || true
echo '[CHECK] Log simulator terakhir'
tail -n 12 .runlogs/simulator.log || true
