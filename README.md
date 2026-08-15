# Briela Sin Fronteras — sitio web

Sitio institucional de Briela Sin Fronteras (BSF), ONG peruana enfocada en
educacion, salud, medio ambiente y ciencia/tecnologia con poblaciones vulnerables.
Reconstruccion completa sobre Wagtail, con todo el contenido editable desde el
panel de administracion (sin tocar codigo ni desplegar para publicar).

## Stack

- [Wagtail](https://wagtail.org/) 6 sobre Django 5, Python 3.12
- PostgreSQL 16
- Tailwind CSS 4 (compilado en un contenedor Node propio)
- Alpine.js para interactividad puntual (sin framework SPA)
- Docker + Docker Compose v2
- Gunicorn + Nginx en produccion, WhiteNoise en desarrollo
- Ruff, Black, djLint y pre-commit para calidad de codigo
- pytest + pytest-django para pruebas

## Requisitos

- Docker Engine y el plugin Docker Compose v2 (`docker compose version`)
- Copia de `.env.example` como `.env`

## Puesta en marcha (desarrollo)

```bash
cp .env.example .env
docker compose up --build
```

En otra terminal, aplica las migraciones y crea un superusuario:

```bash
make migrate
make superuser
```

El sitio queda disponible en http://localhost:8000 y el panel de administracion
de Wagtail en http://localhost:8000/admin/.

El contenedor `node` recompila los estilos de Tailwind (`frontend/`) en cuanto
detecta cambios; no hace falta ningun paso manual adicional.

## Comandos frecuentes (Makefile)

| Comando            | Que hace                                             |
|---------------------|-------------------------------------------------------|
| `make up`            | Levanta todos los servicios (web, db, node)           |
| `make migrate`       | Aplica migraciones de Django                          |
| `make makemigrations`| Genera migraciones nuevas                             |
| `make shell`         | Abre el shell de Django dentro del contenedor web     |
| `make dbshell`       | Abre `psql` contra la base de datos                   |
| `make superuser`     | Crea un usuario administrador de Wagtail              |
| `make lint`          | Corre ruff, black --check y djlint --check            |
| `make fmt`           | Aplica formato con ruff, black y djlint                |
| `make test`          | Corre la suite de pytest                              |

## Estructura del repositorio

```
compose.yml            Orquestacion para desarrollo
compose.prod.yml        Orquestacion para produccion (Fase 6)
Dockerfile               Imagen de la app Django/Wagtail
Dockerfile.node          Imagen para compilar Tailwind
frontend/                Fuente de estilos (Tailwind) y JS (Alpine)
src/                      Proyecto Django/Wagtail
  config/                 Settings (base/dev/prod), urls, wsgi/asgi
  core/                   Configuracion global del sitio (SiteSettings)
  home/                   Pagina de inicio
  nosotros/               Pagina institucional (mision, vision, equipo)
  areas/                  Areas de trabajo
  proyectos/              Proyectos de la ONG
  testimonios/            Testimonios de voluntarios, beneficiarios y aliados
  contacto/                Formularios de voluntariado, donacion y empresas
docs/                     Documentacion (despliegue, manual del editor)
deploy/nginx/             Configuracion de Nginx para produccion
```

## Estado del proyecto

Este repositorio se construye por fases, con revision al final de cada una:

- [x] Fase 0 — Cimientos (estructura, Docker, Wagtail arrancando, Tailwind compilando)
- [ ] Fase 1 — Modelo de contenido
- [ ] Fase 2 — Diseno (tokens, componentes, plantilla maestra)
- [ ] Fase 3 — Home
- [ ] Fase 4 — Paginas internas y formularios
- [ ] Fase 5 — SEO y rendimiento
- [ ] Fase 6 — Produccion

## Licencia

MIT. Ver [LICENSE](LICENSE).
