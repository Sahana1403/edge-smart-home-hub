PRAGMA journal_mode=WAL;


CREATE TABLE IF NOT EXISTS devices (
id TEXT PRIMARY KEY,
friendly_name TEXT,
type TEXT,
capabilities TEXT,
last_seen INTEGER
);


CREATE TABLE IF NOT EXISTS telemetry (
id INTEGER PRIMARY KEY AUTOINCREMENT,
device_id TEXT,
ts INTEGER,
payload TEXT
);


CREATE TABLE IF NOT EXISTS events (
id INTEGER PRIMARY KEY AUTOINCREMENT,
ts INTEGER,
source TEXT,
event_type TEXT,
payload TEXT
);


CREATE TABLE IF NOT EXISTS automations (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
trigger TEXT,
action TEXT,
enabled INTEGER DEFAULT 1
);


CREATE TABLE IF NOT EXISTS models (
name TEXT PRIMARY KEY,
version TEXT,
file_path TEXT,
last_trained INTEGER
);


CREATE TABLE IF NOT EXISTS maintenance (
id INTEGER PRIMARY KEY AUTOINCREMENT,
device_id TEXT,
ts INTEGER,
message TEXT,
severity TEXT
);
