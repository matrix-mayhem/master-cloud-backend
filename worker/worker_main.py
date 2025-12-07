import redis
import json
import os
import time

from tasks.simple_task import process_data
from tasks.finance.ingest import ingest_ohlc

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
QUEUE_NAME = "default"

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

print("✅ Worker started successfully...")
print(f"🔗 Connected to Redis at {REDIS_HOST}:{REDIS_PORT}")
print(f"📥 Listening on queue: {QUEUE_NAME}")

while True:
    try:
        job_data = r.brpop(QUEUE_NAME)
        job = json.loads(job_data[1])
        print(f"📨 Received job: {job}")

        if job.get("task") == "finance_ingest":
            symbol = job.get("symbol", "AAPL")
            print(f"📊 Finance ingest requested for {symbol}")
            result = ingest_ohlc(symbol)
            print(f"✅ Finance ingest result: {result}")

        elif "payload" in job:
            payload = job["payload"]
            result = process_data(payload)
            print(f"✅ Simple task result: {result}")

        else:
            print("⚠️ Unknown job format:", job)

    except Exception as e:
        print("❌ Worker error:", str(e))

    time.sleep(1)
