import os
import requests
from pydoftk import function, Request


@function
def main(request: Request):
    if request.method != "POST":
        return "Method not allowed", 405

    request_json = request.json()
    if "phone_number" not in request_json:
        return "Missing parameter 'phone_number'.", 422

    phone_number = request_json["phone_number"]
    verify_profile_id = request_json.get(
        "verify_profile_id", os.environ["DEFAULT_VERIFY_PROFILE_ID"]
    )

    payload = {"phone_number": phone_number, "verify_profile_id": verify_profile_id}

    TELNYX_API_KEY = os.environ["TELNYX_API_KEY"]
    headers = {"Authorization": f"Bearer {TELNYX_API_KEY}"}
    resp = requests.post(
        "https://api.telnyx.com/v2/verifications/sms",
        headers=headers,
        json=payload,
        timeout=5,
    )
    return resp.json(), resp.status_code