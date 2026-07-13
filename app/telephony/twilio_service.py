from twilio.rest import Client

from app.telephony.models import CallRequest, CallResponse
from app.telephony.outbound_service import OutboundService
from app.telephony.telephony_config import TelephonyConfig


class TwilioService(OutboundService):

    def __init__(self):

        self.client = Client(
            TelephonyConfig.ACCOUNT_SID,
            TelephonyConfig.AUTH_TOKEN
        )

    def make_call(
        self,
        request: CallRequest
    ) -> CallResponse:

        try:

            call = self.client.calls.create(

                to=request.phone_number,

                from_=TelephonyConfig.FROM_NUMBER,

                url=f"{TelephonyConfig.BASE_URL}/telephony/voice"

            )

            return CallResponse(

                success=True,

                call_id=call.sid,

                message="Call initiated"

            )

        except Exception as ex:

            return CallResponse(

                success=False,

                message=str(ex)

            )