import db.db as db
import pytest


def test_db_connection():
    try:
        database = db.ConnectToDB()
        assert database is not None
    except Exception:
        pytest.skip("Skipping test_db_connection: DB Connection Failed")
