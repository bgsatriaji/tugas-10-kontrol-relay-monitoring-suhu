#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
if [[ "${1:-}" == "--restart" ]]; then
  bash scripts/berhenti.sh
fi
mkdir -p .runlogs
active() {
  local pfile="$1"
  [[ -f "$pfile" ]] && kill -0 "$(cat "$pfile")" 2>/dev/null
}
spawn() {
  local name="$1"; shift
  nohup "$@" > ".runlogs/$name.log" 2>&1 < /dev/null &
  echo $! > ".runlogs/$name.pid"
  echo "[START] $name pid=$(cat ".runlogs/$name.pid")"
}
port_ready() {
  python3 - "$1" <<'PYTEST'
import socket,sys
with socket.socket() as sock:
    sock.settimeout(1)
    try: sock.connect(('127.0.0.1',int(sys.argv[1]))); sys.exit(0)
    except OSError: sys.exit(1)
PYTEST
}
if ! active .runlogs/mosquitto.pid; then
  spawn mosquitto mosquitto -c "$ROOT/.devcontainer/mosquitto.conf"
fi
for i in $(seq 1 20); do
  port_ready 1883 && break
  sleep 1
done
if ! port_ready 1883; then
  echo "[ERROR] MQTT port 1883 belum hidup, cek .runlogs/mosquitto.log" >&2
  tail -n 30 .runlogs/mosquitto.log >&2
  exit 1
fi
if ! active .runlogs/node-red.pid; then
  if [[ ! -x node_modules/.bin/node-red ]]; then
    echo '[ERROR] Node-RED belum terinstall. Jalankan: bash scripts/siapkan.sh' >&2
    exit 1
  fi
  spawn node-red "$ROOT/node_modules/.bin/node-red" --userDir "$ROOT" --settings "$ROOT/settings.js" "$ROOT/flow-pertemuan10.json"
fi
for i in $(seq 1 45); do
  port_ready 1880 && break
  sleep 1
done
if ! port_ready 1880; then
  echo "[ERROR] Node-RED port 1880 belum hidup, cek .runlogs/node-red.log" >&2
  tail -n 40 .runlogs/node-red.log >&2
  exit 1
fi
if ! active .runlogs/simulator.pid; then
  if [[ ! -x .venv/bin/python ]]; then
    echo '[ERROR] Python venv belum ada. Jalankan: bash scripts/siapkan.sh' >&2
    exit 1
  fi
  spawn simulator "$ROOT/.venv/bin/python" "$ROOT/iot_device.py" --broker 127.0.0.1
fi
echo ""
echo "[SIAP] MQTT: 127.0.0.1:1883 (HANYA DALAM CLOUD)"
echo "[SIAP] Node-RED dashboard: buka tab PORTS, port 1880, lalu tambah /ui"
echo "[SIAP] Node-RED editor: buka tab PORTS, port 1880, tanpa /ui"
echo "[INFO] Periksa log: tail -f .runlogs/simulator.log"
echo "[PENTING] Topik masih DEMO10? Jalankan: python3 scripts/atur_nim.py NIM_KAMU"
echo "          lalu: bash scripts/mulai.sh --restart"
