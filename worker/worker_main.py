import redis
import json
import os
import time
import sys

from tasks.simple_task import process_data
from tasks.finance.ingest import ingest_ohlc
from tasks.adas.simulate import start_adas_simulation, stop_adas_simulation

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
QUEUE_NAME = "default"

print("🔥 WORKER PROCESS STARTED 🔥", flush=True)

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

print("✅ Worker started successfully...", flush=True)
print(f"🔗 Connected to Redis at {REDIS_HOST}:{REDIS_PORT}", flush=True)
print(f"📥 Listening on queue: {QUEUE_NAME}", flush=True)

while True:
    try:
        print("🟡 Waiting for job...")
        sys.stdout.flush()
        job_data = r.brpop([QUEUE_NAME])

        # Defensive checks
        if not job_data or len(job_data) < 2:
            print("⚠️ Empty job_data received:", job_data)
            continue

        raw = job_data[1]

        if not raw:
            print("⚠️ Empty payload from Redis")
            continue

        try:
            job = json.loads(raw)
        except json.JSONDecodeError:
            print("⚠️ Non-JSON payload ignored:", raw)
            continue

        print(f"📨 Received job: {job}")

        if job.get("task") == "adas_start":
            print("🚗 ADAS simulation start requested")
            start_adas_simulation()

        elif job.get("task") == "adas_stop":
            print("🛑 ADAS simulation stop requested")
            stop_adas_simulation()

        elif job.get("task") == "finance_ingest":
            symbol = job.get("symbol", "AAPL")
            print(f"📊 Finance ingest requested for {symbol}")
            ingest_ohlc(symbol)

        elif "payload" in job:
            result = process_data(job["payload"])
            print(f"✅ Simple task result: {result}")

        else:
            print("⚠️ Unknown job format:", job)

    except Exception as e:
        print("❌ Worker error:", str(e))

    time.sleep(0.2)