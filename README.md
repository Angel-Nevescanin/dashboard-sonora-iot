#  Dashboard IoT – Monitoreo Climático Sonora (Django + MQTT)

Proyecto final del curso **Internet de las Cosas**.  
Este sistema permite el monitoreo en tiempo real de variables climáticas
(publicadas vía MQTT) para distintos municipios del estado de Sonora.

---

##  Objetivo del Proyecto

Desarrollar un **dashboard web** que:
- Se suscriba a un broker **MQTT**
- Procese datos en tiempo real
- Almacene la información temporalmente en **cache**
- Visualice gráficas dinámicas y alertas
- Permita exportar datos históricos

---

##  Arquitectura General
Sensores / Simuladores
↓
MQTT Broker
↓
Cliente MQTT (Python)
↓
Django Cache
↓
API REST (Django)
↓
Dashboard Web (HTML + JS)



---

## ⚙️ Tecnologías Utilizadas

- Python 3
- Django 4.2
- MQTT (paho-mqtt)
- Chart.js
- HTML / CSS / JavaScript
- Cache de Django
- (Opcional) WhatsApp API (Twilio)

---

## 📡 Funcionalidad MQTT

- Suscripción al tópico: `sonora/#`
- Manejo de múltiples municipios
- Reconexión automática ante fallos
- Procesamiento de:
  - Temperatura 🌡️
  - Humedad 💧
  - Índice UV ☀️

---

## 📊 Dashboard

- Gráficas en tiempo real
- Diferentes colores por variable
- Alerta visual cuando:
  - **UV ≥ 8 → barra roja**
- Texto explicativo integrado

📌 *“El sistema muestra datos en tiempo real obtenidos vía MQTT y almacenados en Django.”*

---

## 🚨 Sistema de Alertas

- Alertas visuales en el dashboard
- Notificaciones automáticas vía **WhatsApp** cuando:
  - UV ≥ 8
  - Temperatura elevada
  - Humedad extrema

---

## 📤 Exportación de Datos

- CSV
- PDF
- Datos históricos por municipio

---

## ▶️ Ejecución del Proyecto

### 1. Crear entorno virtual
```bash
python -m venv venv

2. Activar entorno
venv\Scripts\activate

3. Instalar dependencias
pip install -r requirements.txt

4. Ejecutar servidor
python manage.py runserver


📁 Estructura del Proyecto
dashboard_sonora/
├── dashboard/
│   ├── settings.py
│   ├── mqtt_client.py
├── monitoreo/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── templates/
│   └── static/
└── manage.py


Angel Stipe Nevescanin Moreno

Proyecto académico – Curso de Internet de las Cosas

Instituto Tecnologico de Sonora

