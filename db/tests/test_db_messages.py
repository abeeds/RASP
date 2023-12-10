import pytest
import db.db_messages as dbm

TEST_USERNAME = "First Last"
TEST_CHATROOM = "test"
TEST_CONTENT = "Lorem ipsum dolor sit amet"


@pytest.fixture(scope='function')
def temp_message():
    msgres = dbm.insert_message(TEST_USERNAME, TEST_CHATROOM, TEST_CONTENT)

    yield msgres[0]  # yields id


def test_insert_message():
    msgres = dbm.insert_message(TEST_USERNAME, TEST_CHATROOM, TEST_CONTENT)
    assert dbm.message_exists(msgres[0])
