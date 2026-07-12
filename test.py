import pytest
from habit_tracker import HabitCreator, HabitEditor, HabitAnalyzer, HabitRemover
from db import connect_db, insert_habit

@pytest.fixture
def test_db(tmp_path):
    """
    Provides a fresh database file for each test in a temporary directory.
    Ensures Windows file-lock issues are avoided.
    """
    db_file = tmp_path / "test.db"
    with connect_db(db_file) as db:
        # Insert two baseline habits
        insert_habit(
            db, name="programming", category="study", frequency="daily",
            duration="5 days", start_day="2025/09/09", marked_off=0,
            last_completed_day="-", streak=0, longest_streak=0
        )
        insert_habit(
            db, name="running", category="health", frequency="weekly",
            duration="3 weeks", start_day="2025/09/09", marked_off=0,
            last_completed_day="-", streak=0, longest_streak=0
        )
    return db_file


def test_add_new_habit(test_db):
    """Test adding a new habit to the database."""
    habit = HabitCreator()
    habit.add_habit("no-coffee", "health", "daily", "2 weeks", test_db)

    with connect_db(test_db) as db:
        result = db.execute("SELECT name FROM habit_data WHERE name='no-coffee'").fetchone()
    assert result is not None


def test_edit_habit(test_db):
    """Test editing an existing habit's duration."""
    habit = HabitEditor(habit_name="programming", field="duration", new_value="6 weeks")
    habit.apply(test_db)

    with connect_db(test_db) as db:
        result = db.execute("SELECT duration FROM habit_data WHERE name='programming'").fetchone()[0]
    assert result == "6 weeks"


def test_analyse_habit_check_off(test_db):
    """Test marking a habit as done increments the marked_off counter."""
    habit = HabitAnalyzer()
    habit.mark_done("programming", test_db)

    with connect_db(test_db) as db:
        result = db.execute("SELECT marked_off FROM habit_data WHERE name='programming'").fetchone()[0]
    assert result == 1


def test_analyse_habit_streak(test_db):
    """Test streak increment logic for consecutive habit completions."""
    habit = HabitAnalyzer()
    habit.mark_done("programming", test_db)
    habit.mark_done("programming", test_db)

    with connect_db(test_db) as db:
        streak, longest = db.execute(
            "SELECT streak, longest_streak_days FROM habit_data WHERE name='programming'"
        ).fetchone()
    assert streak >= 1
    assert longest >= streak


def test_analyse_report_all(capsys, test_db):
    """Test reporting all habits displays all baseline habits."""
    habit = HabitAnalyzer()
    habit.generate_report(report_type="all habits", db_path=test_db)

    captured = capsys.readouterr()
    assert "programming" in captured.out
    assert "running" in captured.out


def test_analyse_report_daily(capsys, test_db):
    """Test reporting all daily habits only shows daily habits."""
    habit = HabitAnalyzer()
    habit.generate_report(report_type="all daily habits", db_path=test_db)

    captured = capsys.readouterr()
    assert "programming" in captured.out
    assert "running" not in captured.out


def test_analyse_report_weekly(capsys, test_db):
    """Test reporting all weekly habits only shows weekly habits."""
    habit = HabitAnalyzer()
    habit.generate_report(report_type="all weekly habits", db_path=test_db)

    captured = capsys.readouterr()
    assert "running" in captured.out
    assert "programming" not in captured.out


def test_delete_habit(test_db):
    """Test deleting an existing habit removes it from the database."""
    habit = HabitRemover()
    habit.remove("running", test_db)

    with connect_db(test_db) as db:
        result = db.execute("SELECT name FROM habit_data WHERE name='running'").fetchone()
    assert result is None


def test_delete_nonexistent_habit(test_db):
    """Deleting a habit that does not exist should not raise an error."""
    habit = HabitRemover()
    habit.remove("nonexistent", test_db)

    with connect_db(test_db) as db:
        all_habits = db.execute("SELECT name FROM habit_data").fetchall()
    assert len(all_habits) == 2


def test_edit_nonexistent_habit(test_db):
    """Editing a habit that does not exist should not change the database."""
    habit = HabitEditor(habit_name="ghost", field="duration", new_value="10 days")
    habit.apply(test_db)

    with connect_db(test_db) as db:
        result = db.execute("SELECT duration FROM habit_data WHERE name='ghost'").fetchone()
    assert result is None


def test_add_duplicate_habit(test_db):
    """Adding a habit that already exists should not break the database."""
    habit = HabitCreator()
    habit.add_habit("programming", "study", "daily", "5 days", test_db)

    with connect_db(test_db) as db:
        results = db.execute("SELECT name FROM habit_data WHERE name='programming'").fetchall()
    assert len(results) == 1   # Because duplicates are not allowed
