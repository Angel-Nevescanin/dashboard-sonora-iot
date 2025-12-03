from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Max
from .models import RegistroSensor
import csv
from django.http import HttpResponse, JsonResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas



def export_csv(request):
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="datos_sonora_iot.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(["Municipio", "Tipo", "Valor", "Fecha"])

    registros = RegistroSensor.objects.all().order_by("-fecha")

    for r in registros:
        writer.writerow([
            r.municipio,
            r.tipo_dato,
            r.valor,
            r.fecha.strftime("%Y-%m-%d %H:%M:%S")
        ])

    return response

def export_pdf(request):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="reporte_sonora_iot.pdf"'

    pdf = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(40, height - 50, "Reporte Dashboard Sonora IoT")

    pdf.setFont("Helvetica", 10)
    y = height - 90

    registros = RegistroSensor.objects.all().order_by("-fecha")[:50]

    pdf.drawString(40, y, "Municipio | Tipo | Valor | Fecha")
    y -= 20

    for r in registros:
        texto = f"{r.municipio} | {r.tipo_dato} | {r.valor} | {r.fecha.strftime('%Y-%m-%d %H:%M')}"
        pdf.drawString(40, y, texto)
        y -= 15

        if y < 60:
            pdf.showPage()
            pdf.setFont("Helvetica", 10)
            y = height - 60

    pdf.save()
    return response



def dashboard(request):
    return render(request, "monitoreo/dashboard.html")


def api_datos(request):
    """
    API REST:
    Devuelve los últimos valores por municipio y tipo de dato
    Usada por el dashboard (Chart.js)
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
