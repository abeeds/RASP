import pytest
import db.db_users as dbu

TEST_USERNAME = "test"
NEW_USERNAME = "anothertest"
TEST_PASSWORD = "testpw"
NEW_PASSWORD = "updatedpw"


@pytest.fixture(scope='function')
def temp_user():
    dbu.insert_user(TEST_USERNAME, TEST_PASSWORD)

    yield TEST_USERNAME

    if dbu.user_exists(TEST_USERNAME):
        dbu.deactivate(TEST_USERNAME)


def test_insert_user():
    dbu.insert_user(TEST_USERNAME, TEST_PASSWORD)
    assert dbu.user_exists(TEST_USERNAME)


def test_update_password():
    dbu.update_password(TEST_USERNAME, NEW_PASSWORD)
    user = dbu.user_exists(TEST_USERNAME)

    assert user is not None
    assert user[dbu.PASSWORD] != TEST_PASSWORD
    assert user[dbu.PASSWORD] == NEW_PASSWORD


def test_update_username():
    dbu.update_username(TEST_USERNAME, NEW_USERNAME)
    user = dbu.user_exists(NEW_USERNAME)

    assert user is not None
    assert user[dbu.USERNAME] != TEST_USERNAME
    assert user[dbu.USERNAME] == NEW_USERNAME


def test_deactivate():
    dbu.deactivate(NEW_USERNAME)
    assert not dbu.user_exists(NEW_USERNAME)
