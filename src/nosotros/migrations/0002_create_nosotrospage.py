from django.db import migrations


def create_nosotrospage(apps, schema_editor):
    from home.models import HomePage
    from nosotros.models import NosotrosPage

    homepage = HomePage.objects.first()
    if homepage is None or NosotrosPage.objects.exists():
        return

    page = NosotrosPage(
        title="Nosotros",
        slug="nosotros",
        mision="<p>Pendiente de completar.</p>",
        vision="<p>Pendiente de completar.</p>",
    )
    homepage.add_child(instance=page)
    page.save_revision().publish()


def remove_nosotrospage(apps, schema_editor):
    NosotrosPage = apps.get_model("nosotros.NosotrosPage")
    NosotrosPage.objects.filter(slug="nosotros").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("nosotros", "0001_initial"),
        ("home", "0003_fase1_contenido"),
    ]

    operations = [
        migrations.RunPython(create_nosotrospage, remove_nosotrospage),
    ]
