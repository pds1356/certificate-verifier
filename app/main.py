from fastapi import FastAPI
from app.database import engine, Base
from app import models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Certificate Verifier",
    description="Issue certificates and verify them publicly, with SHA-256 tamper detection.",
    version="0.1.0",
)

@app.get("/health", tags=["System"])
def health():
    return {"status": "ok"}
