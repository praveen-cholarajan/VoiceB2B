from twilio.rest import Client

from app.telephony.config import TelephonyConfig


class TwilioClient:

    def __init__(self):

        self.client = Client(
            TelephonyConfig.ACCOUNT_SID,
            TelephonyConfig.AUTH_TOKEN
        )

    # ---------------------------------------------------------
    # Outbound Voice Call
    # ---------------------------------------------------------

    def make_call(self, to_number: str):

        try:

            print("\n========================================")
            print("VOICE CLIENT CALL STARTED")
            print("TO NUMBER :", to_number)
            print("FROM_NUMBER     :", TelephonyConfig.FROM_NUMBER)
            print("VOICE_WEBHOOK       :", TelephonyConfig.VOICE_WEBHOOK)
            print("========================================\n")

            call = self.client.calls.create(

                to=to_number,

                from_=TelephonyConfig.FROM_NUMBER,

                url=TelephonyConfig.VOICE_WEBHOOK,

                method="POST"

            )

            print("-----------------------------------------")
            print("Outbound Call Initiated")
            print("Call SID :", call.sid)
            print("-----------------------------------------")

            return {

                "success": True,

                "call_sid": call.sid,

                "status": call.status

            }

        except Exception as ex:

            print("Twilio Error :", ex)

            return {

                "success": False,

                "error": str(ex)

            }