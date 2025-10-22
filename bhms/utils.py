from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from config.models import BrandingConfig
import string
from django.db.models import Model
import random
import os
from uuid import uuid4
from datetime import datetime
from functools import wraps
# from collections import OrderedDict


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


def generate_random_ref(length: int = 7) -> str:
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))


def send_email(
    subject: str,
    template_name: str,
    context: dict,
    from_email: str,
    to: list = None,
    bcc: list = None,
):
    app_name = BrandingConfig.get_app_name()
    context.setdefault("boarding_house_name", app_name)

    message = render_to_string(template_name, context)

    if not (to or bcc):
        raise ValueError("At least one recipient (to or bcc) must be provided")

    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=from_email,
        to=to or [],
        bcc=bcc or [],
    )

    email.send(fail_silently=True)


# def serialize_choices(choices_class):
#     return [
#         OrderedDict(value=value, label=label)
#         for value, label in choices_class.choices
#     ]
