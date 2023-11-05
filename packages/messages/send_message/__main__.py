import os
from seastar import web_function
from seastar.requests import Request
from seastar.responses import JSONResponse
import requests


TELNYX_API_KEY = os.environ["TELNYX_API_KEY"]
TELNYX_BASE_URL = os.environ["TELNYX_BASE_URL"]


@web_function(methods=["POST"])
def main(request: Request):
    # parameters
    # - from, to, text, media_urls.
    headers = {"Authorization": f"Bearer {TELNYX_API_KEY}"}
    resp = requests.post(
        url=f"{TELNYX_BASE_URL}/v2/messages",
        json=request.json(),
        headers=headers,
        timeout=5
    )

    return JSONResponse(resp.json(), resp.status_code)
