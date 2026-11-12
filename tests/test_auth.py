def test_register_returns_201_and_hides_password(client):
    response = client.post(
        "/register",
        json={"email": "a@example.com", "password": "secret123"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "a@example.com"
    assert "id" in body
    assert "password" not in body
    assert "hashed_password" not in body

def test_register_duplicate_email_returns_400(client):
    payload = {"email": "dup@example.com", "password": "secret123"}
    first = client.post("/register", json=payload)
    assert first.status_code == 201

    second = client.post("/register", json=payload)
    assert second.status_code == 400
    assert second.json()["detail"] == "Email already registered"

def test_login_returns_token(client):
    client.post("/register", json={"email": "u@example.com", "password": "secret123"})

    response = client.post(
        "/login",
        data={"username": "u@example.com", "password": "secret123"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


def test_login_wrong_password_returns_401(client):
    client.post("/register", json={"email": "u@example.com", "password": "secret123"})

    response = client.post(
        "/login",
        data={"username": "u@example.com", "password": "wrong-password"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"
