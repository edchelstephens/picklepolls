from picklepolls.settings.base import *

CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


MIDDLEWARE = (
    [
        "django_prometheus.middleware.PrometheusBeforeMiddleware",
    ]
    + MIDDLEWARE
    + [
        "django_prometheus.middleware.PrometheusAfterMiddleware",
    ]
)


STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    },
}


STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
