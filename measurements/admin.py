from django.contrib import admin

from .models import MeasurementSession, MeasurementResponse

# Register your models here.

admin.site.register(MeasurementSession)
admin.site.register(MeasurementResponse)
