import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.fingerprint import compute_fingerprint
from app.models import CertificateModel, UserModel
from app.schemas import CertificateCreate, CertificateResponse

router = APIRouter(prefix="/certificates", tags=["Certificates"])

@router.post("", response_model=CertificateResponse, status_code=201)
def issue_certificate(
    data: CertificateCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    public_id = str(uuid.uuid4())
    fingerprint = compute_fingerprint(
        public_id, data.holder_name, data.course_name, data.issue_date
    )
    certificate = CertificateModel(
        public_id=public_id,
        issuer_id=current_user.id,
        holder_name=data.holder_name,
        course_name=data.course_name,
        issue_date=data.issue_date,
        fingerprint=fingerprint,
        status="valid",
    )
    db.add(certificate)
    db.commit()
    db.refresh(certificate)
    return certificate
