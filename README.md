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
