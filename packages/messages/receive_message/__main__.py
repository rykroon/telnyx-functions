from seastar.application import seastar
from seastar.requests import Request
from seastar.responses import PlainTextResponse



@seastar
def main(request: Request):
    return PlainTextResponse("Hello World")
