import db.db as db


def test_fetch_pets():
    pets = db.fetch_pets()
    assert isinstance(pets, dict)
    assert len(pets) > 0
