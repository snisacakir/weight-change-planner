from datetime import timedelta
from typing import List

from core.data_models import (
    WeightChangeInput,
    WeightChangeResult,
    Gender,
)
from core.utils import (
    validate_positive,
    validate_date_range,
)


class WeightChangeCalculator:
    """
    Core business logic for weight change planning.

    Responsibilities:
    - Input validation (domain-level)
    - Weight timeline calculation
    - BMI calculation
    - Result aggregation

    This module is UI-agnostic.
    """

    # ------------------------------------------------------------------
    # PUBLIC API
    # ------------------------------------------------------------------
    def calculate(self, data: WeightChangeInput) -> WeightChangeResult:
        """
        Perform weight change calculation based on provided input.
        """

        # --------------------------------------------------------------
        # Validation
        # --------------------------------------------------------------
        start_weight = validate_positive(data.start_weight, "Start weight")
        end_weight = validate_positive(data.end_weight, "End weight")
        height_cm = validate_positive(data.height_cm, "Height")

        validate_date_range(data.start_date, data.end_date)

        # --------------------------------------------------------------
        # Time calculations
        # --------------------------------------------------------------
        total_days = (data.end_date - data.start_date).days
        if total_days <= 0:
            raise ValueError("Date range must be at least 1 day.")

        # --------------------------------------------------------------
        # Weight calculations
        # --------------------------------------------------------------
        weight_difference = end_weight - start_weight
        daily_change = weight_difference / total_days

        weights: List[float] = []
        bmis: List[float] = []

        for day in range(total_days + 1):
            current_weight = start_weight + daily_change * day
            current_weight = round(current_weight, 2)

            weights.append(current_weight)
            bmis.append(self._calculate_bmi(current_weight, height_cm))

        # --------------------------------------------------------------
        # BMI boundaries
        # --------------------------------------------------------------
        bmi_start = bmis[0]
        bmi_end = bmis[-1]

        # --------------------------------------------------------------
        # Result
        # --------------------------------------------------------------
        return WeightChangeResult(
            start_weight=start_weight,
            end_weight=end_weight,
            height_cm=height_cm,
            start_date=data.start_date,
            end_date=data.end_date,
            days=total_days,
            weight_difference=round(weight_difference, 2),
            daily_change=round(daily_change, 4),
            weights=weights,
            bmis=bmis,
            bmi_start=bmi_start,
            bmi_end=bmi_end,
        )

    # ------------------------------------------------------------------
    # INTERNAL HELPERS
    # ------------------------------------------------------------------
    @staticmethod
    def _calculate_bmi(weight: float, height_cm: float) -> float:
        """
        BMI = weight (kg) / height (m)^2
        """
        height_m = height_cm / 100
        bmi = weight / (height_m ** 2)
        return round(bmi, 2)
