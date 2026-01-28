"""
app.py

Single entry point for the Weight Change Planner application.

Supports:
- GUI mode (CustomTkinter)
- CLI mode (terminal)

Usage:
    python app.py            # GUI (default)
    python app.py --mode cli # CLI
"""

import argparse
import sys


# -----------------------------------------------------------------------------
# Safe imports
# -----------------------------------------------------------------------------
def load_cli():
    try:
        from ui.ui_console import ConsoleUI
        return ConsoleUI
    except Exception as e:
        print(f"[CLI LOAD ERROR] {e}")
        return None


def load_gui():
    try:
        from ui.ui_customtkinter import MainApp
        return MainApp
    except Exception as e:
        print(f"[GUI LOAD ERROR] {e}")
        return None


# -----------------------------------------------------------------------------
# Argument parsing
# -----------------------------------------------------------------------------
def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Weight Change Planner Application"
    )

    parser.add_argument(
        "--mode",
        choices=("gui", "cli"),
        default="gui",
        help="Interface mode (default: gui)",
    )

    return parser.parse_args()


# -----------------------------------------------------------------------------
# Runners
# -----------------------------------------------------------------------------
def run_cli():
    ConsoleUI = load_cli()
    if ConsoleUI is None:
        print("❌ CLI interface unavailable.")
        sys.exit(1)

    print("Starting application in CLI mode...\n")
    ConsoleUI().run()


def run_gui():
    MainApp = load_gui()
    if MainApp is None:
        print("⚠ GUI unavailable. Falling back to CLI...\n")
        return run_cli()

    print("Starting application in GUI mode...")
    app = MainApp()
    app.mainloop()


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
def main():
    args = parse_arguments()

    if args.mode == "cli":
        run_cli()
    else:
        run_gui()


if __name__ == "__main__":
    main()
