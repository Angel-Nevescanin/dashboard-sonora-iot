# dashboard_sonora/mqtt_client.py
"""
Cliente MQTT para el proyecto Dashboard Sonora.
Ejecuta:
    (venv) python dashboard_sonora/mqtt_client.py

Funciones:
- Se suscribe a 'sonora/#'
- Parsea topics: sonora/<municipio>/<tipo>
- Actualiza latest_data (cache en memoria)
- Inserta registros en la BD (monitoreo.models.RegistroSensor)
"""

import os
import re
import sys
import time
import json
import logging
from threading import Event

# --- Configuración Django (permite usar los modelos desde script externo) ---
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard_sonora.settings')

import django
django.setup()

from django.utils import timezone
from monitoreo.models import RegistroSensor

# --- MQTT (paho) ---
import paho.mqtt.client as mqtt

# --- Logging ---
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')
logger = logging.getLogger('mqtt-client')

# --- Parámetros configurables ---
BROKER = "broker.emqx.io"     # broker público; el profesor puede usar otro
PORT = 1883
KEEPALIVE = 60
TOPIC = "sonora/#"            # wildcard pedido por el proyecto

# --- Cache en memoria con los últimos valores ---
# Estructura: { "hermosillo": {"temperatura": 29.4, "humedad": 45.0, "timestamp": "2025-11-30T17:..."}, ...}
latest_data = {}

# Evento para controlar el loop
_stop_event = Event()

# --- Funciones auxiliares ---
def parse_topic(topic: str):
    """
    Espera: 'sonora/<municipio>/<tipo>'
    Retorna (municipio, tipo) o (None, None) si no cuadra.
    """
    parts = topic.split('/')
    if len(parts) >= 3 and parts[0].lower() == 'sonora':
        municipio = parts[1].lower()
        tipo = parts[2].lower()
        return municipio, tipo
    return None, None

def save_reading(municipio: str, tipo: str, valor: float):
    """
    Guarda en la base de datos usando el modelo RegistroSensor
    """
    try:
        # Ajusta municipio/tipo si quieres mapear a choices
        RegistroSensor.objects.create(
            municipio=municipio[:50],
            tipo_dato=tipo[:50],
            valor=valor
        )
        logger.debug(f"Guardado en DB: {municipio} {tipo}={valor}")
    except Exception as e:
        logger.exception("Error guardando lectura en DB: %s", e)

def update_cache(municipio: str, tipo: str, valor: float):
    ts = timezone.now().isoformat()
    entry = latest_data.get(municipio, {})
    entry[tipo] = valor
    entry['timestamp'] = ts
    latest_data[municipio] = entry

# --- Callbacks MQTT ---
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Conectado al broker MQTT")
        client.subscribe(TOPIC)
        logger.info("Suscrito a: %s", TOPIC)
    else:
        logger.error("Error de conexión MQTT, rc=%s", rc)

def on_message(client, userdata, msg):
    topic = msg.topic
    payload_bytes = msg.payload
    try:
        payload = payload_bytes.decode('utf-8').strip()
    except Exception:
        payload = None

    municipio, tipo = parse_topic(topic)
    if municipio is None or tipo is None:
        logger.warning("Topic no reconocido: %s", topic)
        return
    
    TIPO_MAP={
        "temperatura": "temperatura",
        "temp": "temperatura",
        "humedad": "humedad",
        "hum": "humedad",
        "uv": "uv",
        "uv_index": "uv",
        "indice_uv": "uv"

    }
    tipo = TIPO_MAP.get(tipo, tipo)


    valor = None
    # Intentar parsear payload: puede ser un número, o JSON con {'value':...}
    if payload is None or payload == '':
        logger.warning("Payload vacío para %s", topic)
        return

    # 1) JSON payload?
    try:
        data = json.loads(payload)
        # buscar valor en keys comunes
        for k in ('value', 'valor', 'v', 'reading'):
            if k in data:
                valor = float(data[k])
                break
        # si payload es { "temperatura": 29.3 }
        if valor is None and tipo in data:
            valor = float(data[tipo])
    except (json.JSONDecodeError, TypeError, ValueError):


        # no es JSON -> intentar extraer número aunque tenga texto
        try:
            match = re.search(r"[-+]?\d*\.?\d+", payload)
            if match:
                valor = float(match.group())
            else:
                raise ValueError("No numeric value found")
        except Exception:
            logger.warning("No se pudo parsear payload: %r (topic=%s)", payload, topic)


    if valor is None:
        logger.warning("Lectura ignorada (sin valor) topic=%s payload=%r", topic, payload)
        return

    # Actualizar cache y guardar en BD
    try:
        update_cache(municipio, tipo, valor)
        save_reading(municipio, tipo, valor)
        logger.info("Lectura recibida: %s | %s = %s", municipio, tipo, valor)
    except Exception as e:
        logger.exception("Error procesando mensaje: %s", e)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        logger.warning("Desconexión inesperada (rc=%s). Reconectando...", rc)
    else:
        logger.info("Desconectado del broker MQTT (rc=0)")

# --- Cliente y loop principal ---
def run(broker=BROKER, port=PORT):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    # Opcional: si el broker requiere usuario/clave
    # client.username_pw_set(username="user", password="pass")

    # Reintentos básicos de conexión
    while not _stop_event.is_set():
        try:
            logger.info("Intentando conectar a %s:%s ...", broker, port)
            client.connect(broker, port, KEEPALIVE)
            client.loop_start()
            # Espera hasta que se pida detener
            while not _stop_event.is_set():
                time.sleep(0.5)
            break
        except Exception as e:
            logger.exception("No se pudo conectar al broker MQTT: %s. Reintentando en 5s...", e)
            try:
                client.loop_stop()
            except Exception:
                pass
            time.sleep(5)

    # Limpieza
    try:
        client.loop_stop()
        client.disconnect()
    except Exception:
        pass
    logger.info("Cliente MQTT detenido.")

def stop():
    _stop_event.set()

# Permite exponer la cache si otro módulo la importa:
def get_latest_data():
    return latest_data

# Cuando se ejecute como script, iniciamos el loop
if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt recibido. Deteniendo...")
        stop()
