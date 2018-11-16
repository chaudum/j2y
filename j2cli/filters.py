import json
import yaml
import hashlib
from base64 import urlsafe_b64decode, urlsafe_b64encode

UTF8 = "utf-8"


registry = {
    "json": json.dumps,
    "yaml": yaml.dump,
    "b64encode": lambda a: urlsafe_b64encode(a.encode(UTF8)).decode(UTF8),
    "b64decode": lambda a: urlsafe_b64decode(a.encode(UTF8)).decode(UTF8),
    "md5sum": lambda a: hashlib.md5(a.encode(UTF8)).hexdigest(),
    "sha1sum": lambda a: hashlib.sha1(a.encode(UTF8)).hexdigest(),
    "sha256sum": lambda a: hashlib.sha256(a.encode(UTF8)).hexdigest(),
    "sha512sum": lambda a: hashlib.sha512(a.encode(UTF8)).hexdigest(),
}
