import os
import requests

from starlette.exceptions import HTTPException

from seastar import web_function
from seastar.requests import Request
from seastar.responses import JSONResponse


TELNYX_API_KEY = os.environ["TELNYX_API_KEY"]
TELNYX_BASE_URL = os.environ["TELNYX_BASE_URL"]


@web_function(methods=["POST"])
def main(request: Request):
    request_json = request.json()
    if "phone_number" not in request_json:
        raise HTTPException(422, "Missing parameter 'phone_number'.")

    phone_number = request_json["phone_number"]
    verify_profile_id = request_json.get(
        "verify_profile_id", os.environ["DEFAULT_VERIFY_PROFILE_ID"]
    )

    payload = {"phone_number": phone_number, "verify_profile_id": verify_profile_id}
    headers = {"Authorization": f"Bearer {TELNYX_API_KEY}"}
    resp = requests.post(
        f"{TELNYX_BASE_URL}/v2/verifications/sms",
        headers=headers,
        json=payload,
        timeout=5,
    )
    return JSONResponse(resp.json(), resp.status_code)
