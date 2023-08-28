from dataclasses import dataclass, field
from typing import Any


@dataclass
class Request:
    headers: dict[str, str]
    method: str
    path: str
    body: str | None
    is_base64_encoded: bool | None
    query_string: str | None
    data: dict[str, Any]

    @classmethod
    def from_event(cls, event):
        http = event["http"]
        return cls(
            headers=http["headers"],
            method=http["method"],
            path=http["path"],
            body=http.get("body"),
            is_base64_encoded=http.get("isBase64Encoded"),
            query_string=http.get("queryString"),
            data={
                k: v
                for k, v in event.items()
                if not k.startswith("__ow") and k != "http"
            },
        )


@dataclass
class Response:
    body: Any
    status_code: int = 200
    headers: dict[str, str] = field(default_factory=dict)


def process_response(resp):
    if isinstance(resp, Response):
        return {"body": resp.body, "statusCode": resp.status_code, "headers": resp.headers}

    elif not isinstance(resp, tuple):
        return {"body": resp}

    match len(resp):
        case 1:
            return {"body": resp[0]}
        case 2:
            return {"body": resp[0], "statusCode": resp[1]}
        case 3:
            return {"body": resp[0], "statusCode": resp[1], "headers": resp[2]}


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