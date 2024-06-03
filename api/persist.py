import os
import sqlite3

DB_NAME = "test.db"
TABLE_NAME = "UserCode"


def persist(code: str, output: str):
    """
    Persists the given code and its output into the SQLite3 database
    """
    try:
        con = sqlite3.connect("test.db")
        cursor = con.cursor()
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} (id INTEGER, code TEXT, output TEXT, Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);"
        )
        cur.execute(
            f"INSERT INTO {TABLE_NAME} (code, output) VALUES({code}, {output});"
        )
    except e as Exception:
        raise Exception(e)
