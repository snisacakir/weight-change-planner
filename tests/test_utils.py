import pytest
from datetime import datetime

from core.utils import (
    is_float,
    to_float,
    validate_positive,
    validate_gender,
    parse_date,
    format_date,
    validate_date_range,
)

### NUMBER HELPERS ###

# is_float

def test_is_float_valid():
    assert is_float(10)
    assert is_float("3.14")
    assert is_float("-5")
    assert is_float(0)


def test_is_float_invalid():
    assert not is_float("abc")
    assert not is_float("")
    assert not is_float(None)

# to_float

def test_to_float_valid():
    assert to_float("5", "value") == 5.0
    assert to_float(2.5, "value") == 2.5


def test_to_float_invalid():
    with pytest.raises(ValueError):
        to_float("abc", "value")

# validate_positive

def test_validate_positive_valid():
    assert validate_positive("10", "weight") == 10.0
    assert validate_positive(3.5, "height") == 3.5


def test_validate_positive_zero_or_negative():
    with pytest.raises(ValueError):
        validate_positive(0, "weight")

    with pytest.raises(ValueError):
        validate_positive(-5, "weight")

### STRING / ENUM HELPERS

# validate_gender

def test_validate_gender_valid():
    assert validate_gender("male") == "male"
    assert validate_gender("FEMALE") == "female"
    assert validate_gender("  Male ") == "male"


def test_validate_gender_invalid():
    with pytest.raises(ValueError):
        validate_gender("other")

    with pytest.raises(ValueError):
        validate_gender("")

    with pytest.raises(ValueError):
        validate_gender(None)

### DATE HELPERS ###

# parse_date

def test_parse_date_valid():
    date = parse_date("01-02-2024", "start_date")
    assert isinstance(date, datetime)
    assert date.day == 1
    assert date.month == 2
    assert date.year == 2024


def test_parse_date_invalid():
    with pytest.raises(ValueError):
        parse_date("2024-02-01", "start_date")

    with pytest.raises(ValueError):
        parse_date("", "start_date")

    with pytest.raises(ValueError):
        parse_date(None, "start_date")

# format_date

def test_format_date():
    date = datetime(2024, 3, 15)
    assert format_date(date) == "15-03-2024"

# validate_date_range

def test_validate_date_range_valid():
    start = datetime(2024, 1, 1)
    end = datetime(2024, 1, 10)

    validate_date_range(start, end)  # should not raise


def test_validate_date_range_invalid():
    start = datetime(2024, 1, 10)
    end = datetime(2024, 1, 1)

    with pytest.raises(ValueError):
        validate_date_range(start, end)

    with pytest.raises(ValueError):
        validate_date_range(start, start)
