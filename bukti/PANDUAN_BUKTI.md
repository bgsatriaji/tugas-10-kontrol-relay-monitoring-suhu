# Cara membuat bukti pengumpulan (WAJIB hasil nyata)

Lembar tugas individu meminta **screenshot dashboard berjalan** dan **video demonstrasi maksimal 60 detik**. Bukti ini belum tersedia dalam paket dari AI, sebab harus direkam dari aplikasi/perangkat yang sungguh berjalan.

## Screenshot `dashboard.png`

1. Jalankan Node-RED, import dan Deploy `flow-pertemuan10.json`.
2. Jalankan `python iot_device.py` atau ESP32 fisik sampai MQTT terhubung.
3. Buka `http://localhost:1880/ui`, pilih tab IoT Pertemuan 10.
4. Pastikan gauge menunjukkan suhu aktual yang diterima dari simulasi/perangkat, switch dan slider terlihat.
5. Tekan **Win+Shift+S** (Windows), ambil screenshot **dari layar asli**, simpan sebagai `bukti/dashboard.png`.

## Video `demo-60-detik.mp4` (maksimal 60 detik)

Rekomendasi urutan perekaman:
- Detik 0-10: tunjukkan dashboard gauge dengan suhu berubah.
- Detik 10-25: tekan switch Relay ON lalu OFF, tunjukkan terminal simulator/Serial Monitor memperlihatkan kedua perintah.
- Detik 25-40: geser PWM dari 0 ke 128 lalu 255, tunjukkan output status PWM.
- Detik 40-50: lihat status feedback relay dan PWM (dan opsional tombol reset).
- Detik 50-60: tampilkan sekilas flow Node-RED.

Di Windows, rekam memakai **Snipping Tool (record)**, Xbox Game Bar atau software perekam layar yang tersedia. Simpan sebagai MP4 dengan durasi **tidak lebih dari 60 detik**, resolusi 720p jika ukuran besar. Upload website GitHub membatasi ukuran upload file individual (periksa pesan batas pada UI, biasanya 25 MiB); kompres video jika perlu.

Jika tidak ada hardware fisik, **jelaskan penggunaan simulator Python** dalam README dan tunjukkan terminal Python. Jangan menyatakan relay fisik telah menyala jika hanya simulator.
