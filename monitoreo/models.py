from django.db import models

class RegistroSensor(models.Model):
    MUNICIPIOS = [
        ('hermosillo', 'Hermosillo'),
        ('guaymas', 'Guaymas'),
        ('nogales', 'Nogales'),
        ('obregon', 'Ciudad Obregón'),
    ]

    TIPOS_DATOS = [
        ('temperatura', 'Temperatura'),
        ('humedad', 'Humedad'),
        ('iluminacion', 'Iluminación'),
    ]

    municipio = models.CharField(
        max_length=50,
        choices=MUNICIPIOS
    )

    tipo_dato = models.CharField(
        max_length=50,
        choices=TIPOS_DATOS
    )

    valor = models.FloatField()

    fecha = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.municipio} - {self.tipo_dato}: {self.valor}"
