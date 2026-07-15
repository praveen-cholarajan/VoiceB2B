from fastapi import APIRouter, Request
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse, Gather

from app.conversation.conversation_orchestrator import ConversationOrchestrator

router = APIRouter(tags=["Telephony"])

# ---------------------------------------------------------
# Single Conversation Engine
# ---------------------------------------------------------

orchestrator = ConversationOrchestrator()


# =========================================================
# START VOICE CALL
# =========================================================

@router.post("/voice")
async def voice_webhook(request: Request):
    """
    Twilio invokes this endpoint when the customer
    answers the outbound call.
    """

    form = await request.form()

    print("\n========================================")
    print("VOICE CALL STARTED")
    print("Call SID :", form.get("CallSid"))
    print("From     :", form.get("From"))
    print("To       :", form.get("To"))
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
    """
    Twilio sends every customer speech response here.
    """

    form = await request.form()

    call_sid = form.get("CallSid")

    customer_message = (
        form.get("SpeechResult") or ""
    ).strip()

    confidence = form.get("Confidence")

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

            ai_reply = orchestrator.process(
                customer_message
            )

        except Exception as ex:

            print("Conversation Error :", ex)

            ai_reply = (
                "Sorry, something went wrong. "
                "Could you please repeat that?"
            )

    print("AI :", ai_reply)

    response = VoiceResponse()

    # -----------------------------------------------------
    # End conversation if state reached END
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
    # Continue conversation
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