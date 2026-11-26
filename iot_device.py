"""Simulator ESP32 pertemuan 10: suhu setiap 3 detik + relay + PWM via MQTT.

Tidak mengakses GPIO fisik pada PC. Output aktuator disimulasikan di terminal.
Jalankan: python iot_device.py  (setelah pip install -r requirements.txt)
"""

import argparse
import random
import threading
import time

import paho.mqtt.client as mqtt

DEFAULT_BROKER = "127.0.0.1"
DEFAULT_PREFIX = "iot/DEMO10"
DEFAULT_PORT = 1883


def parse_args():
    parser = argparse.ArgumentParser(description="Simulator IoT: MQTT suhu, relay, PWM")
    parser.add_argument("--broker", default=DEFAULT_BROKER, help="host MQTT, default 127.0.0.1")
    parser.add_argument("--port", default=DEFAULT_PORT, type=int)
    parser.add_argument("--prefix", default=DEFAULT_PREFIX, help="topic prefix iot/NIM")
    parser.add_argument("--interval", type=float, default=3.0, help="interval suhu dalam detik")
    args = parser.parse_args()
    if args.interval <= 0:
        parser.error("--interval harus lebih dari 0")
    if "DEMO10" in args.prefix:
        parser.error("Isi NIM terlebih dahulu dengan 'python isi_nim.py NIM_KAMU'")
    return args


def run():
    args = parse_args()
    base = args.prefix.rstrip("/")
    topic_suhu = base + "/sensor/suhu"
    topic_relay = base + "/aktuator/relay"
    topic_pwm = base + "/aktuator/pwm"
    topic_status_relay = base + "/status/relay"
    topic_status_pwm = base + "/status/pwm"

    state = {"relay": "OFF", "pwm": 0}
    connected = threading.Event()
    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id=f"Sim-P10-{int(time.time()) % 1000000}",
        protocol=mqtt.MQTTv311,
    )
    client.reconnect_delay_set(min_delay=1, max_delay=30)

    def publish_status():
        client.publish(topic_status_relay, state["relay"], qos=0, retain=True)
        client.publish(topic_status_pwm, str(state["pwm"]), qos=0, retain=True)

    def on_connect(cli, userdata, flags, reason_code, properties):
        if reason_code != 0:
            print(f"[MQTT] Gagal terhubung: {reason_code}", flush=True)
            return
        connected.set()
        cli.subscribe([(topic_relay, 0), (topic_pwm, 0)])
        print(f"[MQTT] Terhubung {args.broker}:{args.port} | prefix={base}", flush=True)
        print(f"[MQTT] Subscribe: {topic_relay}, {topic_pwm}", flush=True)
        publish_status()

    def on_disconnect(cli, userdata, disconnect_flags, reason_code, properties):
        connected.clear()
        print(f"[MQTT] Terputus: {reason_code}; mencoba terhubung ulang...", flush=True)

    def on_message(cli, userdata, msg):
        command = msg.payload.decode("utf-8", errors="replace").strip()
        print(f"[MQTT] Diterima {msg.topic} => {command}", flush=True)
        if msg.topic == topic_relay:
            if command not in ("ON", "OFF"):
                print("[RELAY] Perintah tidak dikenal (harus ON atau OFF)", flush=True)
                return
            state["relay"] = command
            print(f"[RELAY GPIO26 - SIMULASI] {command}", flush=True)
            cli.publish(topic_status_relay, command, qos=0, retain=True)
        elif msg.topic == topic_pwm:
            if not command.isascii() or not command.isdigit():
                print("[PWM] Perintah tidak valid (harus bilangan 0-255)", flush=True)
                return
            value = int(command)
            if value < 0 or value > 255:
                print("[PWM] Nilai di luar 0-255", flush=True)
                return
            state["pwm"] = value
            print(f"[LED GPIO2 - SIMULASI] Kecerahan PWM = {value}/255", flush=True)
            cli.publish(topic_status_pwm, str(value), qos=0, retain=True)

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    print(f"[MULAI] Menghubungkan ke MQTT {args.broker}:{args.port} ...", flush=True)
    try:
        client.connect(args.broker, args.port, keepalive=60)
        client.loop_start()
        # Sensor dapat mengirim saat broker tersambung. Waktu pengiriman sekitar 3 dtk.
        try:
            while True:
                if connected.is_set():
                    suhu = round(random.uniform(24.0, 33.0), 2)
                    client.publish(topic_suhu, f"{suhu:.2f}", qos=0)
                    print(f"[SENSOR SIMULASI] {topic_suhu} -> {suhu:.2f} °C", flush=True)
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\n[STOP] Menghentikan simulator...", flush=True)
    except OSError as err:
        print(f"[ERROR MQTT] {err}. Cek broker / internet / firewall.", flush=True)
        raise SystemExit(1) from err
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    run()
