from prometheus_client import Counter, Gauge, Histogram

REQUEST_COUNT = Counter(
    "http_requests_total", "Total HTTP requests", ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_latency_seconds", "Latency of HTTP requests", ["endpoint"]
)
