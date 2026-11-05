from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.fingerprint import compute_fingerprint
from app.models import CertificateModel
from app.schemas import VerifyResponse

router = APIRouter(prefix="/verify", tags=["Verify"])
