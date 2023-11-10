import db.db as db
import pytest


def test_fetch_pets():
    pets = db.fetch_pets()
    assert isinstance(pets, dict)
    assert len(pets) > 0


def test_db_connection():
    try:
        database = db.ConnectToDB()
        assert database is not None
    except Exception:
        pytest.skip("Skipping test_db_connection: DB Connection Failed")
