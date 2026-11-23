import threading
import time
import schedule
import requests
from fastapi import FastAPI
import uvicorn

app = FastAPI()
TARGET_URL = "https://uniapi.jmc.kdns.fr/health"
last_result = {"status": "waiting for first run"}

def ping_health():
    global last_result
    try:
        # 10-second timeout prevents the thread from hanging if the server is slow
        response = requests.get(TARGET_URL, timeout=10)
        last_result = {
            "status_code": response.status_code,
            "response": response.json(),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
        }
        print(f"Success: {last_result}")
    except Exception as e:
        last_result = {
            "error": str(e),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
        }
        print(f"Error pinging URL: {e}")

# Run once immediately on startup
ping_health()

# Schedule to run every 5 minutes (adjust as needed)
# schedule.every(5).minutes.do(ping_health)
schedule.every().day.at("20:00").do(ping_health)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=run_scheduler, daemon=True).start()

# Status endpoint to satisfy Jade Hosting's web port check and let you inspect logs
@app.get("/")
def status():
    return {
        "service": "health-pinger",
        "target": TARGET_URL,
        "last_run": last_result
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
