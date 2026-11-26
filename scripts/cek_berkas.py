#!/usr/bin/env python3
"""Pemeriksaan statis, BUKAN pengganti demo berjalan."""
import json
import pathlib
import sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
flow=json.loads((ROOT/'flow-pertemuan10.json').read_text(encoding='utf8'))
assert len(flow)>=20
idx={n['id']:n for n in flow}
assert len(idx)==len(flow)
assert all(x['id'] in idx for x in flow)
for n in flow:
    for outs in n.get('wires',[]):
        for target in outs:
            assert target in idx, (n['id'],target)
assert any(n['type']=='ui_gauge' for n in flow)
assert any(n['type']=='ui_switch' for n in flow)
assert any(n['type']=='ui_slider' for n in flow)
assert any(n['type']=='mqtt in' for n in flow)
assert any(n['type']=='mqtt out' for n in flow)
broker=next(n for n in flow if n['type']=='mqtt-broker')
assert broker['broker'] in ('127.0.0.1','localhost')
assert str(broker['port'])=='1883'
nim=(ROOT/'.nim').read_text(encoding='utf8').strip() if (ROOT/'.nim').exists() else 'GANTI_NIM'
topics=[n['topic'] for n in flow if str(n.get('topic','')).startswith('iot/')]
assert all(t.startswith('iot/'+nim+'/') for t in topics)
code=(ROOT/'iot_device.py').read_text(encoding='utf8')
assert 'iot/'+nim in code
compile(code,str(ROOT/'iot_device.py'),'exec')
print(f"[OK] {len(flow)} node, {len(topics)} topik MQTT, broker lokal 1883, NIM: {nim}")
print('[INFO] Status ini hanya pemeriksaan berkas, bukan bukti runtime / hardware.')
