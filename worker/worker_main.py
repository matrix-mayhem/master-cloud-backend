import redis
import json
import os
import time
from tasks.simple_task import process_data
from tasks.finance.ingest import ingest_ohlc

redis_host = os.getenv("REDIS_HOST", "redis")
queue_name = "default"

r = redis.Redis(host=redis_host, port=6379, db=0)

print("Worker started. Listening for tasks...")

while True:
    try:
        job_data = r.brpop(queue_name)
        job = json.loads(job_data[1])

        print(f"Received job {job['id']} with payload {job['payload']}")

        if job.get("task")=="finance_ingest":
            symbol = job.get("symbol","AAPL")
            print(f"Starting finance ingestion for: {symbol}")
            result=ingest_ohlc(symbol)
            print(f"Finance ingestion is complete: {result}")
        elif "payload" in job:
            payload = job["payload"]
            result = process_data(payload)
            print(f"Processed simple task result: {result}")
        else:
            print("Unknown job format",job)
        result = process_data(job["payload"])
        print(f"Job done → {result}")
    except Exception as e:
        print("Worker error",str(e))
    time.sleep(1)