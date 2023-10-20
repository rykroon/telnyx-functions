import os
import requests
from seastar.applications import seastar
from seastar.exceptions import HttpException
from seastar.requests import Request
from seastar.responses import Response


TELNYX_API_KEY = os.environ["TELNYX_API_KEY"]
TELNYX_BASE_URL = os.environ["TELNYX_BASE_URL"]


@seastar(methods=["POST"], debug=True)
def main(request: Request):
    request_json = request.json()

    try:
        code = request_json["code"]
        verification_id = request_json["verification_id"]

    except KeyError as e:
        raise HttpException(422, f"Missing parameter {e}.")

    # get verification information.
    headers = {"Authorization": f"Bearer {TELNYX_API_KEY}"}
    url = f"{TELNYX_BASE_URL}/v2/verifications/{verification_id}"
    resp = requests.get(url, headers=headers, timeout=5)
    if not resp.ok:
        return Response(resp.content.decode(), resp.status_code, resp.headers)

    result = resp.json()
    phone_number = result["data"]["phone_number"]
    verify_profile_id = result["data"]["verify_profile_id"]
    payload = {"code": code, "verify_profile_id": verify_profile_id}

    url = f"{TELNYX_BASE_URL}/v2/verifications/by_phone_number/{phone_number}/actions/verify"
    resp = requests.post(url, headers=headers, json=payload, timeout=5)
    return Response(resp.content.decode(), resp.status_code, resp.headers)
