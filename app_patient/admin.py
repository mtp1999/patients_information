from django.contrib import admin
from .models import Patient, Prescription, Visit, Phone

admin.site.register(Patient)
admin.site.register(Phone)


class CustomVisitAdmin(admin.ModelAdmin):
    model = Visit
    list_display = (
        "pk",
        "patient",
        "datetime"
    )
    ordering = ("pk",)


class CustomPrescriptionAdmin(admin.ModelAdmin):
    model = Prescription
    list_display = (
        "pk",
        "patient",
        "datetime"
    )
    ordering = ("pk",)


admin.site.register(Visit, CustomVisitAdmin)
admin.site.register(Prescription, CustomPrescriptionAdmin)
