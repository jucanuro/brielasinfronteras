from wagtail.models import Page


class HomePage(Page):
    """Pagina de inicio. Los campos reales (video de hero, cifras de
    impacto, orden de secciones) se agregan en la Fase 1."""

    class Meta:
        verbose_name = "Página de inicio"
