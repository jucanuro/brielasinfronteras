from django.core.validators import RegexValidator
from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.fields import RichTextField
from wagtail.models import Orderable

RUC_VALIDATOR = RegexValidator(r"^\d{11}$", "El RUC debe tener 11 dígitos numéricos.")
TELEFONO_VALIDATOR = RegexValidator(
    r"^\+?\d{1,3}[\s-]?\d{6,12}$",
    "Ingresa un teléfono válido, con prefijo de país. Ej. +51 999 999 999.",
)


class SEOPageMixin(models.Model):
    """Campos SEO comunes a todas las páginas públicas del sitio.

    Se combina por herencia múltiple con wagtail.models.Page, por ejemplo:
    class HomePage(SEOPageMixin, Page). Los campos seo_title y
    search_description ya existen en Page y no se duplican aquí.
    """

    imagen_social = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name="Imagen para redes sociales",
        help_text=(
            "Se usa como imagen Open Graph / Twitter Card al compartir esta "
            "página. Si se deja vacía, Fase 5 definirá una imagen por defecto."
        ),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    noindex = models.BooleanField(
        verbose_name="No indexar en buscadores",
        help_text=(
            "Marca esta casilla para pedir a los buscadores que no muestren "
            "esta página en resultados."
        ),
        default=False,
    )

    class Meta:
        abstract = True


def seo_promote_panels():
    """Lista nueva de paneles SEO para agregar a promote_panels de cada página.

    Se define como función (no como lista a nivel de módulo) para evitar que
    varias páginas compartan y muten la misma lista de paneles.
    """
    return [
        FieldPanel("seo_title"),
        FieldPanel("search_description"),
        FieldPanel("imagen_social"),
        FieldPanel("noindex"),
    ]


@register_setting(icon="cog")
class SiteSettings(ClusterableModel, BaseSiteSetting):
    class Meta:
        verbose_name = "Configuración del sitio"

    logo = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name="Logo",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    favicon = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name="Favicon",
        help_text="Idealmente una imagen cuadrada simple, se usa en la pestaña del navegador.",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    nombre_legal = models.CharField(
        verbose_name="Nombre legal de la organización", max_length=255, blank=True
    )
    ruc = models.CharField(
        verbose_name="RUC", max_length=11, validators=[RUC_VALIDATOR], blank=True
    )
    direccion = models.TextField(verbose_name="Dirección", blank=True)
    texto_legal_footer = RichTextField(
        verbose_name="Texto legal del pie de página",
        help_text="Ej. datos de inscripción como asociación sin fines de lucro.",
        features=["bold", "italic", "link"],
        blank=True,
    )

    correo_general = models.EmailField(verbose_name="Correo general", blank=True)
    correo_voluntariado = models.EmailField(verbose_name="Correo de voluntariado", blank=True)
    correo_donaciones = models.EmailField(verbose_name="Correo de donaciones", blank=True)
    correo_empresas = models.EmailField(verbose_name="Correo para empresas", blank=True)

    telefono = models.CharField(
        verbose_name="Teléfono",
        max_length=20,
        validators=[TELEFONO_VALIDATOR],
        blank=True,
        help_text="Con prefijo de país. Ej. +51 999 999 999.",
    )
    whatsapp = models.CharField(
        verbose_name="WhatsApp",
        max_length=20,
        validators=[TELEFONO_VALIDATOR],
        blank=True,
        help_text="Con prefijo de país. Ej. +51 999 999 999.",
    )

    google_analytics_id = models.CharField(
        verbose_name="ID de Google Analytics",
        max_length=50,
        blank=True,
        help_text="Formato G-XXXXXXX.",
    )
    meta_pixel_id = models.CharField(verbose_name="ID de Meta Pixel", max_length=50, blank=True)

    panels = [
        MultiFieldPanel(
            [FieldPanel("logo"), FieldPanel("favicon")],
            heading="Identidad visual",
        ),
        MultiFieldPanel(
            [
                FieldPanel("nombre_legal"),
                FieldPanel("ruc"),
                FieldPanel("direccion"),
                FieldPanel("texto_legal_footer"),
            ],
            heading="Datos legales",
        ),
        MultiFieldPanel(
            [
                FieldPanel("correo_general"),
                FieldPanel("correo_voluntariado"),
                FieldPanel("correo_donaciones"),
                FieldPanel("correo_empresas"),
            ],
            heading="Correos por área",
        ),
        MultiFieldPanel(
            [FieldPanel("telefono"), FieldPanel("whatsapp")],
            heading="Teléfono y WhatsApp",
        ),
        InlinePanel("redes_sociales", heading="Redes sociales", label="Red social"),
        MultiFieldPanel(
            [FieldPanel("google_analytics_id"), FieldPanel("meta_pixel_id")],
            heading="Medición",
        ),
    ]


class RedSocial(Orderable):
    settings = ParentalKey(SiteSettings, on_delete=models.CASCADE, related_name="redes_sociales")
    red = models.CharField(
        verbose_name="Red social",
        max_length=20,
        choices=[
            ("facebook", "Facebook"),
            ("instagram", "Instagram"),
            ("tiktok", "TikTok"),
            ("youtube", "YouTube"),
            ("linkedin", "LinkedIn"),
            ("x", "X (Twitter)"),
            ("whatsapp", "WhatsApp"),
            ("otro", "Otro"),
        ],
    )
    url = models.URLField(verbose_name="URL")

    panels = [FieldPanel("red"), FieldPanel("url")]

    class Meta(Orderable.Meta):
        verbose_name = "Red social"
        verbose_name_plural = "Redes sociales"
