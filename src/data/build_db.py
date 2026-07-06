import sqlite3
import pandas as pd

class Table:
    """Base class for all the SQL tables. Handles the extraction, loading & renaming"""
    RAW_COLS = []
    CLEAN_COLS = []
    DEDUP_KEY = None
    DROPNA_COL = None
    TABLE_NAME = ""

    def __init__(self, df, conn):
        self.conn = conn
        self.data = self._extract(df)
        self._load()

    def _extract(self, df):
        result = df[self.RAW_COLS].copy()
        result.columns = self.CLEAN_COLS
        if self.DEDUP_KEY:
            result = result.drop_duplicates(subset=self.DEDUP_KEY)
        if self.DROPNA_COL:
            result = result.dropna(subset=self.DROPNA_COL)

        return result

    def _load(self):
        self.data.to_sql(self.TABLE_NAME, self.conn, if_exists='replace', index=False)
        print(f"Loaded {self.TABLE_NAME}, ({len(self.data)}) rows.")


class Students(Table):
    """Students Table. Holds information such as year, name, student id, etc."""
    TABLE_NAME = "students"
    RAW_COLS = [
        "year_of_study",
        "full_name",
        "student_id",
        "assignments_not_handed_in",
        "study_day",
        "days_spent_learning"
    ]


class Assignments(Table):
    """Assignments Table. Holds information such as assignment details."""
    TABLE_NAME = "assignments"
    RAW_COLS = [
        "assignment_id",
        "assignment_name",
        "module_name",
        "release_date",
        "due_date",
        "number_of_credits",
        "number_of_hours"
    ]

class apprenticeLog(Table):
    """Apprentice Log Table. Holds information such as apprentice log details."""
    TABLE_NAME = "apprentice_log"
    RAW_COLS = [
        "student_id",
        "assignment_id",
        "assignment_name",
        "module_name",
        "number_of_hours"
    ]


class DataBase:
    TABLES = []

    def __init__(self, db_path=":memory:"):
        self.conn = sqlite3.connect(db_path)

    def load(self, fpath):
        print("Loading data...")
        df = pd.read_csv(fpath) #   Subject to change
        for TableClass in self.TABLES:
            TableClass(df, self.conn)
        print("Done!")

    def query(self, sql_query):
        return pd.read_sql(sql_query, self.conn)

    def close(self):
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()