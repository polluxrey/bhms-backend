from django.utils.formats import date_format
import re
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from config.models import BrandingConfig
import string
import random
import os
from uuid import uuid4
from datetime import datetime
from functools import wraps
from django.conf import settings
import requests


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


def parse_room_code(code: str) -> str:
    match = re.match(r"^(\d+)F(?:R(\d+))?$", code, re.IGNORECASE)
    if not match:
        return code

    floor = int(match.group(1))
    room = match.group(2)  # None if no room part

    # Determine floor suffix
    suffix = "th" if 10 <= floor % 100 <= 20 else {
        1: "st", 2: "nd", 3: "rd"
    }.get(floor % 10, "th")

    if room:
        return f"{floor}{suffix} Floor, Room {int(room)}"
    else:
        return f"{floor}{suffix} Floor"


def format_date(date_obj):
    """Return a human-readable date like 'January 1, 2001'."""
    return date_format(date_obj, format='F j, Y') if date_obj else None


def send_sms(phone_number, message):
    payload = {
        "api_token": settings.SMS_API_TOKEN,
        "sender_name": settings.SMS_API_SENDER_NAME,
        "phone_number": phone_number,
        "message": message,
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(
        settings.SMS_API_URL,
        json=payload,
        headers=headers,
        proxies={"https": None},
        timeout=10
    )
    response.raise_for_status()
    return response.json()
