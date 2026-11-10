from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter(tags=["Pages"])

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"

@router.get("/v/{public_id}", include_in_schema=False)
def verify_page(public_id: str):
    return FileResponse(STATIC_DIR / "verify.html")
