from django.db import models
from wagtail.admin.panels import FieldPanel


class RolTestimonio(models.TextChoices):
    VOLUNTARIO = "voluntario", "Voluntario/a"
    BENEFICIARIO = "beneficiario", "Beneficiario/a"
    ALIADO = "aliado", "Aliado/a"


class Testimonio(models.Model):
    nombre = models.CharField(verbose_name="Nombre", max_length=150)
    rol = models.CharField(verbose_name="Rol", max_length=20, choices=RolTestimonio.choices)
    foto = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name="Foto",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    texto = models.TextField(verbose_name="Testimonio")
    proyecto = models.ForeignKey(
        "proyectos.ProyectoPage",
        verbose_name="Proyecto relacionado",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="testimonios",
    )
    orden = models.PositiveIntegerField(verbose_name="Orden", default=0)
    activo = models.BooleanField(
        verbose_name="Activo",
        default=True,
        help_text="Desactívalo para ocultarlo del sitio sin borrarlo.",
    )

    panels = [
        FieldPanel("nombre"),
        FieldPanel("rol"),
        FieldPanel("foto"),
        FieldPanel("texto"),
        FieldPanel("proyecto"),
        FieldPanel("orden"),
        FieldPanel("activo"),
    ]

    class Meta:
        verbose_name = "Testimonio"
        verbose_name_plural = "Testimonios"
        ordering = ["orden"]

    def __str__(self):
        return self.nombre
