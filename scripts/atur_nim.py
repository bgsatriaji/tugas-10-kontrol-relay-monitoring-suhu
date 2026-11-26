#!/usr/bin/env python3
"""Ganti semua topik iot/NIM secara konsisten pada flow, simulator, sketch.

python3 scripts/atur_nim.py 2312345678
"""
import json
import re
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "flow-pertemuan10.json",
    ROOT / "iot_device.py",
    ROOT / "esp32_kontrol_relay_pwm" / "esp32_kontrol_relay_pwm.ino",
    ROOT / "README.md",
]
STATE = ROOT / ".nim"

def main():
    if len(sys.argv) != 2 or not re.fullmatch(r"[A-Za-z0-9_-]{4,24}", sys.argv[1]):
        raise SystemExit("PAKAI: python3 scripts/atur_nim.py NIM_KAMU (4-24 karakter, huruf/angka/underscore/minus)")
    new = sys.argv[1]
    old = STATE.read_text(encoding="utf-8").strip() if STATE.exists() else "GANTI_NIM"
    if old == new:
        print(f"NIM sudah terpasang: {new}")
        return
    for path in TARGETS:
        content = path.read_text(encoding="utf-8")
        old_prefix = "iot/" + old
        new_prefix = "iot/" + new
        if old_prefix not in content and path.name != 'README.md':
            raise SystemExit(f"GAGAL: Tidak ditemukan {old_prefix} pada {path.name}. Jangan ubah file manual sebelum konfigurasi.")
        content = content.replace(old_prefix, new_prefix)
        if old == 'GANTI_NIM':
            content = content.replace('GANTI_NIM', new)
        if path.name == 'README.md':
            content = content.replace('**NIM:** '+old, '**NIM:** '+new)
        path.write_text(content, encoding="utf-8")
    STATE.write_text(new + "\n", encoding="utf-8")
    flow = json.loads((ROOT / 'flow-pertemuan10.json').read_text(encoding='utf-8'))
    topics = sorted({n.get('topic') for n in flow if n.get('topic','').startswith('iot/')})
    print(f"NIM berhasil diatur: {new}")
    print("Topik MQTT:")
    for t in topics:
        print('  ' + t)
    print("Langkah berikut: bash scripts/mulai.sh --restart")

if __name__ == '__main__':
    main()
