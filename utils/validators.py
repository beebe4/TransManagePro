import re

def validate_dot_number(dot_number):
    """Validate DOT number format."""
    return bool(re.match(r'^\d{6,7}$', dot_number))

def validate_phone(phone):
    """Validate phone number format."""
    return bool(re.match(r'^\+?1?\d{10,12}$', phone))

def validate_email(email):
    """Validate email format."""
    return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))

def validate_mc_number(mc_number):
    """Validate MC number format."""
    return bool(re.match(r'^MC\d{6}$', mc_number))
