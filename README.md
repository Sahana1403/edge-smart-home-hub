# Edge Smart Home Hub
Lightweight on-premise smart home hub for Indian households.


## Features
- Local MQTT broker integration
- SQLite local storage
- Basic automation rules & example AI stubs
- Minimal PWA UI
- ESP32 MicroPython example to publish telemetry


## Quickstart (local)
1. Create a Python venv and install dependencies:


```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

2. Initialize DB:

sqlite3 hub.db < sql/schema.sql

3. Start the hub (this starts the FastAPI app):

uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

4. Run a local MQTT broker (e.g., Mosquitto) or use a provided docker-compose:

docker-compose up -d

5. Open the UI at http://localhost:8000/ui/
