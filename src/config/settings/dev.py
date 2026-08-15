from .base import *  # noqa: F401,F403
from .base import env

DEBUG = env.bool("DJANGO_DEBUG", default=True)

if not ALLOWED_HOSTS:  # noqa: F405
    ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Permite que WhiteNoise sirva los estaticos en dev sin correr collectstatic
# antes de cada arranque.
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = True

INTERNAL_IPS = ["127.0.0.1"]
