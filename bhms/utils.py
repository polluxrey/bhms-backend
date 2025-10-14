import os
from uuid import uuid4
from datetime import datetime
from functools import wraps


def clean_text(value, uppercase=True, lowercase=False):
    if not value:
        return ""
    value = value.strip()
    if uppercase:
        return value.upper()
    if lowercase:
        return value.lower()
    return value


def path_and_rename(base_path="uploads"):
    @wraps(path_and_rename)
    def wrapper(instance, filename):
        ext = filename.split(".")[-1]
        new_filename = f"{uuid4().hex}.{ext}"
        date_path = datetime.now().strftime("%Y/%m/%d")
        return os.path.join(base_path, date_path, new_filename)
    return wrapper
