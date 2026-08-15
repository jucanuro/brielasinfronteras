# BRIEF — Sitio web ONG Briela Sin Fronteras

## Rol
Eres tech lead + diseñador principal. Construyes desde cero el nuevo sitio de ONG
Briela Sin Fronteras (BSF), organizacion peruana sin fines de lucro: educacion,
salud, medio ambiente y ciencia/tecnologia con poblaciones vulnerables.
El sitio actual (brielasinfronteras.org) es una sola pagina con anclas, contenido
quemado en HTML, sin admin y sin paginas indexables por proyecto. Se reemplaza completo.

Audiencia por prioridad: voluntarios jovenes (movil), donantes individuales (Peru y
exterior), empresas buscando alianzas, aliados institucionales y prensa.
Quien administra el contenido NO es tecnico: todo texto, imagen, video, proyecto,
area y testimonio debe editarse desde el panel sin tocar codigo ni desplegar.

## Stack obligatorio
- Wagtail 6 sobre Django 5.x, Python 3.12
- PostgreSQL 16
- TailwindCSS 4 (build con Node en contenedor propio)
- Alpine.js (nada de React ni SPA)
- Docker + Docker Compose v2
- Gunicorn + Nginx; WhiteNoise en dev
- Ruff, Black, djLint, pre-commit; pytest + pytest-django
- Hueco listo para Celery + Redis, sin implementarlo aun
No agregues dependencias fuera de esta lista sin justificarlo en pyproject.toml.

## Repositorio
Remoto ya creado: git@github.com:jucanuro/brielasinfronteras.git (rama main)
Commits en espanol, Conventional Commits (feat:, fix:, chore:, docs:).
Un commit por fase, no uno gigante al final.
.gitignore: .env, media/, staticfiles/, __pycache__, node_modules, *.sqlite3
Nunca subir .env, credenciales ni media.

## Estructura
compose.yml, compose.prod.yml, Dockerfile, Dockerfile.node, .env.example,
.gitignore, .dockerignore, .pre-commit-config.yaml, pyproject.toml, README.md,
LICENSE, Makefile (make up/migrate/shell/lint)
docs/DESPLIEGUE.md, docs/MANUAL-EDITOR.md
deploy/nginx/default.conf
frontend/ (package.json, tailwind.config.js, src/styles/main.css, src/js/main.js)
src/ -> manage.py, config/settings/{base,dev,prod}.py, y apps:
  core, home, nosotros, areas, proyectos, testimonios, contacto
  + templates/ y static/

## Modelo de contenido
Todo modelo lleva orden, activo/publicado y campos SEO.
verbose_name y textos de ayuda del admin EN ESPANOL.

core.SiteSettings: logo, favicon, nombre legal, RUC, direccion, correos por area
(general, voluntariado, donaciones, empresas), telefono/WhatsApp, redes sociales
(repetible), texto legal del footer, ID Google Analytics, ID Meta Pixel.

home.HomePage: video de fondo (subida o URL), poster obligatorio, video movil
opcional, titular, subtitulo, hasta 2 botones, cifras de impacto (repetible:
numero, sufijo, etiqueta), y StreamField para ordenar las secciones sin codigo.

nosotros.NosotrosPage: intro, mision, vision, valores (repetible: nombre, icono,
descripcion), historia opcional en linea de tiempo, equipo (foto, nombre, cargo, bio).

areas.AreaDeTrabajo: nombre, slug, icono SVG, imagen, descripcion_corta,
descripcion_larga, color_acento, orden, activo.
Pagina propia en /areas-de-trabajo/<slug>/ que lista sus proyectos.

proyectos.ProyectoPage: titulo, slug, area (FK), resumen, contenido (StreamField:
parrafo, imagen, cita, galeria, video, datos), imagen_destacada, galeria, ubicacion,
fecha_inicio, fecha_fin, estado (planificado/en curso/finalizado), beneficiarios,
aliados (nombre + logo), destacado, orden.
Indice en /proyectos/ con filtro por area y por estado.

