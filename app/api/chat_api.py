from fastapi import APIRouter

from app.telephony.voice_webhook import orchestrator 

router = APIRouter(tags=["Chat"])


@router.get("/chat")
def get_chat():

    messages = []

    # If ConversationMemory has messages
    if hasattr(orchestrator.memory, "history"):

        for msg in orchestrator.memory.history:

            role = msg.get("role", "").lower()

            if role in ["user", "human", "customer"]:
                role = "customer"
            elif role in ["assistant", "ai"]:
                role = "ai"

            messages.append({
                "role": role,
                "message": msg.get("content", "")
            })

    return messages