from seastar import web_function
from seastar.requests import Request
from seastar.responses import PlainTextResponse



@web_function(methods=["POST"])
def main(request: Request):
    return PlainTextResponse("Hello World")
