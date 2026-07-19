from fastapi import APIRouter, Request
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse, Gather

from app.conversation.conversation_orchestrator import ConversationOrchestrator

router = APIRouter(tags=["Telephony"])

# ---------------------------------------------------------
# Single Conversation Engine
# ---------------------------------------------------------

orchestrator = ConversationOrchestrator()

from pathlib import Path
from datetime import datetime

LOG_FILE = Path("logs/conversation.log")
LOG_FILE.parent.mkdir(exist_ok=True)


def write_log(call_sid, customer_message, ai_reply, confidence=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write("=" * 80 + "\n")
        f.write(f"Time       : {timestamp}\n")
        f.write(f"Call SID   : {call_sid}\n")
        f.write(f"Confidence : {confidence}\n")
        f.write(f"Customer   : {customer_message}\n")
        f.write(f"AI         : {ai_reply}\n")
        f.write("=" * 80 + "\n\n")

# =========================================================
# Helper
# =========================================================

async def get_request_data(request: Request):
    """
    Supports both:
    1. Twilio (form-urlencoded)
    2. Postman (application/json)
    """

    content_type = request.headers.get("content-type", "")

    if "application/json" in content_type:
        return await request.json()

    return await request.form()


# =========================================================
# START VOICE CALL
# =========================================================

@router.post("/voice")
async def voice_webhook(request: Request):

    data = await get_request_data(request)

    print("\n========================================")
    print("VOICE CALL STARTED")
    print("Call SID :", data.get("CallSid"))
    print("From     :", data.get("From"))
    print("To       :", data.get("To"))
    print("========================================\n")

    try:
        ai_reply = orchestrator.start()

    except Exception as ex:

        print("Start Error :", ex)

        ai_reply = (
            "Sorry, we are unable to process your request at the moment."
        )

    response = VoiceResponse()

    gather = Gather(
        input="speech",
        action="/api/voice/process",
        method="POST",
        speech_timeout="auto",
        language="en-IN"
    )

    gather.say(
        ai_reply,
        voice="alice",
        language="en-IN"
    )

    response.append(gather)

    return Response(
        content=str(response),
        media_type="application/xml"
    )


# =========================================================
# PROCESS CUSTOMER SPEECH
# =========================================================

@router.post("/voice/process")
async def process_voice(request: Request):

    data = await get_request_data(request)

    call_sid = data.get("CallSid")

    customer_message = (
        data.get("SpeechResult") or ""
    ).strip()

    confidence = data.get("Confidence")

    print("\n========================================")
    print("VOICE INPUT")
    print("Call SID   :", call_sid)
    print("Customer   :", customer_message)
    print("Confidence :", confidence)
    print("========================================\n")

    if not customer_message:

        ai_reply = (
            "Sorry, I couldn't hear you clearly. "
            "Could you please repeat that?"
        )

    else:

        try:

            ai_response = orchestrator.process(
                customer_message
            )
            print("AI Response:", ai_response)
            ai_reply = ai_response.get("reply", "")

        except Exception as ex:

            print("Conversation Error :", ex)

            ai_reply = (
                "Sorry, something went wrong. "
                "Could you please repeat that?"
            )

    print("AI Replay:", ai_reply)

    write_log(
    call_sid=call_sid,
    customer_message=customer_message,
    ai_reply=ai_reply,
    confidence=confidence)

    response = VoiceResponse()

    # -----------------------------------------------------
    # Conversation Completed
    # -----------------------------------------------------

    if orchestrator.memory.current_state == "END":

        response.say(
            ai_reply,
            voice="alice",
            language="en-IN"
        )

        response.hangup()

        return Response(
            content=str(response),
            media_type="application/xml"
        )

    # -----------------------------------------------------
    # Continue Conversation
    # -----------------------------------------------------

    gather = Gather(
        input="speech",
        action="/api/voice/process",
        method="POST",
        speech_timeout="auto",
        language="en-IN"
    )

    gather.say(
        ai_reply,
        voice="alice",
        language="en-IN"
    )

    response.append(gather)

    return Response(
        content=str(response),
        media_type="application/xml"
    )