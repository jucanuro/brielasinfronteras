from django.core.validators import FileExtensionValidator
from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.models import Orderable, Page

from core.models import SEOPageMixin, seo_promote_panels
from home.blocks import SECCIONES_HOME_BLOCKS

VIDEO_VALIDATOR = FileExtensionValidator(["mp4", "webm"])


class HomePage(SEOPageMixin, Page):
    """Pagina de inicio: hero en video, cifras de impacto y orden de secciones."""

    video_fondo = models.FileField(
        verbose_name="Video de fondo (archivo)",
        upload_to="home/videos/",
        validators=[VIDEO_VALIDATOR],
        blank=True,
        help_text=(
            "MP4 o WebM, recomendado menos de 2MB, 8-12 segundos, sin audio. "
            "Alternativa: completa la URL de video más abajo."
        ),
    )
    video_fondo_url = models.URLField(
        verbose_name="Video de fondo (URL)",
        blank=True,
        help_text=(
            "Alternativa a subir un archivo: enlace a un video alojado "
            "externamente. Si ambos campos están completos, el archivo subido "
            "tiene prioridad."
        ),
    )
    video_fondo_poster = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name="Imagen de portada del video (poster)",
        help_text=(
            "Obligatoria. Se muestra mientras el video carga, en móvil y "
            "cuando la persona prefiere movimiento reducido."
        ),
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    video_fondo_movil = models.FileField(
        verbose_name="Video de fondo para móvil (opcional)",
        upload_to="home/videos/",
        validators=[VIDEO_VALIDATOR],
        blank=True,
        help_text="Opcional. Versión más liviana del video para conexiones móviles.",
    )

    titular = models.CharField(verbose_name="Titular", max_length=200, default="")
    subtitulo = models.CharField(verbose_name="Subtítulo", max_length=300, blank=True)

    secciones = StreamField(
        SECCIONES_HOME_BLOCKS,
        verbose_name="Orden de secciones",
        blank=True,
        help_text="Agrega y ordena las secciones de la portada, sin repetirlas.",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("video_fondo"),
                FieldPanel("video_fondo_url"),
                FieldPanel("video_fondo_poster"),
                FieldPanel("video_fondo_movil"),
            ],
            heading="Video de fondo (hero)",
        ),
        MultiFieldPanel(
            [FieldPanel("titular"), FieldPanel("subtitulo")],
            heading="Texto del hero",
        ),
        InlinePanel("botones_hero", heading="Botones del hero", label="Botón", max_num=2),
        InlinePanel("cifras_impacto", heading="Cifras de impacto", label="Cifra"),
        FieldPanel("secciones"),
    ]
    promote_panels = Page.promote_panels + seo_promote_panels()

    subpage_types = [
        "nosotros.NosotrosPage",
        "areas.AreasIndexPage",
        "proyectos.ProyectosIndexPage",
        "contacto.ContactoPage",
    ]

    class Meta:
        verbose_name = "Página de inicio"


class BotonHero(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name="botones_hero")
    texto = models.CharField(verbose_name="Texto del botón", max_length=50)
    pagina_destino = models.ForeignKey(
        "wagtailcore.Page",
        verbose_name="Página de destino",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    url_externa = models.URLField(verbose_name="URL externa", blank=True)
    estilo = models.CharField(
        verbose_name="Estilo",
        max_length=20,
        choices=[("primario", "Primario"), ("secundario", "Secundario")],
        default="primario",
    )

    panels = [
        FieldPanel("texto"),
        FieldPanel("pagina_destino"),
        FieldPanel("url_externa"),
        FieldPanel("estilo"),
    ]

    class Meta(Orderable.Meta):
        verbose_name = "Botón del hero"
        verbose_name_plural = "Botones del hero"


class CifraImpacto(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name="cifras_impacto")
    numero = models.PositiveIntegerField(verbose_name="Número")
    sufijo = models.CharField(
        verbose_name="Sufijo", max_length=10, blank=True, help_text="Ej. '+', '%', 'k'."
    )
    etiqueta = models.CharField(verbose_name="Etiqueta", max_length=100)

    panels = [FieldPanel("numero"), FieldPanel("sufijo"), FieldPanel("etiqueta")]

    class Meta(Orderable.Meta):
        verbose_name = "Cifra de impacto"
        verbose_name_plural = "Cifras de impacto"
