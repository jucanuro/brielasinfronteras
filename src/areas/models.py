from django.core.validators import FileExtensionValidator, RegexValidator
from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page

from core.models import SEOPageMixin, seo_promote_panels

COLOR_HEX_VALIDATOR = RegexValidator(
    r"^#[0-9A-Fa-f]{6}$", "Ingresa un color hexadecimal válido, ej. #12369B."
)


class AreasIndexPage(SEOPageMixin, Page):
    """Índice de áreas de trabajo, en /areas-de-trabajo/."""

    intro = RichTextField(
        verbose_name="Introducción",
        features=["bold", "italic", "link"],
        blank=True,
        help_text="Texto introductorio antes del listado de áreas.",
    )

    content_panels = Page.content_panels + [FieldPanel("intro")]
    promote_panels = Page.promote_panels + seo_promote_panels()

    parent_page_types = ["home.HomePage"]
    subpage_types = ["areas.AreaDeTrabajoPage"]
    max_count = 1

    class Meta:
        verbose_name = "Índice de áreas de trabajo"


class AreaDeTrabajoPage(SEOPageMixin, Page):
    """Un área de trabajo de la ONG, en /areas-de-trabajo/<slug>/."""

    icono_svg = models.FileField(
        verbose_name="Ícono (SVG)",
        upload_to="areas/iconos/",
        validators=[FileExtensionValidator(["svg"])],
        help_text=(
            "Archivo SVG. Se muestra siempre como imagen, nunca insertado directo en el HTML."
        ),
    )
    imagen = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name="Imagen",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    descripcion_corta = models.CharField(
        verbose_name="Descripción corta",
        max_length=200,
        help_text="Resumen breve para tarjetas y menús.",
    )
    descripcion_larga = RichTextField(
        verbose_name="Descripción larga", features=["bold", "italic", "link", "ol", "ul"]
    )
    color_acento = models.CharField(
        verbose_name="Color de acento",
        max_length=7,
        validators=[COLOR_HEX_VALIDATOR],
        help_text="Color hexadecimal, ej. #12369B.",
    )
    orden = models.PositiveIntegerField(verbose_name="Orden", default=0)
    activo = models.BooleanField(
        verbose_name="Activo",
        default=True,
        help_text=(
            "Si está desactivada, el área no aparece en los listados aunque la "
            "página siga publicada."
        ),
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [FieldPanel("icono_svg"), FieldPanel("color_acento")], heading="Identidad visual"
        ),
        FieldPanel("imagen"),
        FieldPanel("descripcion_corta"),
        FieldPanel("descripcion_larga"),
        MultiFieldPanel([FieldPanel("orden"), FieldPanel("activo")], heading="Visibilidad y orden"),
    ]
    promote_panels = Page.promote_panels + seo_promote_panels()

    parent_page_types = ["areas.AreasIndexPage"]
    subpage_types = []

    class Meta:
        verbose_name = "Área de trabajo"
        verbose_name_plural = "Áreas de trabajo"
