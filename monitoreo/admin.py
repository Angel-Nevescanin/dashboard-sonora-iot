from django.contrib import admin
from .models import RegistroSensor

@admin.register(RegistroSensor)
class RegistroSensorAdmin(admin.ModelAdmin):
    list_display = ('municipio', 'tipo_dato', 'valor', 'fecha')
    list_filter = ('municipio', 'tipo_dato')
    search_fields = ('municipio',)