testimonios.Testimonio: nombre, rol (voluntario/beneficiario/aliado), foto, texto,
proyecto (FK opcional), orden, activo.

contacto.Contacto: tipo (voluntario|donacion|empresa), nombre, apellido, email,
telefono con prefijo, mensaje, estado (nuevo/en proceso/atendido/descartado),
creado, ip, origen. Campos condicionales:
- voluntario: disponibilidad, areas de interes (M2M), profesion, ciudad
- donacion: tipo (monetaria/especie/recurrente), rango de aporte, si desea recibo
- empresa: razon social, RUC, cargo, tipo de alianza
Listado en admin con filtros, buscador y exportacion CSV.

## Home (8 secciones)
1 Hero video pantalla completa con texto encima en HTML real (nunca quemado en video)
2 Cifras de impacto
3 Conocenos (mision, vision, valores del sitio actual, mejor presentados)
4 Areas de trabajo desde BD
5 Proyectos en cards desde BD + ver todos
6 Testimonios desde BD
7 Como quieres ayudar hoy: las tres vias, cada una abre su formulario
8 Footer mejor que el actual: navegacion completa, datos legales, contacto, redes

## Diseno
El diseno es un entregable. Nada de plantilla de agencia ni degradados morados.

Tokens (ajustar al logo real: circulo amarillo con lemniscata azul):
--azul-bsf #12369B | --amarillo-bsf #FCD434 | --azul-noche #081A45
--nieve #F2F4F9 | --tinta #0E1220
El amarillo NO es fondo de secciones: es acento, subrayado, estado activo y CTA.

Tipografia: display Bricolage Grotesque; cuerpo Instrument Sans (respaldo Public
Sans); monoespaciada (Space Mono o JetBrains Mono) SOLO para cifras de impacto,
fechas y beneficiarios. Tratar los numeros como datos comunica transparencia,
que es como se legitima una ONG.

Elemento firma: la lemniscata del logo como motivo estructural. Trazo SVG continuo
que enlaza secciones y se dibuja al hacer scroll, enmarca las cifras de impacto y
aparece como microinteraccion en las cards de proyecto. Es el UNICO lugar donde se
gasta audacia; todo lo demas, disciplinado y silencioso.

Reglas: movil primero (trafico movil con datos limitados), contraste AA, foco de
teclado visible, prefers-reduced-motion respetado, alt obligatorio en el admin.
Antes de codificar, escribe un plan de diseno (paleta, tipografia, wireframe ASCII,
elemento firma) y criticalo: si algo aplicaria igual a cualquier otra ONG, cambialo
y explica por que. Copy en espanol peruano, voz activa. Los botones dicen lo que
hacen: "Quiero ser voluntario", no "Enviar".

## Video del hero (innegociable)
- El poster (AVIF/WebP) es el elemento LCP: se precarga y se pinta primero
- video muted autoplay loop playsinline preload="none" + IntersectionObserver
- WebM/VP9 + MP4/H.264, 8-12 s, sin audio, objetivo bajo 2 MB
- En movil y con prefers-reduced-motion: solo el poster
- El admin avisa al editor si el archivo supera el peso recomendado
- Meta medible: LCP < 2.5 s y CLS < 0.1 en movil

