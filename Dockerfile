FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq5 \
        gettext \
        curl \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./
RUN pip install --upgrade pip && pip install .[dev]

COPY src ./src

# Usuario no root con el mismo UID/GID por defecto del host, para que los
# archivos que Django escriba en los volumenes montados (migraciones,
# media) no queden con dueño root.
RUN groupadd --gid 1000 app && useradd --uid 1000 --gid app --create-home app \
    && chown -R app:app /app
USER app

WORKDIR /app/src

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
