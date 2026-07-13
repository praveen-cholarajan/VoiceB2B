from fastapi import FastAPI
from app.api.routes import router as conversation_router

app = FastAPI(
    title="Conversation API",
    version="1.0.0"
)

app.include_router(conversation_router)

@app.get("/")
def root():
    return {
        "status": "Running",
        "message": "Welcome to Conversation API"
    }