import json, time
import paho.mqtt.client as mqtt
from . import db, automation

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
HOME_ID = "home123"

client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("MQTT connected", rc)
    client.subscribe(f"home/{HOME_ID}/device/+/telemetry")
    client.subscribe(f"home/{HOME_ID}/device/+/status")


def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        topic_parts = msg.topic.split('/')
        device_id = topic_parts[3]
        ts = int(time.time()*1000)
        db.insert_telemetry(device_id, ts, payload)
        # run automations if any
        automation.evaluate_triggers(device_id, json.loads(payload))
    except Exception as e:
        print("MQTT msg err", e)


def start():
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()


def publish_cmd(device_id, cmd: dict):
    topic = f"home/{HOME_ID}/device/{device_id}/cmd"
    client.publish(topic, json.dumps(cmd))