## SEO
URLs limpias /proyectos/<slug>/, /areas-de-trabajo/<slug>/, /nosotros/, /contacto/
Cada proyecto y area son paginas indexables propias (hoy no existen: es la mayor
oportunidad organica del proyecto).
Campos SEO editables por pagina: titulo, meta description, imagen social, noindex.
django.contrib.sitemaps + robots.txt.
JSON-LD: NGO/NonprofitOrganization en home (logo, sameAs, direccion), Article o
Project en cada proyecto, BreadcrumbList en internas.
Open Graph y Twitter Card desde la imagen destacada.
Imagenes en WebP con srcset y loading=lazy salvo el hero.
Un solo h1 por pagina. Canonical en todas.
Redirecciones 301 desde las anclas antiguas (/#proyectos, /#conocenos).

## Formularios
Tres formularios distintos sobre el mismo modelo Contacto.
Honeypot + limite por IP + validacion en servidor. django-recaptcha configurado
pero desactivable por variable de entorno.
Al enviar: notificacion al buzon segun tipo + autorespuesta HTML al remitente.
Errores claros y especificos junto al campo que fallo.
Donaciones: en esta version solo registra la intencion. App "pagos" vacia con su
interfaz lista para Culqi/Yape (Peru) y PayPal/Stripe (exterior). NO integrar
pasarelas ahora.

## Docker y entornos
compose.yml (dev): web con recarga, db postgres:16-alpine, node con Tailwind watch.
Volumenes nombrados postgres_data y media.
compose.prod.yml: web con Gunicorn, db, nginx, build de Tailwind en etapa de
construccion, healthchecks en web y db, restart unless-stopped.
.env.example comentado: DJANGO_SECRET_KEY, DJANGO_DEBUG, DJANGO_ALLOWED_HOSTS,
DATABASE_URL, EMAIL_*, WAGTAILADMIN_BASE_URL, RECAPTCHA_*, CSRF_TRUSTED_ORIGINS.
Produccion: DEBUG=False, HSTS, cookies seguras, SECURE_SSL_REDIRECT,
X-Frame-Options, CSP basica.
docs/DESPLIEGUE.md debe documentar la instalacion de Docker Engine + plugin Compose
en Ubuntu desde el repositorio oficial de Docker (NO el paquete docker.io de
Ubuntu), incluyendo agregar el usuario al grupo docker.

## Fases (detente al final de cada una para que revise)
0 Cimientos: estructura, Docker, Postgres arriba, Wagtail en localhost:8000,
  Tailwind compilando, pre-commit, README, primer commit y push a main
1 Modelo de contenido: modelos, migraciones, admin en espanol, fixtures con el
  contenido real actual (mision, vision, valores, 3 testimonios, 4 areas)
2 Diseno: plan escrito y criticado, tokens, componentes base, plantilla maestra,
  header y footer
3 Home: las 8 secciones, hero optimizado, todo desde BD
4 Internas: nosotros, indice y detalle de proyectos, paginas de areas, contacto
5 SEO y rendimiento: sitemap, JSON-LD, metadatos, redirecciones, auditoria
  Lighthouse con resultados por escrito
6 Produccion: compose.prod.yml, Nginx, DESPLIEGUE.md, MANUAL-EDITOR.md, checklist

## Criterios de aceptacion
- docker compose up levanta todo desde cero, solo copiando .env
- Un editor no tecnico cambia el video del hero, agrega un proyecto y publica un
  testimonio sin ayuda
- Cero contenido quemado en plantillas: todo viene de BD
- Lighthouse movil: Rendimiento >= 90, Accesibilidad >= 95, SEO = 100
- Responsive de 320 px a 2560 px
- Navegable completo con teclado, foco visible
- Los tres formularios guardan, notifican y responden
- MANUAL-EDITOR.md en espanol claro con pasos numerados

## Prohibido
- React, Next.js o cualquier framework JS pesado
- Bootstrap, DaisyUI, Flowbite u otra libreria de componentes prefabricados
- Inventar contenido de la ONG (usar el actual; si falta, marcador claro y avisar)
- Integrar pasarelas de pago en esta version
- Commit de secretos
- Entregar las 6 fases sin revision intermedia

## Confirmar antes de empezar
1 Donde se aloja (VPS propio, Railway, Fly.io, Render) -> condiciona la Fase 6
2 Hay video del hero o uso marcador
3 Solo espanol o tambien ingles (afecta el modelo de datos desde ya)
4 Correos de destino de cada formulario
Si no respondo, asume: VPS propio con Nginx, video marcador, solo espanol con
wagtail-localize preinstalado pero desactivado, y un correo unico configurable.
