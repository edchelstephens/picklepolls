from .base import *

MIDDLEWARE = (
    [
        "django_prometheus.middleware.PrometheusBeforeMiddleware",
    ]
    + MIDDLEWARE
    + [
        "django_prometheus.middleware.PrometheusAfterMiddleware",
    ]
)
