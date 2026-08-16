from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from testimonios.models import Testimonio


class TestimonioViewSet(SnippetViewSet):
    model = Testimonio
    icon = "openquote"
    menu_label = "Testimonios"
    list_display = ("nombre", "rol", "proyecto", "activo", "orden")
    list_filter = ("rol", "activo")
    search_fields = ("nombre", "texto")
    ordering = ["orden"]


register_snippet(TestimonioViewSet)
