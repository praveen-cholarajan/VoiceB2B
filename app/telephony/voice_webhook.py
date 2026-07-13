from fastapi import APIRouter
from fastapi.responses import Response

router = APIRouter()


@router.post("/voice")
def voice():

    xml = """
<Response>
    <Say>Welcome.</Say>
</Response>
"""

    return Response(
        content=xml,
        media_type="application/xml"
    )