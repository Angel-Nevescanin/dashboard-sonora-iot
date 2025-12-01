from django.urls import path
from . import views

app_name = 'monitoreo'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('municipios/', views.municipios, name='municipios'),
    path('api/datos/', views.api_datos, name='api_datos'),
]
