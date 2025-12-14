from fastapi import APIRouter
import os, json, uuid, redis
from app.database.finance_db import SessionLocal
from app.models.adas_frame import AdasFrame

router = APIRouter()

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=6379,
    db=0
)

@router.post("/start")
def start_adas():
    job = {
        "id": str(uuid.uuid4()),
        "task": "adas_start"
    }
    r.lpush("default", json.dumps(job))
    return {"message": "ADAS simulation start queued", "job_id": job["id"]}


@router.post("/stop")
def stop_adas():
    job = {
        "id": str(uuid.uuid4()),
        "task": "adas_stop"
    }
    r.lpush("default", json.dumps(job))
    return {"message": "ADAS simulation stop queued", "job_id": job["id"]}


@router.get("/latest")
def latest_frame():
    session = SessionLocal()

    frame = session.query(AdasFrame) \
        .order_by(AdasFrame.timestamp.desc()) \
        .first()

    session.close()

    if not frame:
        return {"error": "No ADAS frames yet"}

    return {
        "timestamp": frame.timestamp,
        "ego_speed": frame.ego_speed,
        "lead_distance": frame.lead_distance,
        "detected_sign": frame.detected_sign,
        "commanded_action": frame.commanded_action,
    }
