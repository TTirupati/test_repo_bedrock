```python
import time
from typing import Optional
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import redis

app = FastAPI()

# Redis connection
r = redis.Redis(host='localhost', port=6379, db=0)

# Middleware to track request counts per API key
@app.middleware("http")
async def request_limiter(request: Request, call_next):
    api_key = request.headers.get("X-API-Key")
    if not api_key:
        return JSONResponse(status_code=401, content={"error": "API key is required"})

    # Check the request count for the API key
    key = f"request_count_{api_key}"
    count = r.get(key)
    if count is None:
        r.set(key, 1, ex=60)  # Set initial count to 1 and expire in 60 seconds
    else:
        count = int(count)
        if count >= 100:
            return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})
        r.incr(key)

    response = await call_next(request)
    return response

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/protected")
async def protected():
    return {"message": "This is a protected API endpoint."}
```