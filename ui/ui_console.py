from datetime import datetime

from core.calculator import WeightChangeCalculator
from core.data_models import WeightChangeInput, Gender
from core.utils import (
    validate_positive,
    validate_gender,
    parse_date,
    validate_date_range,
)


class ConsoleUI:
    """
    Console-based user interface for the Weight Change Calculator.
    Responsible ONLY for:
    - collecting user input
    - displaying results

    All validation & calculations are delegated to core modules.
    """

    def __init__(self):
        self.calculator = WeightChangeCalculator()

    def run(self):
        try:
            data = self._collect_input()
            result = self.calculator.calculate(data)
            self._display_result(result)
        except ValueError as e:
            print(f"\n[ERROR] {e}")

    # ------------------------------------------------------------------
    # INPUT
    # ------------------------------------------------------------------

    def _collect_input(self) -> WeightChangeInput:
        print("\n=== Weight Change Calculator ===\n")

        start_weight = validate_positive(
            input("Start weight (kg): "), "start_weight"
        )
        end_weight = validate_positive(
            input("End weight (kg): "), "end_weight"
        )
        height_cm = validate_positive(
            input("Height (cm): "), "height_cm"
        )

        gender_str = validate_gender(input("Gender (male/female): "))
        gender = Gender(gender_str)

        start_date = parse_date(
            input("Start date (DD-MM-YYYY): "), "start_date"
        )
        end_date = parse_date(
            input("End date (DD-MM-YYYY): "), "end_date"
        )

        validate_date_range(start_date, end_date)

        return WeightChangeInput(
            start_weight=start_weight,
            end_weight=end_weight,
            height_cm=height_cm,
            gender=gender,
            start_date=start_date,
            end_date=end_date,
        )

    # ------------------------------------------------------------------
    # OUTPUT
    # ------------------------------------------------------------------

    def _display_result(self, result):
        print("\n--- Results ---")
        print(f"Start weight : {result.start_weight:.1f} kg")
        print(f"End weight   : {result.end_weight:.1f} kg")
        print(f"Difference   : {result.weight_difference:+.1f} kg")
        print(f"Days         : {result.days}")
        print(f"Start BMI    : {result.bmi_start:.1f}")
        print(f"End BMI      : {result.bmi_end:.1f}")

        if result.is_weight_loss:
            print("Status       : Weight loss ✅")
        elif result.is_weight_gain:
            print("Status       : Weight gain ⚠️")
        else:
            print("Status       : Weight stable ➖")