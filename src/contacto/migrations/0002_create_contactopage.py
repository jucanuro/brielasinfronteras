from django.db import migrations


def create_contactopage(apps, schema_editor):
    from contacto.models import ContactoPage
    from home.models import HomePage

    homepage = HomePage.objects.first()
    if homepage is None or ContactoPage.objects.exists():
        return

    page = ContactoPage(title="Contacto", slug="contacto")
    homepage.add_child(instance=page)
    page.save_revision().publish()


def remove_contactopage(apps, schema_editor):
    ContactoPage = apps.get_model("contacto.ContactoPage")
    ContactoPage.objects.filter(slug="contacto").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("contacto", "0001_initial"),
        ("home", "0003_fase1_contenido"),
    ]

    operations = [
        migrations.RunPython(create_contactopage, remove_contactopage),
    ]
