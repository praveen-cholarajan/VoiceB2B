from fastapi import APIRouter
from pydantic import BaseModel

from app.telephony.twilio_client import TwilioClient

router = APIRouter(tags=["Call"])


# ---------------------------------------------------------
# Request Model
# ---------------------------------------------------------

class CallRequest(BaseModel):
    to_number: str


# ---------------------------------------------------------
# Start Outbound Call
# ---------------------------------------------------------

@router.post("/call")
def start_call(req: CallRequest):

    client = TwilioClient()

    result = client.make_call(req.to_number)

    return result