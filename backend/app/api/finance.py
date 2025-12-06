from fastapi import APIRouter
import redis, json, uuid, os

router = APIRouter()

r=redis.Redis(host=os.getenv("REDIS_HOST","redis"),port=6379)

@router.post("/ingest")
def ingest(symbol:str):
    job = {"id":str(uuid.uuid4()),"task":"finance_ingest","symbol":symbol}
    r.lpush("default",json.dumps(job))
    return {"message":"ingestion_started","job":job}