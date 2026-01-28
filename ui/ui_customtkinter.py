import customtkinter as ctk
from tkinter import messagebox

# -----------------------------------------------------------------------------
# CustomTkinter global configuration
# MUST be set before creating any CTk instance
# -----------------------------------------------------------------------------
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

from core.calculator import WeightChangeCalculator
from core.data_models import WeightChangeInput, Gender
from core.utils import (
    validate_positive,
    validate_gender,
    parse_date,
    validate_date_range,
)
from ui.results_window import ResultsWindow


# -----------------------------------------------------------------------------
# Reusable input component
# -----------------------------------------------------------------------------
class LabeledEntry(ctk.CTkFrame):
    def __init__(self, master, label: str, placeholder: str = ""):
        super().__init__(master)

        self.label = ctk.CTkLabel(self, text=label)
        self.label.pack(anchor="w", pady=(0, 2))

        self.entry = ctk.CTkEntry(
            self,
            placeholder_text=placeholder,
            width=220,
        )
        self.entry.pack()

    def get(self) -> str:
        return self.entry.get().strip()


# -----------------------------------------------------------------------------
# Main Application Window
# -----------------------------------------------------------------------------
class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Weight Change Planner")
        self.geometry("480x600")
        self.resizable(False, False)

        self.calculator = WeightChangeCalculator()

        self._build_ui()

    # -------------------------------------------------------------------------
    # UI construction
    # -------------------------------------------------------------------------
    def _build_ui(self):
        title = ctk.CTkLabel(
            self,
            text="Weight Change Planner",
            font=("Segoe UI", 22, "bold"),
        )
        title.pack(pady=20)

        form = ctk.CTkFrame(self)
        form.pack(pady=10)

        self.start_weight = LabeledEntry(form, "Start Weight (kg)", "e.g. 80")
        self.end_weight = LabeledEntry(form, "Goal Weight (kg)", "e.g. 75")
        self.height_cm = LabeledEntry(form, "Height (cm)", "e.g. 170")

        self.gender_label = ctk.CTkLabel(form, text="Gender")
        self.gender_combo = ctk.CTkComboBox(
            form,
            values=["male", "female"],
            width=220,
        )
        self.gender_combo.set("female")

        self.start_date = LabeledEntry(
            form, "Start Date (DD-MM-YYYY)", "01-01-2024"
        )
        self.end_date = LabeledEntry(
            form, "End Date (DD-MM-YYYY)", "01-02-2024"
        )

        for widget in (
            self.start_weight,
            self.end_weight,
            self.height_cm,
        ):
            widget.pack(pady=6)

        self.gender_label.pack(anchor="w", pady=(10, 0))
        self.gender_combo.pack(pady=4)

        self.start_date.pack(pady=6)
        self.end_date.pack(pady=6)

        calculate_btn = ctk.CTkButton(
            self,
            text="Calculate",
            command=self.on_calculate,
            width=200,
        )
        calculate_btn.pack(pady=30)

    # -------------------------------------------------------------------------
    # Event handlers
    # -------------------------------------------------------------------------
    def on_calculate(self):
        try:
            start_weight = validate_positive(
                self.start_weight.get(), "Start weight"
            )
            end_weight = validate_positive(
                self.end_weight.get(), "End weight"
            )
            height_cm = validate_positive(
                self.height_cm.get(), "Height"
            )

            gender_str = validate_gender(self.gender_combo.get())
            gender = Gender(gender_str)

            start_date = parse_date(
                self.start_date.get(), "Start date"
            )
            end_date = parse_date(
                self.end_date.get(), "End date"
            )

            validate_date_range(start_date, end_date)

            data = WeightChangeInput(
                start_weight=start_weight,
                end_weight=end_weight,
                height_cm=height_cm,
                gender=gender,
                start_date=start_date,
                end_date=end_date,
            )

            result = self.calculator.calculate(data)

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            return
        except Exception as e:
            messagebox.showerror("Unexpected Error", str(e))
            return

        ResultsWindow(self, result)


# -----------------------------------------------------------------------------
# Standalone execution (for development/debugging)
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
