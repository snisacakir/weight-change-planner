import pytest
from datetime import datetime

from core.calculator import WeightChangeCalculator
from core.data_models import WeightChangeInput, Gender

@pytest.fixture
def calculator():
    return WeightChangeCalculator()

### HAPPY PATH ###

def test_weight_change_calculation(calculator):
    data = WeightChangeInput(
        start_weight=80,
        end_weight=75,
        height_cm=170,
        gender=Gender.FEMALE,
        start_date=datetime(2024, 1, 1),
        end_date=datetime(2024, 2, 1),
    )

    result = calculator.calculate(data)

    assert result.weight_difference == -5
    assert result.days == 31
    assert result.is_weight_loss is True

def test_weight_gain_detection(calculator):
    data = WeightChangeInput(
        start_weight=70,
        end_weight=75,
        height_cm=175,
        gender=Gender.MALE,
        start_date=datetime(2024, 1, 1),
        end_date=datetime(2024, 1, 11),
    )

    result = calculator.calculate(data)

    assert result.weight_difference == 5
    assert result.is_weight_gain is True

### EDGE CASE ###

def test_no_weight_change(calculator):
    data = WeightChangeInput(
        start_weight=70,
        end_weight=70,
        height_cm=180,
        gender=Gender.MALE,
        start_date=datetime(2024, 1, 1),
        end_date=datetime(2024, 1, 10),
    )

    result = calculator.calculate(data)

    assert result.weight_difference == 0
    assert result.is_weight_stable is True

def test_same_day_raises_error(calculator):
    data = WeightChangeInput(
        start_weight=80,
        end_weight=75,
        height_cm=170,
        gender=Gender.FEMALE,
        start_date=datetime(2024, 1, 1),
        end_date=datetime(2024, 1, 1),
    )

    with pytest.raises(ValueError):
        calculator.calculate(data)

### INPUT VALIDATION ###

def test_negative_weight_raises_error(calculator):
    data = WeightChangeInput(
        start_weight=-70,
        end_weight=65,
        height_cm=170,
        gender=Gender.FEMALE,
        start_date=datetime(2024, 1, 1),
        end_date=datetime(2024, 1, 10),
    )

    with pytest.raises(ValueError, match="weight"):
        calculator.calculate(data)

### SMOKE TEST ###

def test_result_type(calculator):
    data = WeightChangeInput(
        start_weight=90,
        end_weight=85,
        height_cm=185,
        gender=Gender.MALE,
        start_date=datetime(2024, 1, 1),
        end_date=datetime(2024, 2, 1),
    )

    result = calculator.calculate(data)

    assert hasattr(result, "weight_difference")
    assert hasattr(result, "bmi_start")
    assert hasattr(result, "bmi_end")



