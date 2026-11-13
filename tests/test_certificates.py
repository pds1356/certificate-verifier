def test_issue_certificate(client, login_as):
    headers = login_as("issuer@example.com")

    response = client.post(
        "/certificates",
        json={
            "holder_name": "Asha Verma",
            "course_name": "Backend Engineering",
            "issue_date": "2026-02-10",
        },
        headers=headers,
    )
    assert response.status_code == 201
    body = response.json()
    assert body["holder_name"] == "Asha Verma"
    assert body["course_name"] == "Backend Engineering"
    assert body["status"] == "valid"
    assert len(body["fingerprint"]) == 64
    assert body["public_id"]
    assert "id" not in body
    assert "issuer_id" not in body

def test_issue_certificate_requires_login(client):
    response = client.post(
        "/certificates",
        json={
            "holder_name": "Asha Verma",
            "course_name": "Backend Engineering",
            "issue_date": "2026-02-10",
        },
    )
    assert response.status_code == 401


def test_list_shows_only_own_certificates(client, login_as):
    headers_a = login_as("a@example.com")
    headers_b = login_as("b@example.com")

    client.post(
        "/certificates",
        json={
            "holder_name": "Asha Verma",
            "course_name": "Backend Engineering",
            "issue_date": "2026-02-10",
        },
        headers=headers_a,
    )

    list_a = client.get("/certificates", headers=headers_a)
    list_b = client.get("/certificates", headers=headers_b)

    assert list_a.status_code == 200
    assert len(list_a.json()) == 1
    assert list_b.status_code == 200
    assert list_b.json() == []


def test_other_issuer_cannot_revoke(client, login_as):
    headers_a = login_as("a@example.com")
    headers_b = login_as("b@example.com")

    issued = client.post(
        "/certificates",
        json={
            "holder_name": "Asha Verma",
            "course_name": "Backend Engineering",
            "issue_date": "2026-02-10",
        },
        headers=headers_a,
    )
    public_id = issued.json()["public_id"]

    attempt = client.patch(f"/certificates/{public_id}/revoke", headers=headers_b)
    assert attempt.status_code == 404

    check = client.get(f"/verify/{public_id}")
    assert check.json()["result"] == "valid"
