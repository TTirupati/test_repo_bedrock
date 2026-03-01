Here's the Python code to implement the middleware that uses Redis to track request counts per API key across multiple distributed instances of the FastAPI app:

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
import redis
from typing import Optional

app = FastAPI()

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Middleware to track request counts
class RateLimitingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        api_key = request.headers.get('X-API-Key')
        if api_key:
            # Increment the request count for the API key
            r.incr(f'request_count_{api_key}')

            # Get the current request count
            current_count = int(r.get(f'request_count_{api_key}') or '0')

            # Check if the request limit is exceeded
            if current_count > 100:
                return JSONResponse(status_code=429, content={'error': 'Rate limit exceeded'})

        response = await call_next(request)
        return response

app.add_middleware(RateLimitingMiddleware)

@app.get('/protected_endpoint')
async def protected_endpoint(api_key: Optional[str] = None):
    return {'message': 'This is a protected endpoint'}