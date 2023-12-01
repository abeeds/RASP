import pytest
import db.db_users as dbu

TEST_USERNAME = "test"
TEST_PASSWORD = "testpw"


@pytest.fixture(scope='function')
def temp_user():
    dbu.insert_user(TEST_USERNAME, TEST_PASSWORD)

    yield TEST_USERNAME

    if dbu.user_exists(TEST_USERNAME):
        dbu.deactivate(TEST_USERNAME)


def test_insert_user():
    dbu.insert_user(TEST_USERNAME, TEST_PASSWORD)
    assert dbu.user_exists(TEST_USERNAME)


def test_deactivate():
    dbu.deactivate(TEST_USERNAME)
    assert not dbu.user_exists(TEST_USERNAME)
