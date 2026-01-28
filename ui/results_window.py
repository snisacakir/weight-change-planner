import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.lines import Line2D
import mplcursors


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

def format_date(d: datetime) -> str:
    return d.strftime("%d-%m-%Y")


def bmi_color(bmi: float) -> str:
    if bmi < 18.5:
        return "#3b82f6"  # blue
    elif bmi < 25:
        return "#22c55e"  # green
    elif bmi < 30:
        return "#eab308"  # yellow
    else:
        return "#ef4444"  # red


def bmi_label(bmi: float) -> str:
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


def pace_warning(daily_change: float):
    if daily_change < -0.15:
        return (
            "danger",
            "Your average weight loss rate appears higher than commonly recommended.\n"
            "Rapid weight loss may affect muscle mass and metabolic health."
        )
    if daily_change > 0.10:
        return (
            "warning",
            "Your average weight gain rate appears higher than commonly recommended.\n"
            "Rapid weight gain may increase fat accumulation."
        )
    return None, None


# ---------------------------------------------------------------------
# Results Window
# ---------------------------------------------------------------------

class ResultsWindow(ctk.CTkToplevel):
    def __init__(self, master, result):
        super().__init__(master)
        self.result = result

        self.title("Results")
        self.geometry("900x900")
        self.resizable(False, False)

        self._build_ui()

    # -----------------------------------------------------------------
    def _build_ui(self):
        # Title
        title = ctk.CTkLabel(
            self,
            text="Weight Change Overview",
            font=("Segoe UI", 20, "bold"),
        )
        title.pack(pady=15)

        # Health pace warning
        daily_change = self.result.weight_difference / self.result.days
        level, message = pace_warning(daily_change)
        if level:
            color = "#ef4444" if level == "danger" else "#eab308"
            warning = ctk.CTkFrame(self, fg_color=color, corner_radius=10)
            warning.pack(padx=20, pady=(5, 10), fill="x")
            warning_label = ctk.CTkLabel(
                warning,
                text="⚠ Health Pace Warning\n" + message,
                text_color="black",
                justify="left",
                font=("Segoe UI", 11, "bold"),
            )
            warning_label.pack(padx=12, pady=8)

        # Info frame
        info = ctk.CTkFrame(self)
        info.pack(pady=10)
        self._row(info, 0, "Start Weight:", f"{self.result.start_weight:.1f} kg")
        self._row(info, 1, "End Weight:", f"{self.result.end_weight:.1f} kg")
        self._row(info, 2, "Duration:", f"{self.result.days} days")
        self._row(info, 3, "Daily Change:", f"{daily_change:+.2f} kg/day")

        # Chart frame
        chart_frame = ctk.CTkFrame(self)
        chart_frame.pack(pady=20, fill="both", expand=True)

        self._build_weight_chart(chart_frame)

        # Export button
        export_btn = ctk.CTkButton(
            self,
            text="📤 Export Plot",
            command=self._export_plot
        )
        export_btn.pack(pady=5)

    # -----------------------------------------------------------------
    def _row(self, parent, row, label, value):
        l = ctk.CTkLabel(parent, text=label)
        v = ctk.CTkLabel(parent, text=value, font=("Segoe UI", 12, "bold"))
        l.grid(row=row, column=0, sticky="w", padx=10, pady=3)
        v.grid(row=row, column=1, sticky="w", padx=10, pady=3)

    # -----------------------------------------------------------------
    def _build_weight_chart(self, parent):
        self.days = list(range(len(self.result.weights)))
        self.weights = self.result.weights
        self.bmis = self.result.bmis
        self.height_m = self.result.height_cm / 100

        self.fig, self.ax = plt.subplots(figsize=(7, 4.5))

        # BMI bands
        def weight_for_bmi(bmi): return bmi * (self.height_m ** 2)
        bands = [
            (0, 18.5, "#3b82f6"),  # Underweight
            (18.5, 25, "#22c55e"), # Normal
            (25, 30, "#eab308"),   # Overweight
            (30, 60, "#ef4444"),   # Obese
        ]
        for bmi_min, bmi_max, color in bands:
            self.ax.axhspan(weight_for_bmi(bmi_min),
                            weight_for_bmi(bmi_max),
                            color=color, alpha=0.08, zorder=0)

        # BMI-colored line
        for i in range(len(self.weights) - 1):
            self.ax.plot(
                self.days[i:i + 2],
                self.weights[i:i + 2],
                color=bmi_color(self.bmis[i]),
                linewidth=3, zorder=3
            )

        # Hover tooltips
        scatter = self.ax.scatter(self.days, self.weights, s=40, alpha=0)
        cursor = mplcursors.cursor(scatter, hover=True)

        @cursor.connect("add")
        def on_add(sel):
            idx = sel.index
            bmi = self.bmis[idx]
            sel.annotation.set(
                text=(
                    f"Day {idx}\n"
                    f"Weight: {self.weights[idx]:.1f} kg\n"
                    f"BMI: {bmi:.1f} ({bmi_label(bmi)})"
                )
            )
            sel.annotation.get_bbox_patch().set(fc="white", alpha=0.95)

        # Styling
        self.ax.set_title("Weight Change Over Time (BMI Zones)")
        self.ax.set_xlabel("Days")
        self.ax.set_ylabel("Weight (kg)")
        self.ax.grid(True, linestyle="--", alpha=0.4)
        legend_elements = [
            Line2D([0], [0], color="#3b82f6", lw=4, label="Underweight"),
            Line2D([0], [0], color="#22c55e", lw=4, label="Normal"),
            Line2D([0], [0], color="#eab308", lw=4, label="Overweight"),
            Line2D([0], [0], color="#ef4444", lw=4, label="Obese"),
        ]
        self.ax.legend(handles=legend_elements, loc="best")

        # Canvas & toolbar
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.toolbar = NavigationToolbar2Tk(self.canvas, parent)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    # -----------------------------------------------------------------
    def _export_plot(self):
        try:
            filename = f"weight_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            self.fig.savefig(filename, dpi=150)
            messagebox.showinfo("Saved", f"Plot saved as {filename}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
