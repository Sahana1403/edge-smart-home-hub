from . import db, mqtt_client
import json, time

AUTOMATIONS = [
    {
        "id": 1,
        "name": "Night motion light",
        "trigger": {"sensor":"motion_sensor_1","field":"motion","value":True},
        "action": {"device":"light_1","cmd": {"cmd":"set","params":{"state":"on"}}},
        "enabled": True
    }
]


def evaluate_triggers(device_id, payload: dict):
    # simple equality-based triggers
    for a in AUTOMATIONS:
        if not a.get("enabled"): continue
        t = a["trigger"]
        if t.get("sensor") == device_id:
            field = t.get("field")
            if payload.get(field) == t.get("value") and is_night():
                action = a.get("action")
                mqtt_client.publish_cmd(action["device"], action["cmd"])


def run_manual(automation_id):
    for a in AUTOMATIONS:
        if a["id"] == automation_id:
            action = a.get("action")
            mqtt_client.publish_cmd(action["device"], action["cmd"])


def is_night():
    h = time.localtime().tm_hour
    return h < 6 or h > 20
