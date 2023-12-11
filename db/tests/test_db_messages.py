import pytest
import db.db_messages as dbm

TEST_USERNAME = "First Last"
TEST_CHATROOM = "test"
TEST_CONTENT = "Lorem ipsum dolor sit amet"
TEST_ID = ""  # set later


@pytest.fixture(scope='function')
def temp_message():
    msgres = dbm.insert_message(TEST_USERNAME, TEST_CHATROOM, TEST_CONTENT)

    yield msgres[0]  # yields id


def test_insert_message():
    global TEST_ID

    msgres = dbm.insert_message(TEST_USERNAME, TEST_CHATROOM, TEST_CONTENT)
    TEST_ID = msgres[0]
    assert dbm.message_exists(TEST_ID)


def test_delete_message():
    global TEST_ID

    dbm.delete_message(TEST_ID)
    assert not dbm.message_exists(TEST_ID)
