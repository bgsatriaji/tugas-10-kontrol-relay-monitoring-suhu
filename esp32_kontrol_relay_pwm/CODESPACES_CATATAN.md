# ESP32 fisik vs simulator Codespaces

Firmware .ino adalah tambahan opsional. Untuk ESP32 fisik perlu broker yang bisa dijangkau ESP32 melalui Wi-Fi. Broker lokal `127.0.0.1:1883` di Codespaces **tidak** bisa langsung diakses ESP32 yang berada di rumah. Jangan membuat port MQTT publik tanpa pengamanan. Untuk tugas individu, file `.py` simulator sudah diizinkan. Jika ingin hardware sungguhan, pindahkan baik ESP32 maupun flow Node-RED ke broker MQTT yang sama dan aman serta uji pin fisik.
