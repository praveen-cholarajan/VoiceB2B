import os
from dotenv import load_dotenv

load_dotenv()


class TelephonyConfig:
    # Twilio Credentials
    ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    FROM_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

    # Public Base URL (Render)
    BASE_URL = os.getenv("BASE_URL")

    # Voice Webhook
    VOICE_WEBHOOK = f"{BASE_URL}/api/voice"

    # Media Stream WebSocket (Sprint 2)
    MEDIA_STREAM = (
        BASE_URL.replace("https://", "wss://")
        + "/api/media"
    )