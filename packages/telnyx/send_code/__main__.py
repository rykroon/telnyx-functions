import os
import requests
from utils import Request, process_response, require_post


def entry_point(event):
    request = Request.from_event(event)
    return process_response(main(request))


@require_post
def main(request):
    if "phone_number" not in request.data:
        return "Missing parameter 'phone_number'.", 422

    phone_number = request.data["phone_number"]
    verify_profile_id = request.data.get(
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
