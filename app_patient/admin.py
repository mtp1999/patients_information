from django.contrib import admin
from .models import Patient, Prescription, Visit, Phone

admin.site.register(Patient)
admin.site.register(Visit)
admin.site.register(Phone)
admin.site.register(Prescription)
