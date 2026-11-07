import uuid

from fastapi import APIRouter, Depends, HTTPException
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

@router.get("", response_model=list[CertificateResponse])
def list_my_certificates(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return (
        db.query(CertificateModel)
        .filter(CertificateModel.issuer_id == current_user.id)
        .order_by(CertificateModel.created_at.desc())
        .all()
    )

# Revoke Certificate
@router.patch("/{public_id}/revoke", response_model=CertificateResponse)
def revoke_certificate(
    public_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    certificate = (
        db.query(CertificateModel)
        .filter(
            CertificateModel.public_id == public_id,
            CertificateModel.issuer_id == current_user.id,
        )
        .first()
    )
    if certificate is None:
        raise HTTPException(status_code=404, detail="Certificate not found")

    certificate.status = "revoked"
    db.commit()
    db.refresh(certificate)
    return certificate
