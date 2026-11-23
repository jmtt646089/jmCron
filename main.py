import threading
import time
import schedule
import requests
from fastapi import FastAPI
import uvicorn

app = FastAPI()

# 1. Define your scheduled task
def my_cron_job():
    print("Running scheduled task...")
    # Example: ping a webhook or run cleanup logic
    # requests.get("https://example.com")

# 2. Configure the schedule
schedule.every(10).minutes.do(my_cron_job)
# Other examples:
# schedule.every().day.at("09:00").do(my_cron_job)
# schedule.every().hour.do(my_cron_job)

# 3. Run the scheduler loop in a background thread
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=run_scheduler, daemon=True).start()

# 4. Lightweight web endpoint to keep container port checks happy
@app.get("/")
def health_check():
    return {"status": "scheduler running"}

if __name__ == "__main__":
    # Run with 1 worker to stay well under 256MB RAM
    uvicorn.run(app, host="0.0.0.0", port=8000)
