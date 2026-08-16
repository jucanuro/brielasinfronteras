from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Orderable, Page

from core.blocks import CitaBlock, DatosBlock, GaleriaBlock, ImagenBlock, ParrafoBlock, VideoBlock
from core.models import SEOPageMixin, seo_promote_panels


class EstadoProyecto(models.TextChoices):
    PLANIFICADO = "planificado", "Planificado"
    EN_CURSO = "en_curso", "En curso"
    FINALIZADO = "finalizado", "Finalizado"


class ProyectosIndexPage(SEOPageMixin, Page):
    """Índice de proyectos, en /proyectos/."""

    intro = RichTextField(
        verbose_name="Introducción", features=["bold", "italic", "link"], blank=True
    )

    content_panels = Page.content_panels + [FieldPanel("intro")]
    promote_panels = Page.promote_panels + seo_promote_panels()

    parent_page_types = ["home.HomePage"]
    subpage_types = ["proyectos.ProyectoPage"]
    max_count = 1

    class Meta:
        verbose_name = "Índice de proyectos"


class ProyectoPage(SEOPageMixin, Page):
    """Un proyecto de la ONG, en /proyectos/<slug>/."""

    area = models.ForeignKey(
        "areas.AreaDeTrabajoPage",
        verbose_name="Área de trabajo",
        on_delete=models.PROTECT,
        related_name="proyectos",
    )
    resumen = models.CharField(verbose_name="Resumen", max_length=300)
    imagen_destacada = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name="Imagen destacada",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    contenido = StreamField(
        [
            ("parrafo", ParrafoBlock()),
            ("imagen", ImagenBlock()),
            ("cita", CitaBlock()),
            ("galeria", GaleriaBlock()),
            ("video", VideoBlock()),
            ("datos", DatosBlock()),
        ],
        verbose_name="Contenido",
        blank=True,
    )
    ubicacion = models.CharField(
        verbose_name="Ubicación",
        max_length=150,
        help_text="Distrito/ciudad y región, ej. 'Villa El Salvador, Lima'.",
    )
    fecha_inicio = models.DateField(verbose_name="Fecha de inicio", null=True, blank=True)
    fecha_fin = models.DateField(
        verbose_name="Fecha de fin",
        null=True,
        blank=True,
        help_text="Déjalo vacío si el proyecto sigue en curso.",
    )
    estado = models.CharField(
        verbose_name="Estado",
        max_length=20,
        choices=EstadoProyecto.choices,
        default=EstadoProyecto.PLANIFICADO,
    )
    beneficiarios = models.PositiveIntegerField(
        verbose_name="Número de beneficiarios", null=True, blank=True
    )
    destacado = models.BooleanField(
        verbose_name="Destacado",
        default=False,
        help_text="Los proyectos destacados aparecen primero en la portada.",
    )
    orden = models.PositiveIntegerField(verbose_name="Orden", default=0)

    content_panels = Page.content_panels + [
        FieldPanel("area"),
        FieldPanel("resumen"),
        FieldPanel("imagen_destacada"),
        FieldPanel("contenido"),
        InlinePanel("galeria", heading="Galería de fotos", label="Foto"),
        MultiFieldPanel(
            [
                FieldPanel("ubicacion"),
                FieldPanel("fecha_inicio"),
                FieldPanel("fecha_fin"),
                FieldPanel("estado"),
                FieldPanel("beneficiarios"),
            ],
            heading="Datos del proyecto",
        ),
        InlinePanel("aliados", heading="Aliados", label="Aliado"),
        MultiFieldPanel([FieldPanel("destacado"), FieldPanel("orden")], heading="Visibilidad"),
    ]
    promote_panels = Page.promote_panels + seo_promote_panels()

    parent_page_types = ["proyectos.ProyectosIndexPage"]
    subpage_types = []

    class Meta:
        verbose_name = "Proyecto"


class ImagenGaleria(Orderable):
    page = ParentalKey(ProyectoPage, on_delete=models.CASCADE, related_name="galeria")
    imagen = models.ForeignKey(
        "wagtailimages.Image", verbose_name="Imagen", on_delete=models.CASCADE, related_name="+"
    )
    leyenda = models.CharField(verbose_name="Leyenda", max_length=200, blank=True)

    panels = [FieldPanel("imagen"), FieldPanel("leyenda")]

    class Meta(Orderable.Meta):
        verbose_name = "Foto de galería"
        verbose_name_plural = "Galería de fotos"


class Aliado(Orderable):
    page = ParentalKey(ProyectoPage, on_delete=models.CASCADE, related_name="aliados")
    nombre = models.CharField(verbose_name="Nombre", max_length=150)
    logo = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name="Logo",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    url = models.URLField(verbose_name="URL", blank=True)

    panels = [FieldPanel("nombre"), FieldPanel("logo"), FieldPanel("url")]

    class Meta(Orderable.Meta):
        verbose_name = "Aliado"
        verbose_name_plural = "Aliados"
