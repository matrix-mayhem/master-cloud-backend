from fastapi import FastAPI
from app.api.tasks import router as task_router
from app.api.finance import router as finance_router

app = FastAPI(title="Backend API")

app.include_router(task_router, prefix="/tasks")
app.include_router(finance_router, prefix="/finance")

@app.get("/health")
def health():
    return {"status": "backend running"}
