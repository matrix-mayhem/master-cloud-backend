from fastapi import APIRouter
import redis
import json
import uuid
import os

router = APIRouter()

redis_host = os.getenv("REDIS_HOST", "redis")
queue_name = "default"

r =redis.Redis(host=redis_host,port=6379,db=0)

@router.post("/run-task")
def run_task(payload: dict):
    task_id = str(uuid.uuid4())
    job = {
        "id":task_id,
        "payload":payload
    }
    r.lpush(queue_name, json.dumps(job))
    return {"message":"Task queued", "task_id":task_id}