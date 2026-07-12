import sqlite3
from tabulate import tabulate


def connect_db(file_path: str) -> sqlite3.Connection:
    """
    Open a connection to an SQLite database, creating the database and
    the required tables if they do not already exist.

    Parameters:
        file_path (str): The path to the SQLite database file.
                         If the file does not exist, it will be created.

    """
    connection = sqlite3.connect(file_path)
    create_tables(connection)
    return connection


def create_tables(connection: sqlite3.Connection) -> None:
    """
    Ensure that the database schema for habit tracking exists.

    Parameters:
        connection (sqlite3.Connection): An active SQLite connection
                                         where the table should be created.
    """
    query = """
        CREATE TABLE IF NOT EXISTS habit_data (
            name TEXT NOT NULL,
            category TEXT,
            frequency TEXT,
            duration TEXT NOT NULL,
            start_day TEXT NOT NULL,
            marked_off INTEGER,
            last_completed_day TEXT NOT NULL,
            streak INTEGER,
            longest_streak_days INTEGER
        )
    """
    connection.execute(query)
    connection.commit()


def insert_habit(connection: sqlite3.Connection, *, name: str, category: str,
                 frequency: str, duration: str, start_day: str,
                 marked_off: int, last_completed_day: str,
                 streak: int, longest_streak: int) -> None:
    """
    Add a new habit entry into the database.

    Parameters:
        connection (sqlite3.Connection): An active SQLite connection to the database.
        name (str): Name of the habit.
        category (str): Category of the habit (e.g., study, health, hobby, sport).
        frequency (str): Habit frequency, either 'daily' or 'weekly'.
        duration (str): Duration of the habit.
        start_day (str): Start date of the habit in YYYY/MM/DD format.
        marked_off (int): Number of times the habit has been completed.
        last_completed_day (str): The date the habit was last completed.
        streak (int): Current consecutive periods the habit has been completed.
        longest_streak (int): Longest consecutive completion streak recorded.
    """
    query = """
        INSERT INTO habit_data (
            name, category, frequency, duration, start_day,
            marked_off, last_completed_day, streak, longest_streak_days
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    connection.execute(query, (
        name, category, frequency, duration, start_day,
        marked_off, last_completed_day, streak, longest_streak
    ))
    connection.commit()


def fetch_habits(connection: sqlite3.Connection,
                 filter_by: str | None = None,
                 match_value: str | None = None) -> str:
    """
    Get all habits or a filtered subset and return them as a formatted table.
    Parameters:
        connection (sqlite3.Connection): An active SQLite connection to the database.
        filter_by: Column name to filter by (e.g., 'frequency', 'category').
                   If None, all habits are returned. Defaults to None.
        match_value: The value to match in the specified column.
                    Ignored if filter_by is None. Defaults to None.
    """
    cursor = connection.cursor()

    if filter_by is None:
        cursor.execute("SELECT * FROM habit_data")
        connection.commit()
    else:
        cursor.execute(f"SELECT * FROM habit_data WHERE {filter_by} = ?", (match_value,))
        connection.commit()

    records = cursor.fetchall()

    headers = [
        "Name", "Category", "Frequency", "Duration",
        "Start Day", "Marked Off", "Last Completed Day",
        "Streak", "Longest Streak"
    ]
    table_data = [list(row) for row in records]
    table_data.insert(0, headers)

    return tabulate(table_data, headers="firstrow", tablefmt="fancy_grid")


