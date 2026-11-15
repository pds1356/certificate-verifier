# Certificate Verifier

An API for issuing certificates and verifying them publicly, with SHA-256 tamper detection.

![Valid certificate](docs/screenshots/valid.png)

## Why this exists

Certificates are easy to edit or fake, and an employer has no quick way to check one. This project lets an institution issue certificates and lets anyone verify them through a public link or QR code, with no login needed.

## What it does

- Issuers register and log in (passwords are hashed, logins use JWT tokens).
- An issuer creates a certificate. The server stores it with a unique public ID and a SHA-256 fingerprint of its details.
- Anyone can open the verification link and see one of four results: **valid**, **revoked**, **tampered** or **not found**.
- If a certificate's stored data is edited after issuing, the fingerprint no longer matches and verification reports it as tampered.
- Issuers can list only their own certificates, and revoke only their own.
- Every certificate has a QR code that points to its verification page.

## How verification works

1. When a certificate is issued, the server creates a random public ID and computes a SHA-256 fingerprint from the ID, holder name, course name and issue date.
2. The fingerprint is stored with the certificate.
3. When someone verifies a certificate, the server recomputes the fingerprint from the stored data and compares it with the saved one.
4. If they match, the result is **valid** (or **revoked**, if the issuer cancelled it). If they differ, the data was changed after issuing, and the result is **tampered**.

The data is written in a fixed JSON form before hashing, so two different certificates can never produce the same text.

## Results

| Valid | Revoked |
|---|---|
| <img src="docs/screenshots/valid.png" width="300"> | <img src="docs/screenshots/revoked.png" width="300"> |

| Tampered | Not found |
|---|---|
| <img src="docs/screenshots/tampered.png" width="300"> | <img src="docs/screenshots/not_found.png" width="300"> |

A tampered result deliberately shows no holder, course or date, because the edited data can't be trusted.

## Tech stack

| Tool | Used for |
|---|---|
| Python 3.12, FastAPI | The API and its automatic `/docs` page |
| PostgreSQL 16 | Storing users and certificates |
| SQLAlchemy | Talking to the database from Python |
| Pydantic | Validating incoming data and shaping responses |
| JWT (PyJWT), pwdlib (argon2) | Login tokens and password hashing |
| hashlib (SHA-256) | Certificate fingerprints |
| qrcode | QR code images |
| pytest | Automated tests |
| Docker, Docker Compose | Running the app and database together |
| HTML, CSS, JavaScript | The public verification page |

## Project structure

```
certificate-verifier/
├── app/
│   ├── main.py            # app setup, router registration, /health
│   ├── database.py        # database engine and session
│   ├── models.py          # database tables (users, certificates)
│   ├── schemas.py         # request and response shapes
│   ├── security.py        # password hashing and JWT creation
│   ├── dependencies.py    # get_current_user (token check)
│   ├── fingerprint.py     # SHA-256 fingerprint function
│   ├── routers/
│   │   ├── auth.py        # register and login
│   │   ├── certificates.py  # issue, list own, revoke
│   │   ├── verify.py      # public verification and QR code
│   │   └── pages.py       # serves the verification page
│   └── static/
│       └── verify.html    # the page a QR code opens
├── tests/                 # pytest tests
├── docs/screenshots/      # images used in this README
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

## Run it with Docker

You need Docker Desktop installed and running.

1. Clone the repo and open the folder.
2. Copy `.env.example` to `.env`:
   ```
   cp .env.example .env
   ```
3. In `.env`, set `POSTGRES_PASSWORD` to a simple password (letters and digits only) and `SECRET_KEY` to a long random string. You can generate one with:
   ```
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
4. Start the app and the database:
   ```
   docker compose up --build
   ```
5. Open http://localhost:8000/docs to try the API.

The database starts empty, so register a user first (`POST /register`), log in with the **Authorize** button, then issue a certificate. Open `http://localhost:8000/v/<public_id>` to see its verification page.

## Run the tests

The tests need Python 3.12 and a local PostgreSQL server with two empty databases: `certdb` and `certdb_test`. Set `DATABASE_URL` and `TEST_DATABASE_URL` in `.env` to match.

```
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
pytest
```

The tests run only against `certdb_test`. The test setup refuses to start if the database name doesn't end in `_test`, so it can't delete real data.
