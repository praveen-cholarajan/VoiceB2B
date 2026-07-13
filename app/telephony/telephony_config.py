import os


class TelephonyConfig:

    ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")

    AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

    FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER")

    BASE_URL = os.getenv("PUBLIC_BASE_URL")