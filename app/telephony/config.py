import os


class TelephonyConfig:

    # ---------------------------------------------------
    # Twilio Credentials
    # ---------------------------------------------------

    ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
    AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
    FROM_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "")

    # ---------------------------------------------------
    # Public Base URL
    # ---------------------------------------------------

    BASE_URL = os.getenv(
        "BASE_URL",
        "http://localhost:8000"
    )

    # ---------------------------------------------------
    # Voice Webhook
    # ---------------------------------------------------

    VOICE_WEBHOOK = f"{BASE_URL}/api/voice"

    # ---------------------------------------------------
    # Media Stream URL
    # ---------------------------------------------------

    MEDIA_STREAM = (
        BASE_URL
        .replace("https://", "wss://")
        .replace("http://", "ws://")
        + "/api/media"
    )