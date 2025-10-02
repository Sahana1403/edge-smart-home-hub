import time, json

def now_ms():
  return int(time.time()*1000)

def pretty_json(obj):
  return json.dumps(obj, indent=2)
