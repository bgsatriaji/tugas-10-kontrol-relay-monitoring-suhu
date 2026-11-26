# Panduan menjalankan Tugas 10 sepenuhnya di browser

## Sebelum mulai

Pakai **Google Chrome / Edge**, koneksi internet, dan akun GitHub. Laptop tidak memerlukan Docker/Node.js/Python. Instalasi berjalan di mesin virtual cloud Codespaces. Kamu tetap perlu merekam video dan screenshot nyata sendiri.

## 1. Unggah proyek ke GitHub

1. Ekstrak `Tugas-10-Codespaces-Siap-GitHub.zip`.
2. Kunjungi https://github.com/new, isi nama repository `tugas-10-kontrol-relay-monitoring-suhu`, pilih **Public**, jangan buat README awal, klik **Create repository**.
3. Klik **uploading an existing file**; di File Explorer masuk ke folder ekstraksi, pilih seluruh **isi** folder (termasuk `.devcontainer`), lalu tarik ke area upload.
4. Tinjau daftar unggahan. Pastikan `.devcontainer/devcontainer.json`, `flow-pertemuan10.json`, `iot_device.py`, `package.json`, `scripts/`, dan README.md terlihat. Klik **Commit changes**.
5. Hindari unggah `secrets.h` atau file rahasia. Jangan hanya upload ZIP.

## 2. Mulai GitHub Codespaces

1. Buka repository baru tersebut.
2. Klik tombol hijau **Code** > tab **Codespaces** > **Create codespace on main**.
3. Tunggu sampai tab kode VS Code versi browser muncul. GitHub menjalankan setup otomatis (`postCreateCommand`) dan menjalankan aplikasi (`postStartCommand`).
4. Jika Codespace gagal dibuat akibat kuota/koneksi, lihat tab **Terminal** atau pesan pembuatan Codespace. Ini tidak bisa diperbaiki dengan memaksa local Docker; Codespaces tergantung akun GitHub dan kuota.
5. Di bagian bawah editor klik **PORTS**. Cari port **1880**. Klik ikon globe atau **Open in Browser**. Ini membuka URL mirip `https://NAMA-1880.app.github.dev`.
6. Tambahkan `/ui` pada akhir URL (contoh `https://NAMA-1880.app.github.dev/ui`). **Jangan mengetik `localhost:1880` di browser Windows**, karena servis berjalan di cloud. Port harus tetap **Private**.

## 3. Isi NIM asli — WAJIB

1. Dalam editor Codespaces buka **Terminal** > **New Terminal**.
2. Ketik perintah di bawah. Ganti `NIM_KAMU` dengan NIM benar (tanpa spasi dan tanda `< >`).

   ```bash
   python3 scripts/atur_nim.py NIM_KAMU
   bash scripts/mulai.sh --restart
   ```

3. Buka `README.md`, ganti `[ISI NAMA]`, `[ISI KELAS]` dengan identitas sendiri. Jangan ada placeholder tersisa.
4. Muat ulang dashboard `/ui`. Angka suhu akan bergerak sekitar tiap 3 detik.

## 4. Uji dan rekam bukti asli

Di editor Codespaces Terminal jalankan:

```bash
tail -f .runlogs/simulator.log
```

Buka dashboard pada tab browser lainnya. Di dashboard, gunakan switch **Relay GPIO 26** ke ON kemudian OFF, geser **PWM LED GPIO 2** dari 0 ke 128 ke 255, dan lihat status feedback. Terminal harus mencatat perintah masuk. Tekan Ctrl+C untuk berhenti mengikuti log (simulator tetap berjalan).

Ambil **screenshot asli** yang menampakkan gauge suhu, switch, slider dan status, simpan dengan nama `dashboard.png`. Rekam **video layar asli maks. 60 detik** (misalnya 0-10 detik dashboard; 10-25 detik ubah relay ON/OFF; 25-40 detik slider PWM; 40-55 detik tunjukkan log Python). Gunakan perekam layar Windows / browser yang sudah ada; jika tidak ada, rekam dengan kamera HP. Jangan rekayasa video atau screenshot.

Upload kedua berkas ke folder `bukti/` pada repository GitHub lewat **Add file > Upload files** atau drag-drop.

## 5. Simpan konfigurasi ke repository

Di Codespaces Terminal ketik:

```bash
git add flow-pertemuan10.json iot_device.py esp32_kontrol_relay_pwm/esp32_kontrol_relay_pwm.ino README.md .nim
git commit -m "Sesuaikan topik MQTT dengan NIM"
git push
```

Jika sudah mengedit nama/kelas, perubahan README ikut tersimpan. Pastikan di GitHub pada tab **Code** topik mengandung NIM bukan `DEMO10`.

## 6. Kumpulkan

Salin alamat repository mis. `https://github.com/USERNAME/tugas-10-kontrol-relay-monitoring-suhu`. Di Classroom buka tugas individu Materi 10 > **Tambahkan atau buat** > **Link** > tempel URL > **Serahkan**. Yang diserahkan adalah link GitHub yang berisi kode, screenshot dan video, bukan link live Codespace.

## Troubleshooting

- **Codespace belum bisa dibuka:** cek kuota Codespaces, jaringan, notifikasi error provisioning.
- **Port 1880 tidak terlihat:** jalankan `bash scripts/mulai.sh --restart`, lalu buka tab PORTS.
- **Dashboard blank / 404:** cek halaman `/ui`, bukan hanya root. Lihat `tail -n 60 .runlogs/node-red.log`.
- **Gauge tidak berubah:** cek `tail -n 30 .runlogs/simulator.log` dan `tail -n 30 .runlogs/mosquitto.log`, pastikan topik semua sesuai NIM.
- **Switch tidak mengubah status:** lihat log simulator; pastikan MQTT port 1883 dan topik `iot/NIM/aktuator/relay` sama.
- **NIM sudah benar tetapi status lama muncul:** ulang `bash scripts/mulai.sh --restart` dan refresh dashboard.
- **Codespace tidur:** buka lagi Codespace (layanan biasanya otomatis dimulai ulang) atau jalankan skrip restart.
- **Port private tidak bisa dibuka:** login GitHub pada browser yang sama; jangan mengubah port menjadi Public.
- **Repo berisi banyak file runtime:** jangan upload `node_modules`, `.venv`, `.runlogs`, file `.env` ataupun password Wi-Fi.
