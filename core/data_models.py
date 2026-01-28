from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List


# ------------------------------------------------------------------
# ENUMS
# ------------------------------------------------------------------
class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"


# ------------------------------------------------------------------
# INPUT MODEL
# ------------------------------------------------------------------
@dataclass(frozen=True)
class WeightChangeInput:
    start_weight: float
    end_weight: float
    height_cm: float
    gender: Gender
    start_date: datetime
    end_date: datetime


# ------------------------------------------------------------------
# RESULT MODEL
# ------------------------------------------------------------------
@dataclass(frozen=True)
class WeightChangeResult:
    # --- raw inputs (for UI & plots) ---
    start_weight: float
    end_weight: float
    height_cm: float

    # --- timeline ---
    start_date: datetime
    end_date: datetime
    days: int

    # --- weight change ---
    weight_difference: float
    daily_change: float
    weights: List[float]

    # --- BMI ---
    bmi_start: float
    bmi_end: float
    bmis: List[float]

    # ------------------------------------------------------------------
    # Derived properties
    # ------------------------------------------------------------------
    @property
    def is_weight_loss(self) -> bool:
        return self.weight_difference < 0

    @property
    def is_weight_gain(self) -> bool:
        return self.weight_difference > 0

    @property
    def is_weight_stable(self) -> bool:
        return self.weight_difference == 0
