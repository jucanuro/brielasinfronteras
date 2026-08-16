from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Orderable, Page

from core.models import SEOPageMixin, seo_promote_panels


class NosotrosPage(SEOPageMixin, Page):
    """Quiénes somos: misión, visión, valores, historia y equipo."""

    intro = RichTextField(
        verbose_name="Introducción", features=["bold", "italic", "link"], blank=True
    )
    mision = RichTextField(verbose_name="Misión", features=["bold", "italic", "link"])
    vision = RichTextField(verbose_name="Visión", features=["bold", "italic", "link"])

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        MultiFieldPanel([FieldPanel("mision"), FieldPanel("vision")], heading="Misión y visión"),
        InlinePanel("valores", heading="Valores", label="Valor"),
        InlinePanel("hitos_historia", heading="Historia (línea de tiempo)", label="Hito"),
        InlinePanel("equipo", heading="Equipo", label="Integrante"),
    ]
    promote_panels = Page.promote_panels + seo_promote_panels()

    parent_page_types = ["home.HomePage"]
    subpage_types = []
    max_count = 1

    class Meta:
        verbose_name = "Página de nosotros"


class Valor(Orderable):
    page = ParentalKey(NosotrosPage, on_delete=models.CASCADE, related_name="valores")
    nombre = models.CharField(verbose_name="Nombre", max_length=80)
    icono = models.CharField(
        verbose_name="Icono",
        max_length=50,
        help_text=(
            "Nombre clave del icono, ej. 'corazon', 'manos'. El catálogo "
            "visual se define en Fase 2."
        ),
    )
    descripcion = models.TextField(verbose_name="Descripción")

    panels = [FieldPanel("nombre"), FieldPanel("icono"), FieldPanel("descripcion")]

    class Meta(Orderable.Meta):
        verbose_name = "Valor"
        verbose_name_plural = "Valores"


class HitoLineaTiempo(Orderable):
    page = ParentalKey(NosotrosPage, on_delete=models.CASCADE, related_name="hitos_historia")
    anio = models.CharField(
        verbose_name="Año", max_length=20, help_text="Ej. '2015' o un rango como '2015-2018'."
    )
    titulo = models.CharField(verbose_name="Título", max_length=150)
    descripcion = models.TextField(verbose_name="Descripción", blank=True)

    panels = [FieldPanel("anio"), FieldPanel("titulo"), FieldPanel("descripcion")]

    class Meta(Orderable.Meta):
        verbose_name = "Hito de la historia"
        verbose_name_plural = "Historia (línea de tiempo)"


class MiembroEquipo(Orderable):
    page = ParentalKey(NosotrosPage, on_delete=models.CASCADE, related_name="equipo")
    foto = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name="Foto",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    nombre = models.CharField(verbose_name="Nombre", max_length=150)
    cargo = models.CharField(verbose_name="Cargo", max_length=150)
    bio = models.TextField(verbose_name="Biografía breve", blank=True)
    activo = models.BooleanField(
        verbose_name="Activo",
        default=True,
        help_text="Desactívalo para ocultarlo del equipo sin borrar sus datos.",
    )

    panels = [
        FieldPanel("foto"),
        FieldPanel("nombre"),
        FieldPanel("cargo"),
        FieldPanel("bio"),
        FieldPanel("activo"),
    ]

    class Meta(Orderable.Meta):
        verbose_name = "Integrante del equipo"
        verbose_name_plural = "Equipo"
