from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page

from core.models import RUC_VALIDATOR, TELEFONO_VALIDATOR, SEOPageMixin, seo_promote_panels


class ContactoPage(SEOPageMixin, Page):
    """Página de contacto, en /contacto/. Los tres formularios los implementa Fase 4."""

    intro = RichTextField(
        verbose_name="Introducción",
        features=["bold", "italic", "link"],
        blank=True,
        help_text="Texto antes de los tres formularios.",
    )

    content_panels = Page.content_panels + [FieldPanel("intro")]
    promote_panels = Page.promote_panels + seo_promote_panels()

    parent_page_types = ["home.HomePage"]
    subpage_types = []
    max_count = 1

    class Meta:
        verbose_name = "Página de contacto"


class TipoContacto(models.TextChoices):
    VOLUNTARIO = "voluntario", "Quiero ser voluntario/a"
    DONACION = "donacion", "Quiero donar"
    EMPRESA = "empresa", "Colaborar como empresa"


class EstadoContacto(models.TextChoices):
    NUEVO = "nuevo", "Nuevo"
    EN_PROCESO = "en_proceso", "En proceso"
    ATENDIDO = "atendido", "Atendido"
    DESCARTADO = "descartado", "Descartado"


class TipoDonacion(models.TextChoices):
    MONETARIA = "monetaria", "Monetaria"
    ESPECIE = "especie", "En especie"
    RECURRENTE = "recurrente", "Recurrente"


class Contacto(models.Model):
    """Un envío de alguno de los tres formularios de contacto del sitio."""

    tipo = models.CharField(verbose_name="Tipo", max_length=20, choices=TipoContacto.choices)
    nombre = models.CharField(verbose_name="Nombre", max_length=100)
    apellido = models.CharField(verbose_name="Apellido", max_length=100)
    email = models.EmailField(verbose_name="Correo electrónico")
    telefono = models.CharField(
        verbose_name="Teléfono",
        max_length=20,
        validators=[TELEFONO_VALIDATOR],
        help_text="Con prefijo de país. Ej. +51 999 999 999.",
    )
    mensaje = models.TextField(verbose_name="Mensaje")
    estado = models.CharField(
        verbose_name="Estado",
        max_length=20,
        choices=EstadoContacto.choices,
        default=EstadoContacto.NUEVO,
    )
    creado = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True)
    ip = models.GenericIPAddressField(verbose_name="IP de origen", null=True, blank=True)
    origen = models.CharField(
        verbose_name="Origen",
        max_length=100,
        blank=True,
        help_text="Página o formulario de origen.",
    )

    # Campos condicionales — voluntariado
    disponibilidad = models.CharField(verbose_name="Disponibilidad", max_length=150, blank=True)
    areas_interes = models.ManyToManyField(
        "areas.AreaDeTrabajoPage",
        verbose_name="Áreas de interés",
        blank=True,
        related_name="voluntarios_interesados",
    )
    profesion = models.CharField(verbose_name="Profesión", max_length=100, blank=True)
    ciudad = models.CharField(verbose_name="Ciudad", max_length=100, blank=True)

    # Campos condicionales — donación
    tipo_donacion = models.CharField(
        verbose_name="Tipo de donación", max_length=20, choices=TipoDonacion.choices, blank=True
    )
    rango_aporte = models.CharField(
        verbose_name="Rango de aporte",
        max_length=100,
        blank=True,
        help_text="Texto libre, ej. 'S/ 50 - S/ 100 mensual'.",
    )
    desea_recibo = models.BooleanField(verbose_name="Desea recibo por donación", default=False)

    # Campos condicionales — empresa
    razon_social = models.CharField(verbose_name="Razón social", max_length=200, blank=True)
    ruc = models.CharField(
        verbose_name="RUC", max_length=11, validators=[RUC_VALIDATOR], blank=True
    )
    cargo = models.CharField(verbose_name="Cargo", max_length=100, blank=True)
    tipo_alianza = models.CharField(verbose_name="Tipo de alianza", max_length=150, blank=True)

    class Meta:
        verbose_name = "Contacto"
        verbose_name_plural = "Contactos"
        ordering = ["-creado"]

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.get_tipo_display()})"
