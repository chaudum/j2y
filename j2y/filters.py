import base64


registry = {
    "b64encode": lambda a: base64.urlsafe_b64encode(a.encode("utf-8")).decode("utf-8"),
    "b64decode": lambda a: base64.urlsafe_b64decode(a.encode("utf-8")).decode("utf-8"),
}
