from dataclasses import dataclass
from typing import Any


@dataclass
class Request:
    path: str
    method: str
    headers: dict[str, str]
    data: dict[str, Any]
    body: bytes | None

    @classmethod
    def from_args(cls, args):
        http = args.pop("http")
        return cls(
            path=http["path"],
            method=http["method"],
            headers=http["headers"],
            body=http.get("body"),
            data={k: v for k, v in args.items() if not k.startswith("__ow")},
        )


def process_response(resp):
    if not isinstance(resp, tuple):
        return {"body": resp}

    match len(resp):
        case 1:
            return {"body": resp[0]}
        case 2:
            return {"body": resp[0], "statusCode": resp[1]}
        case _:
            raise Exception("idk bro.")


def require_http_methods(method_list, /):
    def decorator(func):
        def wrapper(request):
            if request.method not in method_list:
                return "Method not allowed", 405
            return func(request)

        return wrapper

    return decorator


require_get = require_http_methods(["GET"])
require_post = require_http_methods(["POST"])
