from .base import *  # noqa: F401,F403

DEBUG = False

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 30  # 30 dias
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# La politica CSP definitiva (origenes de fuentes, Google Analytics, Meta
# Pixel, etc.) se define en la Fase 6 junto con Nginx y docs/DESPLIEGUE.md.

if not SECRET_KEY:  # noqa: F405
    raise ValueError("DJANGO_SECRET_KEY es obligatorio en produccion")
