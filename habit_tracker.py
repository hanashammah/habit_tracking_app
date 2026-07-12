import datetime
import questionary
import sqlite3
from db import connect_db, insert_habit, fetch_habits


class PredefinedHabitViewer:
    """
    View all predefined habits from the database.
    """

    def show_all(self, db_path):
        """
        Print all predefined habits.
        Parameters:
        db_path: database file path
        """
        with connect_db(db_path) as db:
            print(fetch_habits(db))

def get_habit_names(db_path):
    """
    Get a list of all habit names in the database.

    db_path: path to the database file

    Returns: list of habit names
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM habit_data")
        records_1 = cursor.fetchall()
        names = [row[0] for row in records_1]
    return names


class HabitCreator:
    """
    Create new habits and add them to the database.
    """

    def add_habit(self, name, category, frequency, duration, db_path):
        """
        Add a new habit with default tracking fields.

        Parameters:
        name: Name of the habit.
        category: Category of the habit (e.g., 'study', 'health', 'hobby', 'sport').
        frequency: Frequency of the habit ('daily' or 'weekly').
        duration: Duration of the habit (e.g., '5 days', '3 weeks').
        db_path: Path to the SQLite database file.
        """
        start_day = datetime.datetime.now().strftime("%Y/%m/%d")
        with connect_db(db_path) as db:
            # ✅ Check if a habit with the same name already exists
            existing = db.execute(
                "SELECT COUNT(*) FROM habit_data WHERE name = ?", (name,)
            ).fetchone()[0]

            if existing > 0:
                print(f" Habit '{name}' already exists. Please choose a different name.\n")
                return

            insert_habit(
                db,
                name=name,
                category=category,
                frequency=frequency,
                duration=duration,
                start_day=start_day,
                marked_off=0,
                last_completed_day="-",
                streak=0,
                longest_streak=0
            )
            print(f" Habit '{name}' created successfully!\n")

class HabitEditor:
    """
    Edit a habit's properties (name, category, frequency, duration).
    """

    def __init__(self, habit_name, field, new_value):
        """
        habit_name: the habit to edit
        field: which field to change
        new_value: the new value to set
        """
        self.habit_name = habit_name
        self.field = field
        self.new_value = new_value

    def apply(self, db_path):
        """
        Apply the planned edit to a habit in the database.

        Parameters:
        db_path (str): Path to the SQLite database file.
        """
        with connect_db(db_path) as db:
            db.execute(
                f"UPDATE habit_data SET {self.field} = ? WHERE name = ?",
                (self.new_value, self.habit_name)
            )
            db.commit()


class HabitAnalyzer:
    """
    Mark habits as done, update streaks, and generate reports.
    """
    def mark_done(self, habit_name, db_path):
        """
        Mark a habit as completed for day/week.

        Parameters:
            habit_name (str): The name of the habit to mark as done.
            db_path (str): Path to the SQLite database file.
        """
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT marked_off, frequency, last_completed_day, streak, longest_streak_days "
                "FROM habit_data WHERE name = ?", (habit_name,)
            )
            data = cursor.fetchone()
            if not data:
                return  # habit does not exist
            marked_off, frequency, last_day, streak, longest = data

            today = datetime.datetime.now().strftime("%Y/%m/%d")

            # Determine the day/week to compare for streaks
            if frequency == "daily":
                compare_day = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y/%m/%d")
                current_period = today
            else:  # weekly
                week_start = datetime.datetime.now() - datetime.timedelta(days=datetime.datetime.now().weekday())
                current_period = week_start.strftime("%Y/%m/%d")
                last_week_start = datetime.datetime.strptime(last_day, "%Y/%m/%d") if last_day != "-" else None
                compare_day = (week_start - datetime.timedelta(weeks=1)).strftime("%Y/%m/%d")

            # Only update if not already marked today/week
            if last_day != current_period:
                # update streak
                if last_day == compare_day:
                    streak += 1
                else:
                    streak = 1

                longest = max(longest, streak)

                # update database
                cursor.execute(
                    "UPDATE habit_data SET marked_off = ?, last_completed_day = ?, streak = ?, longest_streak_days = ? "
                    "WHERE name = ?",
                    (marked_off + 1, current_period, streak, longest, habit_name)
                )
                conn.commit()

    def report_all_habits(self, db):
        """Display all habits."""
        print(fetch_habits(db))

    def report_daily_habits(self, db):
        """Display all daily habits."""
        print(fetch_habits(db, filter_by="frequency", match_value="daily"))

    def report_weekly_habits(self, db):
        """Display all weekly habits."""
        print(fetch_habits(db, filter_by="frequency", match_value="weekly"))

    def report_one_habit(self, db, db_path):
        """
        Display information for one selected habit.

        Parameters:
            db: Active database connection.
            db_path (str): Path to the database.
        """
        name = questionary.select(
            "Which habit to report?",
            choices=get_habit_names(db_path)
        ).ask()

        print(fetch_habits(db, filter_by="name", match_value=name))

    def report_longest_streak(self, db):
        """Display the habit with the longest recorded streak."""

        result = db.execute(
            """
            SELECT name, longest_streak_days, frequency
            FROM habit_data
            ORDER BY longest_streak_days DESC
            LIMIT 1
            """
        ).fetchone()

        if result:
            name, longest_streak, frequency = result

            unit = "days" if frequency == "daily" else "weeks"

            print(
                f"🏆 Longest streak overall: "
                f"{name} ({longest_streak} {unit})"
            )

    def report_longest_streak_one_habit(self, db, db_path):
        """
        Display the longest streak for one selected habit.

        Parameters:
            db: Active database connection.
            db_path (str): Path to the database.
        """

        name = questionary.select(
            "Which habit to check?",
            choices=get_habit_names(db_path)
        ).ask()

        result = db.execute(
            """
            SELECT longest_streak_days, frequency
            FROM habit_data
            WHERE name = ?
            """,
            (name,),
        ).fetchone()

        if result:
            longest_streak, frequency = result

            unit = "days" if frequency == "daily" else "weeks"

            print(
                f"🔥 Longest streak for {name}: "
                f"{longest_streak} {unit}"
            )


    def generate_report(self, report_type, db_path):
        """
        Generate a report based on the selected report type.

        Parameters:
            report_type (str): The type of report to display.
            db_path (str): Path to the SQLite database file.
        """

        with connect_db(db_path) as db:

            if report_type == "all habits":
                self.report_all_habits(db)

            elif report_type == "all daily habits":
                self.report_daily_habits(db)

            elif report_type == "all weekly habits":
                self.report_weekly_habits(db)

            elif report_type == "one habit":
                self.report_one_habit(db, db_path)

            elif report_type == "longest streak (all habits)":
                self.report_longest_streak(db)

            elif report_type == "longest streak (one habit)":
                self.report_longest_streak_one_habit(db, db_path)


class HabitRemover:
    """
    Delete a habit from the database.
    """

    def remove(self, habit_name, db_path):
        """
        Delete a habit by name.

        Parameters:
        habit_name: the habit to delete
        db_path: database file path
        """
        with sqlite3.connect(db_path) as conn:
            conn.execute("DELETE FROM habit_data WHERE name = ?", (habit_name,))
            conn.commit()
