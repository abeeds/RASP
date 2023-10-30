import db.db_test as db_test


def test_fetch_pets():
    pets = db_test.fetch_pets()
    assert isinstance(pets, dict)
    assert len(pets) > 0
