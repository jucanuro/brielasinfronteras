"""Bloques del StreamField "secciones" de HomePage.

Cada bloque solo controla si una sección aparece y en qué orden, con un
título opcional de reemplazo. El contenido real de cada sección (áreas,
proyectos, testimonios) se lee de la base de datos en la plantilla — no se
duplica aquí.
"""

from wagtail.blocks import CharBlock, IntegerBlock, StructBlock


class TituloOpcionalBlock(StructBlock):
    titulo = CharBlock(
        label="Título de la sección",
        required=False,
        help_text="Déjalo vacío para usar el título por defecto.",
    )


class SeccionCifrasBlock(TituloOpcionalBlock):
    class Meta:
        icon = "table"
        label = "Cifras de impacto"


class SeccionConoceNosBlock(TituloOpcionalBlock):
    class Meta:
        icon = "help"
        label = "Conócenos"


class SeccionAreasBlock(TituloOpcionalBlock):
    class Meta:
        icon = "grip"
        label = "Áreas de trabajo"


class SeccionProyectosBlock(TituloOpcionalBlock):
    cantidad = IntegerBlock(
        label="Cantidad de proyectos a mostrar", default=3, min_value=1, max_value=12
    )

    class Meta:
        icon = "folder-open-inverse"
        label = "Proyectos destacados"


class SeccionTestimoniosBlock(TituloOpcionalBlock):
    cantidad = IntegerBlock(
        label="Cantidad de testimonios a mostrar", default=3, min_value=1, max_value=12
    )

    class Meta:
        icon = "openquote"
        label = "Testimonios"


class SeccionAyudaBlock(TituloOpcionalBlock):
    class Meta:
        icon = "heart"
        label = "Cómo quieres ayudar hoy"


SECCIONES_HOME_BLOCKS = [
    ("cifras_impacto", SeccionCifrasBlock()),
    ("conocenos", SeccionConoceNosBlock()),
    ("areas_de_trabajo", SeccionAreasBlock()),
    ("proyectos", SeccionProyectosBlock()),
    ("testimonios", SeccionTestimoniosBlock()),
    ("como_ayudar", SeccionAyudaBlock()),
]
