import pytest
import db.db_users as dbu

TEST_USERNAME = "test"
TEST_PASSWORD = "testpw"
TEST_NEWPW = "updatedpw"


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
    dbu.update_password(TEST_USERNAME, TEST_NEWPW)
    user = dbu.user_exists(TEST_USERNAME)

    assert user is not None
    assert user["Password"] != TEST_PASSWORD
    assert user["Password"] == TEST_NEWPW


def test_deactivate():
    dbu.deactivate(TEST_USERNAME)
    assert not dbu.user_exists(TEST_USERNAME)
