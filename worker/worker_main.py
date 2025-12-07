import redis
import json
import os
import time
from tasks.simple_task import process_data
from tasks.finance.ingest import ingest_ohlc

# --- Configuration & Setup ---
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
QUEUE_NAME = os.getenv("QUEUE_NAME", "default_queue")

try:
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=False)
    r.ping()
    print(f"✅ Successfully connected to Redis at {REDIS_HOST}:{REDIS_PORT}")
except Exception as e:
    print(f"❌ ERROR: Could not connect to Redis. {e}")
    # Exit if Redis connection fails on startup
    exit(1)

# --- Main Worker Execution Loop ---

if __name__ == '__main__':
    print(f"Listening for jobs on queue: {QUEUE_NAME}")
    
    while True:
        try:
            # BRPOP blocks until a job is available
            job_data = r.brpop(QUEUE_NAME, timeout=0) 
            
            # Extract data and load JSON
            # job_data is a tuple: (queue_name, serialized_data)
            job = json.loads(job_data[1])
            job_id = job.get('id', 'N/A')

            print(f"\n--- Received job ID: {job_id} (Task: {job.get('task')}) ---")

            if job.get("task") == "finance_ingest":
                symbol = job.get("symbol", "AAPL")
                print(f"-> Starting finance ingestion for: {symbol}")
                
                # EXECUTE THE TASK
                result = ingest_ohlc(symbol) 
                
                print(f"-> Finance ingestion complete. Result: {result}")
            
            # ... elif conditions for other tasks ...

            print(f"Job {job_id} successfully completed.")

        except json.JSONDecodeError as e:
            print(f"❌ ERROR: Failed to decode job JSON. Error: {e}")
            
        except Exception as e:
            # Critical error during task execution (e.g., DB connection loss, missing library)
            print(f"❌ CRITICAL ERROR during task execution for job ID {job.get('id', 'N/A')}: {e}")
            
        # time.sleep(1) is NOT needed here because r.brpop is blocking.
        
# redis_host = os.getenv("REDIS_HOST", "redis")
# queue_name = "default"

#r = redis.Redis(host=redis_host, port=6379, db=0)

# try:
#     r = redis.Redis(host=redis_host, port=6379, decode_responses=False, db=0)
#     r.ping()
#     print(f"✅ Successfully connected to Redis at {redis_host}:6379")
# except Exception as e:
#     print(f"❌ ERROR: Could not connect to Redis. {e}")
#     # Exit if Redis connection fails on startup
#     exit(1)

# print("Worker started. Listening for tasks...")

# while True:
#     try:
#         job_data = r.brpop(queue_name)
#         job = json.loads(job_data[1])

#         print(f"Received job {job['id']} with payload {job['payload']}")

#         if job.get("task")=="finance_ingest":
#             symbol = job.get("symbol","AAPL")
#             print(f"Starting finance ingestion for: {symbol}")
#             result=ingest_ohlc(symbol)
#             print(f"Finance ingestion is complete: {result}")
#         elif "payload" in job:
#             payload = job["payload"]
#             result = process_data(payload)
#             print(f"Processed simple task result: {result}")
#         else:
#             print("Unknown job format",job)
#         result = process_data(job["payload"])
#         print(f"Job done → {result}")
#     except Exception as e:
#         print("Worker error",str(e))
#     time.sleep(1)