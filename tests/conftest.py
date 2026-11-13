import os
import pytest

from fastapi.testclient import TestClient
from app.database import Base, get_db
from app.main import app
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker

load_dotenv()
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if not TEST_DATABASE_URL:
    raise RuntimeError("TEST_DATABASE_URL is not set in .env")

if not make_url(TEST_DATABASE_URL).database.endswith("_test"):
    raise RuntimeError("Refusing to run tests: the database name must end with _test")

test_engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=test_engine)

@pytest.fixture
def client():
    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def login_as(client):
    def _login(email: str) -> dict:
        client.post("/register", json={"email": email, "password": "secret123"})
        response = client.post("/login", data={"username": email, "password": "secret123"})
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    return _login

@pytest.fixture
def db_session(client):
    db = TestingSessionLocal()
    yield db
    db.close()
