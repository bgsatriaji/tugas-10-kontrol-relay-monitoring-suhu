// Tugas Praktikum 10 - Kontrol relay & PWM, monitoring DHT22 dengan ESP32.
// Target: ESP32 (GPIO26 relay, GPIO2 PWM, GPIO4 DHT22).
// Library Arduino IDE: PubSubClient (Nick O'Leary), DHT sensor library (Adafruit),
// Adafruit Unified Sensor. Pasang ESP32 boards package.
// Untuk kredensial Wi-Fi buat salinan secrets.example.h => secrets.h (JANGAN upload secrets.h).

#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <esp_arduino_version.h>
#include "secrets.h"

const char* MQTT_BROKER = "broker.emqx.io";
const uint16_t MQTT_PORT = 1883;
const char* MQTT_TOPIC_SUHU = "iot/DEMO10/sensor/suhu";
const char* MQTT_TOPIC_RELAY = "iot/DEMO10/aktuator/relay";
const char* MQTT_TOPIC_PWM = "iot/DEMO10/aktuator/pwm";
const char* MQTT_TOPIC_STATUS_RELAY = "iot/DEMO10/status/relay";
const char* MQTT_TOPIC_STATUS_PWM = "iot/DEMO10/status/pwm";

constexpr uint8_t PIN_DHT = 4;
constexpr uint8_t PIN_RELAY = 26;
constexpr uint8_t PIN_LED_PWM = 2;
constexpr uint8_t DHT_TYPE = DHT22;
constexpr bool RELAY_ACTIVE_HIGH = true;  // ubah false jika modul relay aktif LOW
constexpr uint32_t SUHU_INTERVAL_MS = 3000;
constexpr uint32_t RETRY_INTERVAL_MS = 5000;

WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);
DHT dht(PIN_DHT, DHT_TYPE);
String relayState = "OFF";
int pwmValue = 0;
uint32_t lastPublish = 0;
uint32_t lastReconnectAttempt = 0;

void applyRelay(bool on) {
  digitalWrite(PIN_RELAY, (on == RELAY_ACTIVE_HIGH) ? HIGH : LOW);
  relayState = on ? "ON" : "OFF";
}

void applyPwm(uint8_t duty) {
  pwmValue = duty;
#if ESP_ARDUINO_VERSION_MAJOR >= 3
  ledcWrite(PIN_LED_PWM, duty); // ESP32 Arduino core 3.x menggunakan nomor pin
#else
  ledcWrite(0, duty);           // ESP32 Arduino core 2.x menggunakan channel
#endif
}

void publishFeedback() {
  mqttClient.publish(MQTT_TOPIC_STATUS_RELAY, relayState.c_str(), true);
  String pwmString = String(pwmValue);
  mqttClient.publish(MQTT_TOPIC_STATUS_PWM, pwmString.c_str(), true);
}

void mqttCallback(char* topic, byte* payload, unsigned int length) {
  String command;
  for (unsigned int i = 0; i < length; i++) command += (char)payload[i];
  command.trim();
  String incoming = String(topic);

  if (incoming == MQTT_TOPIC_RELAY) {
    if (command == "ON") applyRelay(true);
    else if (command == "OFF") applyRelay(false);
    else {
      Serial.println("[RELAY] Harus ON atau OFF");
      return;
    }
    mqttClient.publish(MQTT_TOPIC_STATUS_RELAY, relayState.c_str(), true);
    Serial.println("[GPIO26] Relay: " + relayState);
  } else if (incoming == MQTT_TOPIC_PWM) {
    if (command.length() == 0) return;
    for (unsigned int i = 0; i < command.length(); i++) {
      if (!isDigit(command[i])) {
        Serial.println("[PWM] Format bukan bilangan bulat");
        return;
      }
    }
    long level = command.toInt();
    if (level < 0 || level > 255) {
      Serial.println("[PWM] Harus 0-255");
      return;
    }
    applyPwm((uint8_t)level);
    String pwmString = String(pwmValue);
    mqttClient.publish(MQTT_TOPIC_STATUS_PWM, pwmString.c_str(), true);
    Serial.println("[GPIO2] PWM: " + pwmString);
  }
}

void connectWifi() {
  if (WiFi.status() == WL_CONNECTED) return;
  Serial.println("[WiFi] Menghubungkan...");
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
}

void connectMqtt() {
  if (mqttClient.connected() || WiFi.status() != WL_CONNECTED) return;
  uint32_t now = millis();
  if (now - lastReconnectAttempt < RETRY_INTERVAL_MS) return;
  lastReconnectAttempt = now;
  String clientId = "esp32-p10-" + WiFi.macAddress();
  clientId.replace(":", "");
  if (mqttClient.connect(clientId.c_str())) {
    Serial.println("[MQTT] Terhubung");
    mqttClient.subscribe(MQTT_TOPIC_RELAY);
    mqttClient.subscribe(MQTT_TOPIC_PWM);
    publishFeedback();
  } else {
    Serial.printf("[MQTT] Gagal state=%d\n", mqttClient.state());
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(PIN_RELAY, OUTPUT);
  applyRelay(false); // kondisi aman saat startup
#if ESP_ARDUINO_VERSION_MAJOR >= 3
  ledcAttach(PIN_LED_PWM, 5000, 8); // PWM freq 5kHz, resolusi 8 bit
#else
  ledcSetup(0, 5000, 8);
  ledcAttachPin(PIN_LED_PWM, 0);
#endif
  applyPwm(0);
  dht.begin();
  mqttClient.setServer(MQTT_BROKER, MQTT_PORT);
  mqttClient.setCallback(mqttCallback);
  connectWifi();
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    static uint32_t lastWifiAttempt = 0;
    if (millis() - lastWifiAttempt > 10000) {
      lastWifiAttempt = millis();
      connectWifi();
    }
  } else {
    connectMqtt();
  }
  if (mqttClient.connected()) mqttClient.loop();

  if (millis() - lastPublish >= SUHU_INTERVAL_MS) {
    lastPublish = millis();
    float suhu = dht.readTemperature();
    if (!isnan(suhu) && mqttClient.connected()) {
      String out = String(suhu, 2);
      mqttClient.publish(MQTT_TOPIC_SUHU, out.c_str());
      Serial.println("[SUHU] " + out + " C");
    } else {
      Serial.println("[SUHU] DHT22 gagal membaca / MQTT belum siap");
    }
  }
}
