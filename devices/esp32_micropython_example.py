# Run on ESP32 with MicroPython and umqtt.simple

import network
import time
import ubinascii
from umqtt.simple import MQTTClient
import machine

# ====== Configuration ======
WIFI_SSID = 'yourssid'
WIFI_PASS = 'yourpass'
MQTT_BROKER = '192.168.1.10'
MQTT_PORT = 1883
HOME_ID = 'home123'
DEVICE_ID = 'sensor_esp32_1'

# MQTT Topics
TOPIC_PUB = b"home/%s/%s/data" % (HOME_ID.encode(), DEVICE_ID.encode())
TOPIC_SUB = b"home/%s/%s/cmd" % (HOME_ID.encode(), DEVICE_ID.encode())

# ====== WiFi Connection ======
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect(WIFI_SSID, WIFI_PASS)

print("Connecting to WiFi...")
while not sta.isconnected():
    time.sleep(1)
    print("Waiting for connection...")
print("Connected to WiFi:", sta.ifconfig())

# ====== Hardware Setup ======
# Onboard LED (GPIO2) for command testing
led = machine.Pin(2, machine.Pin.OUT)

# Simulated sensor using ADC (can replace with real sensor like DHT)
adc = machine.ADC(machine.Pin(34))  # GPIO34 analog input
adc.atten(machine.ADC.ATTN_11DB)    # Full range: 0–3.3V

# ====== MQTT Callbacks ======
def sub_callback(topic, msg):
    print("Message received:", topic, msg)
    if msg == b"LED_ON":
        led.value(1)
        print("LED turned ON")
    elif msg == b"LED_OFF":
        led.value(0)
        print("LED turned OFF")

# ====== Main ======
def main():
    client_id = ubinascii.hexlify(machine.unique_id())
    client = MQTTClient(client_id, MQTT_BROKER, MQTT_PORT)
    client.set_callback(sub_callback)
    client.connect()
    print("Connected to MQTT broker:", MQTT_BROKER)

    # Subscribe to command topic
    client.subscribe(TOPIC_SUB)
    print("Subscribed to:", TOPIC_SUB)

    while True:
        try:
            # Check for commands
            client.check_msg()

            # Read sensor (simulated value from ADC)
            sensor_val = adc.read()
            payload = b'{"device":"%s","sensor_val":%d}' % (DEVICE_ID.encode(), sensor_val)
            client.publish(TOPIC_PUB, payload)
            print("Published:", payload)

            time.sleep(10)  # every 10 seconds
        except Exception as e:
            print("Error:", e)
            time.sleep(5)

# ====== Run ======
try:
    main()
except KeyboardInterrupt:
    print("Program stopped")
