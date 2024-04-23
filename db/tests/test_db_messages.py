import pytest
import db.db_messages as dbm
import db.db_connect as dbc

TEST_USERNAME = "First Last"
TEST_CHATROOM = "test"
TEST_CONTENT = "Lorem ipsum dolor sit amet"
TEST_NEW_CONTENT = "NEW MSG"
TEST_ID = ""  # set later


@pytest.fixture(scope='function')
def temp_message():
    msgres = dbm.insert_message(TEST_USERNAME, TEST_CHATROOM, TEST_CONTENT)

    yield msgres[0]  # yields id

    if dbm.message_exists(msgres[0]):
        dbm.delete_message(msgres[0])


def test_insert_message():
    global TEST_ID

    TEST_ID = dbm.insert_message(TEST_USERNAME, TEST_CHATROOM, TEST_CONTENT)[0]
    assert dbm.message_exists(TEST_ID)


def test_edit_message():
    dbm.edit_message(TEST_ID)

    msg = dbm.message_exists(TEST_ID, TEST_NEW_CONTENT)
    assert msg[dbm.CONTENT] == TEST_NEW_CONTENT


def test_delete_message():
    global TEST_ID

    dbm.delete_message(TEST_ID)
    assert not dbm.message_exists(TEST_ID)
