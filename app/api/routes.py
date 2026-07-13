from fastapi import APIRouter
from pydantic import BaseModel

from app.conversation.conversation_orchestrator import ConversationOrchestrator

router = APIRouter()
orchestrator = ConversationOrchestrator()


class MessageRequest(BaseModel):
    message: str


@router.post("/api/start")
def start_call():
    greeting = "Hello! Good morning."
    orchestrator.memory.add_ai_message(greeting)
    return {"reply": greeting}


@router.post("/api/message")
def message(req: MessageRequest):
    return orchestrator.process(req.message)
