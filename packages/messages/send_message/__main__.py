import os
from pydoftk import function, Request
import requests


TELNYX_API_KEY = os.environ["TELNYX_API_KEY"]
TELNYX_BASE_URL = os.environ["TELNYX_BASE_URL"]


@function
def main(request: Request):
    if request.method != "POST":
        return "Method not allowed.", 405

    # parameters
    # - from, to, text, media_urls.

    headers = {"Authorization": f"Bearer {TELNYX_API_KEY}"}
    resp = requests.post(
        url=f"{TELNYX_BASE_URL}/v2/messages",
        json=request.json(),
        headers=headers,
        timeout=5
    )

    return resp.json(), resp.status_code
