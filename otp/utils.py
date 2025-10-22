# utils.py
import random


def generate_otp():
    return str(random.randint(100000, 999999))


def mask_email(email):
    if not email or '@' not in email:
        return None

    name, domain = email.split('@')

    if len(name) <= 5:
        masked_name = name[0] + '****'
    else:
        stars = '*' * (len(name) - 2)
        masked_name = f"{name[0]}{stars}{name[-1]}"

    return f"{masked_name}@{domain}"
