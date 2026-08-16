"""Carga contenido real de brielasinfronteras.org para que el sitio se vea
completo y creíble desde el primer arranque, sin lorem ipsum.

Fuente: brielasinfronteras.org (investigado el 2026-08-15). Misión, visión,
nombres de los 6 valores, las 4 áreas, las 3 cifras de impacto, el titular del
hero y los 3 testimonios (Lucero, Jacqueline, Angie) son texto real del sitio
actual. El sitio actual no publica: descripciones de valores, descripciones de
áreas, datos legales (RUC/dirección/correos/redes), ni un listado de
proyectos — esos campos quedan marcados como "[PENDIENTE DE COMPLETAR CON
BSF]" o se omiten, en vez de inventarse. Los 4 proyectos son de ejemplo,
marcados explícitamente como tales, tal como pide PROMPT.md.

Idempotente: se puede correr varias veces sin duplicar contenido.
"""

import io

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from PIL import Image as PILImage
from PIL import ImageDraw
from wagtail.images import get_image_model
from wagtail.models import Site

from areas.models import AreaDeTrabajoPage, AreasIndexPage
from core.models import SiteSettings
from home.models import BotonHero, CifraImpacto, HomePage
from nosotros.models import NosotrosPage, Valor
from proyectos.models import EstadoProyecto, ProyectoPage, ProyectosIndexPage
from testimonios.models import RolTestimonio, Testimonio

PENDIENTE = "[PENDIENTE DE COMPLETAR CON BSF]"

VALORES = ["Solidaridad", "Transparencia", "Inclusión", "Cooperación", "Compromiso", "Respeto"]

AREAS = [
    ("Educación", "#12369B"),
    ("Salud", "#0E9488"),
    ("Medio Ambiente", "#2E7D32"),
    ("Ciencia y Tecnología", "#6A3FA0"),
]

TESTIMONIOS = [
    (
        "Lucero",
        "Siento una alegría inmensa al ver a los niños abrir ese regalito "
        "llenos de ilusión. Es muy gratificante ser parte de esto.",
    ),
    (
        "Jacqueline",
        "Ser parte de Briela Sin Fronteras significa unión, enseñanza y que "
        "la comunidad se siente escuchada, motivada y con ganas de salir "
        "adelante.",
    ),
    (
        "Angie",
        "Ser parte de la ONG es despertar cada día sabiendo que tus "
        "acciones, por pequeñas que sean, están construyendo un mundo más "
        "justo.",
    ),
]

PROYECTOS_EJEMPLO = [
    (
        "[Ejemplo] Aulas que Enseñan",
        "Educación",
        "Refuerzo escolar y útiles para niñas y niños de zonas vulnerables.",
        "Villa El Salvador, Lima",
        EstadoProyecto.EN_CURSO,
        80,
        True,
    ),
    (
        "[Ejemplo] Salud en Comunidad",
        "Salud",
        "Jornadas de salud preventiva y donación de medicamentos básicos.",
        "Comas, Lima",
        EstadoProyecto.PLANIFICADO,
        150,
        False,
    ),
    (
        "[Ejemplo] Bosques Vivos",
        "Medio Ambiente",
        "Reforestación y educación ambiental con familias de la comunidad.",
        "Chosica, Lima",
        EstadoProyecto.FINALIZADO,
        60,
        False,
    ),
    (
        "[Ejemplo] Aprende Code",
        "Ciencia y Tecnología",
        "Talleres de programación básica para adolescentes.",
        "San Juan de Lurigancho, Lima",
        EstadoProyecto.EN_CURSO,
        40,
        True,
    ),
]


