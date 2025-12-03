from django.urls import path
from . import views

app_name = 'monitoreo'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    #path('municipios/', views.municipios, name='municipios'),
    path('api/datos/', views.api_datos, name='api_datos'),
    path("api/export/csv/", views.export_csv, name="export_csv"),
    path("api/export/pdf/", views.export_pdf, name="export_pdf"),

]
