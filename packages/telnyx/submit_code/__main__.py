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

    if "code" not in request.data:
        return "Missing parameter 'code'.", 422
    
    if "verify_profile_id" not in request.data:
        return "Missing parameter 'verify_profile_id'.", 422

    phone_number = request.data["phone_number"]
    code = request.data["code"]
    verify_profile_id = request.data["verify_profile_id"]

    payload = {
        "code": code,
        "verify_profile_id": verify_profile_id
    }

    API_KEY = os.environ["API_KEY"]
    headers = {"Authorization": f"Bearer {API_KEY}"}
    url = f"https://api.telnyx.com/v2/verifications/by_phone_number/{phone_number}/actions/verify"
    resp = requests.post(url, headers=headers, json=payload, timeout=5)
    return resp.json(), resp.status_code
