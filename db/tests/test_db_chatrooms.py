import pytest
import db.db_chatrooms as dbch

TEST_CHATROOM = "room"
TEST_DESC = "A place to hang out."
TEST_NEW_DESC = "A fun place to hang out."
TEST_OWNER = "King Lizard"


@pytest.fixture(scope='function')
def temp_chatroom():
    dbch.insert_chatroom(TEST_CHATROOM, TEST_DESC)

    yield TEST_CHATROOM

    if dbch.room_exists(TEST_CHATROOM):
        dbch.delete_chatroom(TEST_CHATROOM)


def test_insert_chatroom():
    dbch.insert_chatroom(TEST_CHATROOM, TEST_DESC, TEST_OWNER)
    assert dbch.room_exists(TEST_CHATROOM)


def test_update_desc():
    dbch.update_description(TEST_CHATROOM, TEST_NEW_DESC)
    room = dbch.room_exists(TEST_CHATROOM)

    assert room is not None
    assert room[dbch.DESC] == TEST_NEW_DESC


def test_delete_chatroom():
    dbch.delete_chatroom(TEST_CHATROOM)
    assert not dbch.room_exists(TEST_CHATROOM)
