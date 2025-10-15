import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import redis

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))
APP_MESSAGE = os.getenv("APP_MESSAGE", "Hello from FastAPI + Redis")

# Redis client (lazy connect; handle failures gracefully)
def get_redis():
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

app = FastAPI(title="DummyRequestCounter", version="1.0.0")

@app.get("/")
def read_root():
    r = get_redis()
    try:
        hits = r.incr("hits")
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Cannot reach Redis", "detail": str(e)})
    return {"message": APP_MESSAGE, "hits": hits}

@app.get("/healthz")
def healthz():
    r = get_redis()
    try:
        pong = r.ping()
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "unhealthy", "redis": str(e)})
    return {"status": "ok", "redis": pong, "host": REDIS_HOST, "port": REDIS_PORT, "db": REDIS_DB}
