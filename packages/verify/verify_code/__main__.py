import os
import requests
from pydoftk import function, Request


@function
def main(request: Request):
    request_json = request.json()

    if request.method != "POST":
        return "Method not allowed.", 405

    if "phone_number" not in request_json:
        return "Missing parameter 'phone_number'.", 422

    if "code" not in request_json:
        return "Missing parameter 'code'.", 422

    if "verify_profile_id" not in request_json:
        return "Missing parameter 'verify_profile_id'.", 422

    phone_number = request_json["phone_number"]
    code = request_json["code"]
    verify_profile_id = request_json["verify_profile_id"]

    payload = {
        "code": code,
        "verify_profile_id": verify_profile_id
    }

    TELNYX_API_KEY = os.environ["TELNYX_API_KEY"]
    headers = {"Authorization": f"Bearer {TELNYX_API_KEY}"}
    url = f"https://api.telnyx.com/v2/verifications/by_phone_number/{phone_number}/actions/verify"
    resp = requests.post(url, headers=headers, json=payload, timeout=5)
    return resp.json(), resp.status_code
