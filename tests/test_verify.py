from app.models import CertificateModel

def test_verify_valid_certificate_is_public(client, login_as):
    headers = login_as("issuer@example.com")
    issued = client.post(
        "/certificates",
        json={
            "holder_name": "Asha Verma",
            "course_name": "Backend Engineering",
            "issue_date": "2026-02-10",
        },
        headers=headers,
    )
    public_id = issued.json()["public_id"]

    response = client.get(f"/verify/{public_id}")
    assert response.status_code == 200
    body = response.json()
    assert body["result"] == "valid"
    assert body["holder_name"] == "Asha Verma"
    assert body["course_name"] == "Backend Engineering"
    assert body["issue_date"] == "2026-02-10"


def test_verify_unknown_id_returns_404(client):
    response = client.get("/verify/not-a-real-id")
    assert response.status_code == 404

def test_verify_detects_tampering(client, login_as, db_session):
    headers = login_as("issuer@example.com")
    issued = client.post(
        "/certificates",
        json={
            "holder_name": "Asha Verma",
            "course_name": "Backend Engineering",
            "issue_date": "2026-02-10",
        },
        headers=headers,
    )
    public_id = issued.json()["public_id"]

    row = db_session.query(CertificateModel).filter(
        CertificateModel.public_id == public_id
    ).first()
    row.holder_name = "Someone Else"
    db_session.commit()

    response = client.get(f"/verify/{public_id}")
    assert response.status_code == 200
    body = response.json()
    assert body["result"] == "tampered"
    assert body["holder_name"] is None
    assert body["course_name"] is None
    assert body["issue_date"] is None


def test_verify_shows_revoked(client, login_as):
    headers = login_as("issuer@example.com")
    issued = client.post(
        "/certificates",
        json={
            "holder_name": "Asha Verma",
            "course_name": "Backend Engineering",
            "issue_date": "2026-02-10",
        },
        headers=headers,
    )
    public_id = issued.json()["public_id"]

    revoked = client.patch(f"/certificates/{public_id}/revoke", headers=headers)
    assert revoked.status_code == 200

    response = client.get(f"/verify/{public_id}")
    body = response.json()
    assert body["result"] == "revoked"
    assert body["holder_name"] == "Asha Verma"
