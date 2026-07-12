import sqlite3
import questionary
from habit_tracker import (
    HabitCreator,
    HabitEditor,
    HabitAnalyzer,
    PredefinedHabitViewer,
    HabitRemover,
    get_habit_names
)

DB_FILE = "files/data.db"
PRESET_DB_FILE = "files/predefined-habits.db"


def run_cli():
    """
    Main entry point for the Habit Tracker CLI.
    """
    print("🌟 Welcome to your Habit Tracker! 🌟\n")

    # Instantiate helpers
    creator = HabitCreator()
    analyzer = HabitAnalyzer()
    presets = PredefinedHabitViewer()
    remover = HabitRemover()

    while True:
        try:
            habits_list = get_habit_names(DB_FILE)
        except (sqlite3.OperationalError, ValueError):
            habits_list = []


        action = questionary.select(
            "Choose an action:",
            choices=[
                " ➕  Create a habit",
                " ✏️ Modify habit details",
                " 📊 View Reports",
                " ✅  Check-off",
                " 🗑️Remove a habit",
                " 📂 View predefined habits",
                " 🚪 Exit"
            ]
        ).ask()

        # Adding a habit
        if action == " ➕  Create a habit":
            habit_name = questionary.text("Habit name:").ask().strip().lower()
            category = questionary.select(
                "Category:",
                choices=["study", "hobby", "health", "sport"]).ask()

            frequency = questionary.select(
                "Frequency:",
                choices=["daily", "weekly"]).ask()

            # unit = days or weeks
            if frequency == "daily":
                unit = "days"
            else:
                unit = "weeks"


            while True:
                number = questionary.text(f"How many {unit}?").ask()
                if number.isdigit():
                    duration = f"{number} {unit}"
                    break
                print("❌ Please enter a valid number.")

            creator.add_habit(habit_name, category, frequency, duration, DB_FILE)


        # Editing habits
        elif action == " ✏️ Modify habit details":
            if not habits_list:
                print("⚠️ No habits available to edit.\n")
                continue

            target = questionary.select("Select a habit:", choices=habits_list).ask()

            field = questionary.select(
                "What do you want to edit?",
                choices=["name", "category", "frequency", "duration"]).ask()

            new_value = questionary.text(f"Enter new {field}:").ask().strip().lower()

            editor = HabitEditor(target, field, new_value)
            editor.apply(DB_FILE)

            print(f"✏️ Habit '{target}' updated!\n")

        # viewing Reports
        elif action == " 📊 View Reports":
            if not habits_list:
                print("⚠️ No habits available. Add one first.\n")
                continue

            report_type = questionary.select(
                "Report type:",
                choices=[
                    "all habits",
                    "all daily habits",
                    "all weekly habits",
                    "one habit",
                    "longest streak (all habits)",
                    "longest streak (one habit)"
                ]).ask()

            analyzer.generate_report(report_type, DB_FILE)

            print("")

        # Check-off when done
        elif action == " ✅  Check-off":
            if not habits_list:
                print("⚠️ No habits available. Add one first.\n")
                continue

            habit_name = questionary.select("Mark which habit as done?", choices=habits_list).ask()
            analyzer.mark_done(habit_name, DB_FILE)

            print("")

        # Predefined habits
        elif action == " 📂 View predefined habits":
            presets.show_all(PRESET_DB_FILE)
            print("")

        # Removing a habit
        elif action == " 🗑️Remove a habit":
            if not habits_list:
                print("⚠️ No habits available to delete.\n")
                continue

            target = questionary.select("Select a habit to delete:", choices=habits_list).ask()
            remover.remove(target, DB_FILE)

            print(f"🗑️ Habit '{target}' removed!\n")

        # Exit
        elif action == " 🚪 Exit":
            print("👋 Thanks for using Habit Tracker. Goodbye!\n")
            break


if __name__ == "__main__":
    run_cli()

