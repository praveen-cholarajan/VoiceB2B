# from fastapi import FastAPI
# from app.api.routes import router as conversation_router
# from app.telephony.voice_webhook import router as voice_router
# from app.api.call_api import router as call_router

# streamlit_process = None

# import subprocess
# import sys
# from fastapi.responses import RedirectResponse
# from app.telephony.config import TelephonyConfig


# app = FastAPI(
#     title="Conversation API",
#     version="1.0.0"
# )

# app.include_router(conversation_router)


# app.include_router(
#     voice_router,
#     prefix="/api"
# )

# app.include_router(
#     call_router,
#     prefix="/api"
# )

# @app.get("/")
# def root():
#     return {
#         "status": "Running",
#         "message": "Welcome to Conversation API"
#     }


from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.api.routes import router as conversation_router
from app.telephony.voice_webhook import router as voice_router
from app.api.call_api import router as call_router
from app.api.chat_api import router as chat_router

app = FastAPI(
    title="Conversation API",
    version="1.0.0"
)

# ---------------------------------------------------------
# Static Files
# ---------------------------------------------------------

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

# ---------------------------------------------------------
# HTML Templates
# ---------------------------------------------------------

templates = Jinja2Templates(directory="app/templates")

# ---------------------------------------------------------
# Routers
# ---------------------------------------------------------

app.include_router(conversation_router)

app.include_router(
    voice_router,
    prefix="/api"
)

app.include_router(
    call_router,
    prefix="/api"
)

app.include_router(
    chat_router,
    prefix="/api"
)

# ---------------------------------------------------------
# Home Page
# ---------------------------------------------------------

@app.get("/")
async def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    ) 