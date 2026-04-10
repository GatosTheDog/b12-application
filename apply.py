import hashlib
import hmac
import json
import os
from datetime import datetime, timezone

import requests

SIGNING_SECRET = os.environ.get("SIGNING_SECRET", "hello-there-from-b12")
SUBMIT_URL = "https://b12.io/apply/submission"

payload = {
    "action_run_link": os.environ["ACTION_RUN_LINK"],
    "email": "manolis22940@yahoo.gr",
    "name": "Manolis Kypriotakis",
    "repository_link": os.environ["REPOSITORY_LINK"],
    "resume_link": "https://www.linkedin.com/in/manolis-kypriotakis",
    "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.") + f"{datetime.now(timezone.utc).microsecond // 1000:03d}Z",
}

# Canonical JSON: sorted keys, compact separators, UTF-8
body = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")

# HMAC-SHA256 signature
signature = hmac.new(SIGNING_SECRET.encode("utf-8"), body, hashlib.sha256).hexdigest()

headers = {
    "Content-Type": "application/json",
    "X-Signature-256": f"sha256={signature}",
}

response = requests.post(SUBMIT_URL, data=body, headers=headers)
response.raise_for_status()

result = response.json()
print(f"Submission receipt: {result['receipt']}")
