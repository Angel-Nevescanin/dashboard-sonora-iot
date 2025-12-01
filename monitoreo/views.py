from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
# Create your views here.
# monitoreo/views.py

# Simulación temporal de datos para que puedas probar el frontend
# Más adelante reemplazaremos esto por la cache que llena mqtt_client.py
def sample_data():
    now = timezone.now().isoformat()
    return {
        "timestamp": now,
        "municipios": [
            {"name": "Hermosillo", "temperatura": 29.4, "humedad": 45.0},
            {"name": "Guaymas", "temperatura": 31.1, "humedad": 40.2},
            {"name": "Nogales", "temperatura": 26.7, "humedad": 55.6},
        ]
    }

def dashboard(request):
    # renderiza el template principal del dashboard
    return render(request, 'monitoreo/dashboard.html')

def municipios(request):
    # renderiza la vista por municipios
    return render(request, 'monitoreo/municipios.html')

def api_datos(request):
    # Endpoint JSON que el frontend consultará cada 3s.
    # En producción esto devolverá datos reales (cache/DB alimentada por MQTT).
    data = sample_data()
    return JsonResponse(data)
