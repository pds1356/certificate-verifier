import hashlib
import json
from datetime import date

def compute_fingerprint(public_id: str, holder_name: str, course_name: str, issue_date: date) -> str:
    data = {
        "public_id": public_id,
        "holder_name": holder_name,
        "course_name": course_name,
        "issue_date": issue_date.isoformat(),
    }
    canonical = json.dumps(data, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
