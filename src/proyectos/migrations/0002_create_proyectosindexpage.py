from django.db import migrations


def create_proyectosindexpage(apps, schema_editor):
    from home.models import HomePage
    from proyectos.models import ProyectosIndexPage

    homepage = HomePage.objects.first()
    if homepage is None or ProyectosIndexPage.objects.exists():
        return

    page = ProyectosIndexPage(title="Proyectos", slug="proyectos")
    homepage.add_child(instance=page)
    page.save_revision().publish()


def remove_proyectosindexpage(apps, schema_editor):
    ProyectosIndexPage = apps.get_model("proyectos.ProyectosIndexPage")
    ProyectosIndexPage.objects.filter(slug="proyectos").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("proyectos", "0001_initial"),
        ("home", "0003_fase1_contenido"),
    ]

    operations = [
        migrations.RunPython(create_proyectosindexpage, remove_proyectosindexpage),
    ]
