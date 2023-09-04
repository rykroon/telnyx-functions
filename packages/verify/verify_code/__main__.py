import os
import requests
from pydoftk import function, Request


TELNYX_API_KEY = os.environ["TELNYX_API_KEY"]
TELNYX_BASE_URL = os.environ["TELNYX_BASE_URL"]


@function
def main(request: Request):
    request_json = request.json()

    if request.method != "POST":
        return "Method not allowed.", 405
    
    try:
        code = request_json["code"]
        verification_id = request_json["verification_id"]

    except KeyError as e:
        return f"Missing parameter {e}.", 422

    # get verification information.
    headers = {"Authorization": f"Bearer {TELNYX_API_KEY}"}
    url = f"{TELNYX_BASE_URL}/verifications/{verification_id}"
    resp = requests.get(url, headers=headers, timeout=5)
    resp.raise_for_status()
    result = resp.json()

    phone_number = result["data"]["phone_number"]
    verify_profile_id = result["data"]["verify_profile_id"]
    payload = {"code": code, "verify_profile_id": verify_profile_id}

    url = f"{TELNYX_BASE_URL}/v2/verifications/by_phone_number/{phone_number}/actions/verify"
    resp = requests.post(url, headers=headers, json=payload, timeout=5)
    return resp.json(), resp.status_code
