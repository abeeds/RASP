import pytest
import db.db_users as dbu

TEST_USERNAME = "test"
NEW_USERNAME = "anothertest"
TEST_PASSWORD = "testpw"
FALSE_PASSWORD = "29318092381"
NEW_PASSWORD = "updatedpw"


@pytest.fixture(scope='function')
def temp_user():
    dbu.insert_user(TEST_USERNAME, TEST_PASSWORD)

    yield TEST_USERNAME

    if dbu.user_exists(TEST_USERNAME):
        dbu.deactivate(TEST_USERNAME)


def test_userpass_check(temp_user):
    response = dbu.userpass_check(TEST_USERNAME, TEST_PASSWORD)
    assert response is not None


def test_false_userpass_check():
    response = dbu.userpass_check(TEST_USERNAME, FALSE_PASSWORD)
    assert response is None


def test_insert_user():
    dbu.insert_user(TEST_USERNAME, TEST_PASSWORD)
    assert dbu.user_exists(TEST_USERNAME)


def test_update_password():
    dbu.update_password(TEST_USERNAME, NEW_PASSWORD)
    user = dbu.user_exists(TEST_USERNAME)

    assert user is not None
    assert dbu.userpass_check(TEST_USERNAME, NEW_PASSWORD) is not None


def test_update_username():
    dbu.update_username(TEST_USERNAME, NEW_USERNAME)
    user = dbu.user_exists(NEW_USERNAME)

    assert user is not None
    assert user[dbu.USERNAME] == NEW_USERNAME


def test_deactivate():
    dbu.deactivate(NEW_USERNAME)
    assert not dbu.user_exists(NEW_USERNAME)
