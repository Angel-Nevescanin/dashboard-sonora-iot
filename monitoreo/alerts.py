from twilio.rest import Client
import os

# Credenciales desde variables de entorno
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
WHATSAPP_FROM = "whatsapp:+14155238886"  # Sandbox Twilio
WHATSAPP_TO = os.getenv("622236661")  # Tu número

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def enviar_alerta_whatsapp(municipio, uv):
    """
    Envía una alerta por WhatsApp cuando el índice UV es peligroso.
    """
    mensaje = (
        "🚨 ALERTA UV 🚨\n"
        f"Municipio: {municipio}\n"
        f"Índice UV: {uv}\n\n"
        "⚠ Riesgo solar alto. Evite exposición prolongada."
    )

    try:
        client.messages.create(
            body=mensaje,
            from_=WHATSAPP_FROM,
            to=WHATSAPP_TO
        )
        print("✅ Alerta WhatsApp enviada")
    except Exception as e:
        print("❌ Error enviando alerta WhatsApp:", e)
