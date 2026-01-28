from datetime import datetime
from typing import Any


DATE_FORMAT = "%d-%m-%Y"


# ------------------------------------------------------------------
# NUMBER HELPERS
# ------------------------------------------------------------------

def is_float(value: Any) -> bool:
    """
    Returns True if value can be safely converted to float.
    """
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False


def to_float(value: Any, field_name: str) -> float:
    """
    Converts value to float or raises a clear ValueError.
    """
    if not is_float(value):
        raise ValueError(f"{field_name} must be a valid number.")
    return float(value)


def validate_positive(value: Any, field_name: str) -> float:
    """
    Ensures value is a positive float.
    """
    number = to_float(value, field_name)
    if number <= 0:
        raise ValueError(f"{field_name} must be greater than zero.")
    return number


# ------------------------------------------------------------------
# STRING / ENUM HELPERS
# ------------------------------------------------------------------

def validate_gender(value: str) -> str:
    """
    Validates gender string input.
    Returns normalized lowercase value.
    """
    gender = (value or "").strip().lower()
    if gender not in ("male", "female"):
        raise ValueError("Gender must be 'male' or 'female'.")
    return gender


# ------------------------------------------------------------------
# DATE HELPERS
# ------------------------------------------------------------------

def parse_date(date_str: str, field_name: str) -> datetime:
    """
    Parses a date string in DD-MM-YYYY format.
    """
    try:
        return datetime.strptime(date_str, DATE_FORMAT)
    except (TypeError, ValueError):
        raise ValueError(
            f"{field_name} must be in DD-MM-YYYY format."
        )


def format_date(date_obj: datetime) -> str:
    """
    Formats datetime to DD-MM-YYYY string.
    """
    return date_obj.strftime(DATE_FORMAT)


def validate_date_range(start: datetime, end: datetime) -> None:
    """
    Ensures end date is after start date.
    """
    if end <= start:
        raise ValueError("End date must be after start date.")
