import redis
import json
import os
import time
from tasks.simple_task import process_data

redis_host = os.getenv("REDIS_HOST", "redis")
queue_name = "default"

r = redis.Redis(host=redis_host, port=6379, db=0)

print("Worker started. Listening for tasks...")

while True:
    job_data = r.brpop(queue_name)
    job = json.loads(job_data[1])

    print(f"Received job {job['id']} with payload {job['payload']}")

    result = process_data(job["payload"])
    print(f"Job done → {result}")

    time.sleep(1)