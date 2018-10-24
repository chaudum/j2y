from base64 import urlsafe_b64decode, urlsafe_b64encode

UTF8 = "utf-8"

registry = {
    "b64encode": lambda a: urlsafe_b64encode(a.encode(UTF8)).decode(UTF8),
    "b64decode": lambda a: urlsafe_b64decode(a.encode(UTF8)).decode(UTF8),
}