def _placeholder_image(titulo, color_hex):
    """Genera una imagen sólida con el título superpuesto, marcada como
    marcador de posición hasta que BSF entregue fotos reales."""
    Image = get_image_model()
    existente = Image.objects.filter(title=titulo).first()
    if existente:
        return existente, False

    color = tuple(int(color_hex.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
    lienzo = PILImage.new("RGB", (1200, 800), color=color)
    dibujo = ImageDraw.Draw(lienzo)
    dibujo.text((60, 380), "Imagen de marcador — pendiente foto real", fill="white")

    buffer = io.BytesIO()
    lienzo.save(buffer, format="JPEG")
    imagen = Image(title=titulo)
    imagen.file.save(f"{titulo}.jpg", ContentFile(buffer.getvalue()), save=True)
    return imagen, True


class Command(BaseCommand):
    help = "Carga contenido real de brielasinfronteras.org para la demo (idempotente)."

    def handle(self, *args, **options):
        self._seed_nosotros()
        self._seed_home()
        areas_por_nombre = self._seed_areas()
        self._seed_proyectos(areas_por_nombre)
        self._seed_testimonios()
        self._seed_site_settings()
        self.stdout.write(self.style.SUCCESS("seed_demo terminó correctamente."))

    def _skip(self, mensaje):
        self.stdout.write(self.style.WARNING(f"  omitido: {mensaje}"))

    def _seed_nosotros(self):
        page = NosotrosPage.objects.first()
        if page is None:
            self._skip("NosotrosPage no existe todavía (falta correr las migraciones).")
            return

        page.mision = (
            "<p>Contribuir al desarrollo social integral mediante la educación, "
            "la salud, la sostenibilidad ambiental y la ciencia, trabajando en "
            "coordinación con instituciones gubernamentales, empresas y "
            "organizaciones de todo el mundo.</p>"
        )
        page.vision = (
            "<p>Ser una organización referente a nivel nacional e internacional "
            "en la construcción de puentes entre culturas, comunidades e "
            "instituciones, generando impacto real y sostenible en las "
            "personas que más lo necesitan.</p>"
        )
        page.save()
        page.save_revision().publish()
        self.stdout.write("NosotrosPage: misión y visión actualizadas.")

        for orden, nombre in enumerate(VALORES):
            _, creado = Valor.objects.get_or_create(
                page=page,
                nombre=nombre,
                defaults={"icono": nombre.lower(), "descripcion": PENDIENTE, "sort_order": orden},
            )
            if not creado:
                self._skip(f"Valor '{nombre}' ya existía.")

        if not page.equipo.exists():
            self._skip("MiembroEquipo: sin nombres/fotos reales confirmados, no se crea ninguno.")

    def _seed_home(self):
        homepage = HomePage.objects.first()
        if homepage is None:
            self._skip("HomePage no existe todavía (falta correr las migraciones).")
            return

        homepage.titular = "No hay frontera cuando decides ayudar"
        homepage.subtitulo = (
            "El cambio más grande empieza con alguien que simplemente dijo: yo quiero ayudar."
        )
        if homepage.video_fondo_poster_id is None:
            poster, _ = _placeholder_image("Poster del hero", "#081A45")
            homepage.video_fondo_poster = poster
        homepage.save()
        homepage.save_revision().publish()
        self.stdout.write("HomePage: titular, subtítulo y poster actualizados.")

        cifras = [
            (300, "+", "Personas beneficiadas"),
            (25, "+", "Voluntarios activos"),
            (1, "", "Año de fundación"),
        ]
        for orden, (numero, sufijo, etiqueta) in enumerate(cifras):
            _, creado = CifraImpacto.objects.get_or_create(
                page=homepage,
                etiqueta=etiqueta,
                defaults={"numero": numero, "sufijo": sufijo, "sort_order": orden},
            )
            if not creado:
                self._skip(f"CifraImpacto '{etiqueta}' ya existía.")

        proyectos_index = ProyectosIndexPage.objects.first()
        if not homepage.botones_hero.exists() and proyectos_index is not None:
            BotonHero.objects.create(
                page=homepage,
                texto="Ver nuestro trabajo",
                pagina_destino=proyectos_index,
                estilo="primario",
                sort_order=0,
            )
            self.stdout.write("HomePage: botón 'Ver nuestro trabajo' creado.")

    def _seed_areas(self):
        areas_index = AreasIndexPage.objects.first()
        if areas_index is None:
            self._skip("AreasIndexPage no existe todavía (falta correr las migraciones).")
            return {}

        areas_por_nombre = {}
        for orden, (nombre, color) in enumerate(AREAS):
            existente = AreaDeTrabajoPage.objects.filter(title=nombre).first()
            if existente:
                self._skip(f"Área '{nombre}' ya existía.")
                areas_por_nombre[nombre] = existente
                continue

            imagen, _ = _placeholder_image(f"Área — {nombre}", color)
            svg = (
                f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
                f'<circle cx="32" cy="32" r="28" fill="{color}" /></svg>'
            ).encode()

            pagina = AreaDeTrabajoPage(
                title=nombre,
                imagen=imagen,
                descripcion_corta=PENDIENTE,
                descripcion_larga=f"<p>{PENDIENTE}</p>",
                color_acento=color,
                orden=orden,
            )
            pagina.icono_svg.save(f"{nombre}.svg", ContentFile(svg), save=False)
            areas_index.add_child(instance=pagina)
            pagina.save_revision().publish()
            areas_por_nombre[nombre] = pagina
            self.stdout.write(f"Área de trabajo creada: {nombre}")

        return areas_por_nombre

    def _seed_proyectos(self, areas_por_nombre):
        proyectos_index = ProyectosIndexPage.objects.first()
        if proyectos_index is None:
            self._skip("ProyectosIndexPage no existe todavía (falta correr las migraciones).")
            return

        for (
            titulo,
            area_nombre,
            resumen,
            ubicacion,
            estado,
            beneficiarios,
            destacado,
        ) in PROYECTOS_EJEMPLO:
            if ProyectoPage.objects.filter(title=titulo).exists():
                self._skip(f"Proyecto '{titulo}' ya existía.")
                continue

            area = areas_por_nombre.get(area_nombre)
            if area is None:
                self._skip(f"Proyecto '{titulo}': no se encontró el área '{area_nombre}'.")
                continue

            imagen, _ = _placeholder_image(f"Proyecto — {titulo}", "#12369B")
            pagina = ProyectoPage(
                title=titulo,
                area=area,
                resumen=resumen,
                imagen_destacada=imagen,
                ubicacion=ubicacion,
                estado=estado,
                beneficiarios=beneficiarios,
                destacado=destacado,
                contenido=[
                    (
                        "parrafo",
                        f"<p>{resumen} Este es un proyecto de ejemplo para la demo; "
                        "debe reemplazarse con datos reales de un proyecto de "
                        "Briela Sin Fronteras.</p>",
                    )
                ],
            )
            proyectos_index.add_child(instance=pagina)
            pagina.save_revision().publish()
            self.stdout.write(f"Proyecto de ejemplo creado: {titulo}")

    def _seed_testimonios(self):
        for orden, (nombre, texto) in enumerate(TESTIMONIOS):
            _, creado = Testimonio.objects.get_or_create(
                nombre=nombre,
                defaults={
                    "rol": RolTestimonio.VOLUNTARIO,
                    "texto": texto,
                    "orden": orden,
                },
            )
            if not creado:
                self._skip(f"Testimonio de '{nombre}' ya existía.")
            else:
                self.stdout.write(f"Testimonio creado: {nombre}")

    def _seed_site_settings(self):
        site = Site.objects.filter(is_default_site=True).first()
        if site is None:
            self._skip("No hay Site por defecto configurado.")
            return

        settings = SiteSettings.for_site(site)
        if not settings.nombre_legal:
            settings.nombre_legal = "Briela Sin Fronteras"
            settings.save()
            self.stdout.write("SiteSettings: nombre legal actualizado.")
        else:
            self._skip("SiteSettings.nombre_legal ya tenía un valor.")
