from fastapi import FastAPI
from app.database import engine, Base
from app import models
from app.routers import auth, certificates, verify, pages

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Certificate Verifier",
    description="Issue certificates and verify them publicly, with SHA-256 tamper detection.",
    version="0.1.0",
)

#tells the app to include every route from [filename].py
app.include_router(auth.router)
app.include_router(certificates.router)
app.include_router(verify.router)
app.include_router(pages.router)

@app.get("/health", tags=["System"])
def health():
    return {"status": "ok"}



