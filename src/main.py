from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
from . import mqtt_client, db, automation
app = FastAPI()
app.mount("/ui", StaticFiles(directory="ui", html=True), name="ui")


@app.get("/api/health")
def health():
  return {"status":"ok"}


# Simple API endpoints
@app.get("/api/devices")
def list_devices():
  return db.list_devices()


@app.post("/api/trigger/{automation_id}")
def trigger(automation_id: int):
  automation.run_manual(automation_id)
  return {"status":"triggered","id": automation_id}


if __name__ == "__main__":
  mqtt_client.start()
  uvicorn.run(app, host="0.0.0.0", port=8000)
