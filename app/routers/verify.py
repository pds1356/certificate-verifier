from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.fingerprint import compute_fingerprint
from app.models import CertificateModel
from app.schemas import VerifyResponse

router = APIRouter(prefix="/verify", tags=["Verify"])

@router.get("/{public_id}", response_model=VerifyResponse)
def verify_certificate(public_id: str, db: Session = Depends(get_db)):
    certificate = (
        db.query(CertificateModel)
        .filter(CertificateModel.public_id == public_id)
        .first()
    )
    if certificate is None:
        raise HTTPException(status_code=404, detail="Certificate not found")

    recomputed = compute_fingerprint(
    certificate.public_id,
    certificate.holder_name,
    certificate.course_name,
    certificate.issue_date,
    )
    
    # For tampered certificate
    if recomputed != certificate.fingerprint:
        return VerifyResponse(
            result="tampered",
            message="This certificate's data does not match its original fingerprint.",
        )

    # For revoked certificate
    if certificate.status == "revoked":
        return VerifyResponse(
            result="revoked",
            message="This certificate was issued but has since been revoked by the issuer.",
            holder_name=certificate.holder_name,
            course_name=certificate.course_name,
            issue_date=certificate.issue_date,
        )

    return VerifyResponse(
        result="valid",
        message="This certificate is genuine and has not been altered.",
        holder_name=certificate.holder_name,
        course_name=certificate.course_name,
        issue_date=certificate.issue_date,
    )

