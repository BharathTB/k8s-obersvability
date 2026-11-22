import time
from flask import request, g, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

REQUEST_COUNT = Counter(
    "http_requests_total", "Total HTTP requests",
    ["method", "endpoint", "status"]
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds", "Request latency in seconds",
    ["endpoint"]
)

def init_metrics(app):
    @app.before_request
    def start_timer():
        g.start = time.perf_counter()

    @app.after_request
    def record(response):
        endpoint = request.url_rule.rule if request.url_rule else "unmatched"
        if endpoint != "/metrics":
            duration = time.perf_counter() - g.start
            REQUEST_COUNT.labels(request.method, endpoint, str(response.status_code)).inc()
            REQUEST_LATENCY.labels(endpoint).observe(duration)
        return response

    @app.route("/metrics")
    def metrics():
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)