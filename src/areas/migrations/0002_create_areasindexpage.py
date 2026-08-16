from django.db import migrations


def create_areasindexpage(apps, schema_editor):
    from areas.models import AreasIndexPage
    from home.models import HomePage

    homepage = HomePage.objects.first()
    if homepage is None or AreasIndexPage.objects.exists():
        return

    page = AreasIndexPage(title="Áreas de trabajo", slug="areas-de-trabajo")
    homepage.add_child(instance=page)
    page.save_revision().publish()


def remove_areasindexpage(apps, schema_editor):
    AreasIndexPage = apps.get_model("areas.AreasIndexPage")
    AreasIndexPage.objects.filter(slug="areas-de-trabajo").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("areas", "0001_initial"),
        ("home", "0003_fase1_contenido"),
    ]

    operations = [
        migrations.RunPython(create_areasindexpage, remove_areasindexpage),
    ]
