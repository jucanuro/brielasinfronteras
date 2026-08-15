"""Configuracion base, comun a desarrollo y produccion."""

from pathlib import Path

import environ

# src/config/settings/base.py -> parents[2] == src/
BASE_DIR = Path(__file__).resolve().parents[2]
REPO_DIR = BASE_DIR.parent

env = environ.Env()
environ.Env.read_env(REPO_DIR / ".env")

SECRET_KEY = env("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[])
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])

INSTALLED_APPS = [
    # Apps propias de Briela Sin Fronteras
    "core",
    "home",
    "nosotros",
    "areas",
    "proyectos",
    "testimonios",
    "contacto",
    # Wagtail
    "wagtail.contrib.settings",
    "wagtail.contrib.forms",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "modelcluster",
    "taggit",
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

DATABASES = {"default": env.db("DATABASE_URL")}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internacionalizacion. Solo espanol por ahora (ver PROMPT.md, seccion
# "Confirmar antes de empezar"): wagtail-localize se evalua en la Fase 1
# si se confirma soporte multi-idioma; por defecto queda desactivado.
LANGUAGE_CODE = "es"
TIME_ZONE = "America/Lima"
USE_I18N = True
USE_TZ = True
WAGTAIL_I18N_ENABLED = False

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django permite un maximo de 1000 campos por formulario; los StreamField y
# paneles de Wagtail con muchos bloques pueden superarlo facilmente.
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10_000

# --- Archivos estaticos y media ----------------------------------------
# "static/" recibe el CSS compilado por Tailwind (frontend/src/styles ->
# src/static/css/main.css). El JS de frontend/src/js/ se sirve tal cual, sin
# paso de build, bajo el mismo prefijo "js/" que usan las plantillas.
STATICFILES_DIRS = [
    BASE_DIR / "static",
    ("js", REPO_DIR / "frontend" / "src" / "js"),
]
STATIC_ROOT = REPO_DIR / "staticfiles"
STATIC_URL = "/static/"

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

# --- Wagtail --------------------------------------------------------------
WAGTAIL_SITE_NAME = "Briela Sin Fronteras"
WAGTAILADMIN_BASE_URL = env("WAGTAILADMIN_BASE_URL", default="http://localhost:8000")

WAGTAILSEARCH_BACKENDS = {
    "default": {"BACKEND": "wagtail.search.backends.database"},
}

WAGTAILDOCS_EXTENSIONS = [
    "csv",
    "docx",
    "key",
    "odt",
    "pdf",
    "pptx",
    "rtf",
    "txt",
    "xlsx",
    "zip",
]

# --- Correo -----------------------------------------------------------
EMAIL_BACKEND = env("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = env("EMAIL_HOST", default="")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="no-responder@brielasinfronteras.org")
# Correo unico de contacto mientras no se configuren buzones por area en
# core.SiteSettings (Fase 1).
CONTACT_EMAIL = env("CONTACT_EMAIL", default="contacto@brielasinfronteras.org")

# --- reCAPTCHA (se activa en la Fase 4, junto con los formularios) ------
RECAPTCHA_ENABLED = env.bool("RECAPTCHA_ENABLED", default=False)
