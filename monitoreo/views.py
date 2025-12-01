from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Max
from .models import RegistroSensor
import csv
from django.http import HttpResponse, JsonResponse


def exportar_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="datos_sensores.csv"'

    writer = csv.writer(response)
    writer.writerow(['Municipio', 'Tipo', 'Valor', 'Fecha'])

    for r in RegistroSensor.objects.all().order_by('-fecha'):
        writer.writerow([r.municipio, r.tipo_dato, r.valor, r.fecha])

    return response


def dashboard(request):
    return render(request, "monitoreo/dashboard.html")


def api_datos(request):
    """
    Devuelve los últimos valores por municipio y tipo de dato
    """
    datos = {}

    registros = (
        RegistroSensor.objects
        .order_by("municipio", "tipo_dato", "-fecha")
    )

    for r in registros:
        if r.municipio not in datos:
            datos[r.municipio] = {}

        # solo el último valor de cada tipo
        if r.tipo_dato not in datos[r.municipio]:
            datos[r.municipio][r.tipo_dato] = r.valor

    return JsonResponse(datos)
