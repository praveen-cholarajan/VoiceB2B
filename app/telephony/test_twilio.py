import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../..")
    )
)

from app.telephony.twilio_client import TwilioClient
from app.telephony.config import TelephonyConfig

print("SID :", TelephonyConfig.ACCOUNT_SID)
print("FROM:", TelephonyConfig.FROM_NUMBER)
print("URL :", TelephonyConfig.VOICE_WEBHOOK)

client = TwilioClient()

result = client.make_call("+918760022251")

print(result)