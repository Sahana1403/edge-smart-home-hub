import sqlite3, json
DB_FILE = "hub.db"
_conn = sqlite3.connect(DB_FILE, check_same_thread=False)
_conn.row_factory = sqlite3.Row


def insert_telemetry(device_id, ts, payload):
    cur = _conn.cursor()
    cur.execute("INSERT INTO telemetry (device_id, ts, payload) VALUES (?,?,?)",
                (device_id, ts, payload))
    _conn.commit()


def list_devices():
    cur = _conn.cursor()
    cur.execute("SELECT * FROM devices")
    rows = [dict(r) for r in cur.fetchall()]
    return rows


def register_device(device_id, friendly_name, type_, capabilities):
    cur = _conn.cursor()
    cur.execute("INSERT OR REPLACE INTO devices (id,friendly_name,type,capabilities,last_seen) VALUES (?,?,?,?,?)",
                (device_id, friendly_name, type_, json.dumps(capabilities), int(time.time()*1000)))
    _conn.commit()
