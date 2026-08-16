import csv

from django.contrib import admin
from django.http import HttpResponse

from contacto.models import Contacto


@admin.action(description="Exportar seleccionados a CSV")
def exportar_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="contactos.csv"'
    writer = csv.writer(response)
    writer.writerow(
        [
            "tipo",
            "nombre",
            "apellido",
            "email",
            "telefono",
            "estado",
            "creado",
            "mensaje",
            "origen",
        ]
    )
    for contacto in queryset:
        writer.writerow(
            [
                contacto.get_tipo_display(),
                contacto.nombre,
                contacto.apellido,
                contacto.email,
                contacto.telefono,
                contacto.get_estado_display(),
                contacto.creado,
                contacto.mensaje,
                contacto.origen,
            ]
        )
    return response


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "apellido", "tipo", "email", "estado", "creado")
    list_filter = ("tipo", "estado", "creado")
    search_fields = ("nombre", "apellido", "email", "telefono")
    date_hierarchy = "creado"
    readonly_fields = ("creado", "ip", "origen")
    actions = [exportar_csv]

    fieldsets = (
        (
            "Datos generales",
            {"fields": ("tipo", "nombre", "apellido", "email", "telefono", "mensaje", "estado")},
        ),
        (
            "Voluntariado",
            {
                "fields": ("disponibilidad", "areas_interes", "profesion", "ciudad"),
                "classes": ("collapse",),
            },
        ),
        (
            "Donación",
            {
                "fields": ("tipo_donacion", "rango_aporte", "desea_recibo"),
                "classes": ("collapse",),
            },
        ),
        (
            "Empresa",
            {
                "fields": ("razon_social", "ruc", "cargo", "tipo_alianza"),
                "classes": ("collapse",),
            },
        ),
        ("Metadatos", {"fields": ("creado", "ip", "origen"), "classes": ("collapse",)}),
    )
