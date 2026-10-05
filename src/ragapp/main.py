from ragapp.ops import router as ops_router
from fastapi import FastAPI, HTTPException
from ragapp.search import answer
app = FastAPI()
app.include_router(ops_router, prefix="/v1")

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.post("/ask")
def ask(body: dict):
    try:
        return answer(body.get("question"), body.get("source"), body.get("session_id"), body.get("tenant"))
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc
