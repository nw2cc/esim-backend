import hashlib

from typing import Any


def md5(content: Any):
    md5_object = hashlib.md5()
    md5_object.update(str(content).encode('utf-8'))
    return md5_object.hexdigest()
