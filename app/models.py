import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from app.database import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

class CertificateModel(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    public_id = Column(String(36), unique=True, index=True, nullable=False,
                       default=lambda: str(uuid.uuid4()))
    issuer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    holder_name = Column(String(200), nullable=False)
    course_name = Column(String(200), nullable=False)
    issue_date = Column(Date, nullable=False)
    fingerprint = Column(String(64), nullable=False)
    status = Column(String(20), nullable=False, default="valid")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
