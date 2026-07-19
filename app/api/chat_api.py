from fastapi import APIRouter

from app.telephony.voice_webhook import orchestrator

router = APIRouter(tags=["Chat"])


@router.get("/chat")
def get_chat():

    messages = []

    # If ConversationMemory has messages
    if hasattr(orchestrator.memory, "messages"):

        for msg in orchestrator.memory.history:

            role = msg.get("role", "")

            # Convert roles for UI
            if role == "user":
                role = "customer"

            elif role == "assistant":
                role = "ai"

            messages.append({
                "role": role,
                "message": msg.get("content", "")
            })

    return messages