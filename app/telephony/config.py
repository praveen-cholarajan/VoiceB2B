import os
from dotenv import load_dotenv

load_dotenv()


class TelephonyConfig:

    # ---------------------------------------------------
    # Twilio Credentials
    # ---------------------------------------------------

    ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
    AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
    FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER", "")

    # ---------------------------------------------------
    # Public Base URL
    # ---------------------------------------------------

    BASE_URL = os.getenv(
        "PUBLIC_BASE_URL",
        "http://localhost:8000"
    )

    # ---------------------------------------------------
    # Voice Webhook
    # ---------------------------------------------------

    VOICE_WEBHOOK = f"{BASE_URL}/api/voice"

    print("\n========================================")
    print("TelephonyConfig ENV STARTED")
    print("ACCOUNT_SID :", ACCOUNT_SID)
    print("FROM_NUMBER     :", FROM_NUMBER)
    print("BASE_URL       :", BASE_URL)
    print("VOICE_WEBHOOK       :", VOICE_WEBHOOK)
    print("========================================\n")
    # ---------------------------------------------------
    # Media Stream URL
    # ---------------------------------------------------

    MEDIA_STREAM = (
        BASE_URL
        .replace("https://", "wss://")
        .replace("http://", "ws://")
        + "/api/media"
    )