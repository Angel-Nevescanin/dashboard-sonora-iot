from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Max
from .models import RegistroSensor


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
