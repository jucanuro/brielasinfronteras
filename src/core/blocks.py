"""Bloques de StreamField reutilizables entre apps (por ahora, proyectos)."""

from wagtail.blocks import CharBlock, ListBlock, RichTextBlock, StructBlock, TextBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock


class ParrafoBlock(RichTextBlock):
    class Meta:
        icon = "pilcrow"
        label = "Párrafo"
        features = ["bold", "italic", "link", "ol", "ul", "h3", "h4"]


class ImagenBlock(StructBlock):
    imagen = ImageChooserBlock(label="Imagen")
    leyenda = CharBlock(label="Leyenda", required=False)

    class Meta:
        icon = "image"
        label = "Imagen"


class CitaBlock(StructBlock):
    texto = TextBlock(label="Cita")
    autor = CharBlock(label="Autor", required=False)
    rol = CharBlock(
        label="Rol o relación",
        required=False,
        help_text="Ej. 'Voluntaria, Proyecto Aulas Abiertas'.",
    )

    class Meta:
        icon = "openquote"
        label = "Cita"


class GaleriaBlock(StructBlock):
    imagenes = ListBlock(ImageChooserBlock(label="Imagen"), label="Imágenes")

    class Meta:
        icon = "image"
        label = "Galería"


class VideoBlock(EmbedBlock):
    class Meta:
        icon = "media"
        label = "Video (YouTube, Vimeo, etc.)"


class DatoIndividualBlock(StructBlock):
    numero = CharBlock(label="Número", help_text="Ej. '120', '+300', '85%'.")
    etiqueta = CharBlock(label="Etiqueta")

    class Meta:
        icon = "table"
        label = "Dato"


class DatosBlock(StructBlock):
    titulo = CharBlock(label="Título", required=False)
    datos = ListBlock(DatoIndividualBlock(), label="Datos")

    class Meta:
        icon = "table"
        label = "Bloque de datos"
