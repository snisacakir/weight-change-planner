# 🏋️‍♀️ Weight Change Planner

A **cleanly architected Python application** that helps users plan and visualize weight change (loss or gain) over time.  
The project is designed to demonstrate **production-ready Python practices**, including separation of concerns, input validation, testing, and multiple user interfaces (GUI & CLI).

This repository is intended as a **portfolio project** for junior software / Python engineer roles.

---

## ✨ Key Highlights (Why this project matters)

- ✅ **Clear separation of layers** (UI · Core Logic · Validation · Data Models)
- ✅ **Single source of truth** for business logic (shared by GUI & CLI)
- ✅ **Strong input validation & error handling**
- ✅ **Enum-based domain modeling** (no magic strings)
- ✅ **Unit-tested core logic** with PyTest
- ✅ **Crash-safe GUI entry point**
- ✅ **Enhanced results visualization (BMI-colored line, BMI bands, hover info, zoom/pan & export)**
- ✅ **Health pace warning for unusually fast weight loss/gain**


---

## 🧠 What the App Does

Users provide:
- start weight
- target weight
- height
- gender
- start & end dates

The application calculates:
- total weight difference
- number of days in the plan
- BMI at start and end
- whether the plan is **weight loss, gain, or stable**

Results are displayed via:
- 🖥️ a **CustomTkinter GUI**
- 🧑‍💻 a **terminal-based CLI** (same logic, different interface)
- The GUI chart includes:
     - BMI background bands (blue/green/yellow/red)
     - BMI-colored weight trajectory line
     - Hover tooltips showing Day | Weight | BMI (Category)
     - Health pace warnings if daily change exceeds recommended thresholds
     - Interactive zoom & pan
     - Export chart as PNG

---

## 🧱 Architecture Overview

```text
wlc/
│
├── app.py                  # Single entry point (GUI / CLI switch)
│
├── core/                   # Business logic (UI-agnostic)
│   ├── calculator.py       # Weight & BMI calculations
│   ├── data_models.py      # Dataclasses & enums
│   └── utils.py            # Validation helpers
│
├── ui/                     # Presentation layer
│   ├── ui_customtkinter.py # GUI implementation
│   ├── ui_console.py       # CLI implementation
│   └── results_window.py   # Result display window
│
├── tests/                  # Automated tests
│   ├── test_calculator.py
│   └── test_utils.py
│
├── requirements.txt
└── README.md
```

### Design Principles Used
- **Single Responsibility Principle**
- **Explicit data models** instead of loose dictionaries
- **No business logic in UI layers**
- **Fail fast, fail clearly** (validated inputs)

---

## 🚀 Running the Application

### 1️⃣ Create a virtual environment

```bash
python -m venv venv
```

Activate it:

- Windows:
```bash
venv\Scripts\activate
```
- macOS / Linux:
```bash
source venv/bin/activate
```

---

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Run the app

**GUI (default):**
```bash
python app.py
```

**CLI mode:**
```bash
python app.py --mode cli
```

---

## 🧪 Running Tests

All core logic is covered by unit tests.

```bash
pytest
```

Tests validate:
- calculation correctness
- edge cases
- invalid inputs

---

## 🛠 Technologies Used

| Category | Tool |
|--------|------|
| Language | Python 3 |
| GUI | CustomTkinter |
| Validation | Custom utilities |
| Testing | PyTest |
| Architecture | Layered / Clean Architecture |
| Charts | Matplotlib + mplcursors (interactive BMI line + bands)

---

## 📌 What This Project Demonstrates

It demonstrates:
- how to design reusable core logic
- how to share business logic across interfaces
- how to write maintainable, testable Python code
- how to structure a small but realistic application
- interactive and informative data visualization (BMI line + bands hover)
- health warnings for unusual weight change rates

---

## 👩‍💻 Author Notes

This project was built to move beyond "tutorial-style" projects and closer to **real-world Python application design**.

It can be easily extended with:
- persistent storage (SQLite / JSON)
- charts & visualizations
- configuration files
- packaging as an executable

---

📫 *Feedback and suggestions are welcome.*