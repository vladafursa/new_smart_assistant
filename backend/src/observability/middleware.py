import time

from starlette.middleware.base import BaseHTTPMiddleware

from .metrics import REQUEST_COUNT, REQUEST_LATENCY


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.time()
        response = await call_next(request)
        latency = time.time() - start

        endpoint = request.url.path

        REQUEST_COUNT.labels(
            method=request.method, endpoint=endpoint, status=response.status_code
        ).inc()

        REQUEST_LATENCY.labels(endpoint=endpoint).observe(latency)

        return response
