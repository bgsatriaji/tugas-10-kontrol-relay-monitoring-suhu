# Tugas Individu Materi 10 - Kontrol Relay & Monitoring Suhu (GitHub Codespaces)

**Mata kuliah:** Pemrograman Internet of Things (SIF1502)  
**NIM:** DEMO10  
**Nama:** [ISI NAMA]  
**Kelas:** [ISI KELAS]

Proyek mengikuti penugasan individu dosen: Node-RED Dashboard mengukur suhu dari simulator Python dan mengontrol relay / PWM melalui MQTT dua arah. **Tidak perlu instal Node.js, Mosquitto, Python, atau Docker di laptop.** Semuanya dipasang otomatis di lingkungan cloud GitHub Codespaces. Tetap perlu internet, akun GitHub, dan kuota Codespaces tersedia.

> **PENTING:** Flow awal menggunakan NIM contoh `DEMO10` hanya agar preview berjalan. Ganti dengan NIM pribadi sebelum mengumpulkan. Bukti dashboard dan video harus benar-benar diambil saat program berjalan; belum termasuk paket awal.

## Fitur sesuai tugas

| Komponen | Topik MQTT | Data |
|---|---|---|
| Suhu simulator setiap 3 detik | `iot/DEMO10/sensor/suhu` | Angka 24-33 C |
| Kontrol relay (simulasi GPIO26) | `iot/DEMO10/aktuator/relay` | `ON` / `OFF` |
| Kecerahan LED (simulasi GPIO2) | `iot/DEMO10/aktuator/pwm` | `0` - `255` |
| Umpan balik status relay | `iot/DEMO10/status/relay` | `ON` / `OFF` |
| Umpan balik PWM | `iot/DEMO10/status/pwm` | `0` - `255` |

Terdapat node `mqtt in`, `mqtt out`, `ui_gauge`, `ui_switch`, `ui_slider`, `ui_chart`, `ui_text` serta tombol reset. Broker **Mosquitto localhost:1883** berjalan hanya di dalam Codespace. **Node-RED port 1880 harus tetap Private**, jangan diubah menjadi Public karena editor Node-RED belum memakai autentikasi.

## Memulai tanpa instal di laptop (langkah bergambar tersedia pada PANDUAN_CODESPACES.md)

1. Ekstrak ZIP yang dibagikan. Di GitHub buat **repository Public** baru tanpa README otomatis.
2. Klik **Add file > Upload files** (atau `uploading an existing file`), lalu **drag seluruh ISI folder** proyek ke GitHub. Jangan unggah ZIP saja. Pastikan `.devcontainer/devcontainer.json` juga ikut terunggah.
3. Klik **Commit changes**.
4. Klik **Code > Codespaces > Create codespace on main**.
5. GitHub menyiapkan lingkungan cloud otomatis: Node-RED, dashboard legacy, Python dan Mosquitto. Setelah editor Codespaces terbuka, buka tab **PORTS** di bawah, klik **Open in Browser** pada port **1880**.
6. Pada alamat browser hasilnya (misal `https://NAMA-1880.app.github.dev`), tambahkan `/ui` di belakangnya. Halaman dashboard akan terbuka.
7. Di Terminal Codespaces, isi NIM Anda:

   ```bash
   python3 scripts/atur_nim.py NIM_KAMU
   bash scripts/mulai.sh --restart
   ```

8. Muat ulang dashboard `/ui`. Nilai suhu berubah sekitar tiap 3 detik. Coba switch ON/OFF dan geser PWM.
9. Untuk lihat respons simulator, buka **Terminal** di Codespaces, jalankan:

   ```bash
   tail -f .runlogs/simulator.log
   ```

10. Ambil screenshot dashboard **asli**, rekam layar **asli** maks. 60 detik; taruh di `bukti/dashboard.png` dan `bukti/demo-60-detik.mp4`, lalu upload ke GitHub. Jangan klaim pengujian jika belum benar-benar berjalan.

Saat berhenti dan membuka Codespace lagi, layanan akan dicoba dinyalakan otomatis. Jika tidak aktif, jalankan `bash scripts/mulai.sh --restart`. Untuk cek kesehatan: `bash scripts/cek_layanan.sh`.

### Cara menyimpan perubahan NIM ke GitHub

Dalam Codespaces, setelah mengganti NIM, buka terminal dan jalankan:

```bash
git add flow-pertemuan10.json iot_device.py esp32_kontrol_relay_pwm/esp32_kontrol_relay_pwm.ino README.md .nim
git commit -m "Konfigurasi topik MQTT sesuai NIM"
git push
```

Jika di GitHub sudah ada perubahan lain, jangan melakukan force push. File `.nim` hanya berisi NIM yang digunakan pada topik, bukan secret.

## Pengujian dan bukti

- Gauge suhu menampilkan data berubah berkala dari **Python (bukan sensor DHT22 fisik)**.
- Switch relay `ON/OFF` menghasilkan baris `[RELAY GPIO26 - SIMULASI] ON/OFF` di log simulator.
- Slider PWM 0-255 menghasilkan baris `[LED GPIO2 - SIMULASI] ...` di log.
- Teks feedback status relay dan PWM ikut berubah. Tombol reset mematikan relay dan mengatur PWM ke 0.
- **Screenshot** `bukti/dashboard.png` dan **video ≤60 detik** `bukti/demo-60-detik.mp4` adalah syarat tugas, harus merekam aplikasi yang berjalan sebenarnya. Tidak ada bukti yang dipalsukan atau dibuat otomatis.

## File pengumpulan

- `flow-pertemuan10.json` - flow Node-RED untuk import atau edit.
- `iot_device.py` - kode Python simulator (diizinkan tugas individu), tidak menyalakan GPIO fisik.
- `esp32_kontrol_relay_pwm/esp32_kontrol_relay_pwm.ino` - kode opsional ESP32 fisik; untuk board asli memerlukan broker MQTT yang dapat diakses board (bukan Mosquitto internal Codespace).
- `bukti/dashboard.png` - diisi pengguna setelah berhasil menjalankan.
- `bukti/demo-60-detik.mp4` - diisi pengguna setelah berhasil merekam.
- `.devcontainer/` - otomatis menyiapkan lingkungan Codespaces.

## Keterangan batasan

Demonstrasi Codespaces membuktikan kontrol **simulator Python**, bukan kendali relay fisik. Itu sesuai pilihan `file .py` yang diizinkan lembar tugas individu. Hasil uji di perangkat mahasiswa hanya dapat dipastikan setelah program benar-benar dijalankan dan diamati.
