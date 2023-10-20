from seastar.applications import seastar
from seastar.requests import Request
from seastar.responses import PlainTextResponse



@seastar(methods=["POST"])
def main(request: Request):
    return PlainTextResponse("Hello World")
