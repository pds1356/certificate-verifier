from datetime import date, datetime
from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str

    model_config = {"from_attributes": True}

class CertificateCreate(BaseModel):
    holder_name: str = Field(min_length=1, max_length=200)
    course_name: str = Field(min_length=1, max_length=200)
    issue_date: date

class CertificateResponse(BaseModel):
    public_id: str
    holder_name: str
    course_name: str
    issue_date: date
    status: str
    fingerprint: str
    created_at: datetime

    model_config = {"from_attributes": True}
