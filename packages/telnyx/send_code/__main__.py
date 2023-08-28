import os
import requests
from .utils import Request, process_response, require_post


def entry_point(args):
    request = Request.from_args(args)
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

    API_KEY = os.environ["API_KEY"]
    headers = {"Authorization": f"Bearer {API_KEY}"}
    resp = requests.post(
        "https://api.telnyx.com/v2/verifications/sms",
        headers=headers,
        json=payload,
        timeout=5,
    )
    return resp.json(), resp.status_code
