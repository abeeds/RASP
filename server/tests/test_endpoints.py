from http.client import OK

from unittest.mock import patch

import pytest

import db.db_users as dbu
import db.db_chatrooms as dbch
import db.db_messages as dbm

import server.endpoints as ep

TEST_CLIENT = ep.app.test_client()

ID_LEN = 24
MOCK_ID = '0' * ID_LEN
TESTROOM = 'dev chatroom'
TESTDESC = 'this description has been updated'
TESTOWNER = 'King Lizard'
TESTUSER = 'dev user'
TESTPASS = 'password'
TESTCONTENT = 'lorem ipsum dolor sit amet'
TESTUPDATEDCONTENT = 'heehee'


@pytest.fixture(scope='function')
def temp_chatroom():
    dbch.insert_chatroom(TESTROOM)
    yield TESTROOM
    dbch.delete_chatroom(TESTROOM)


@pytest.fixture(scope='function')
def temp_user():
    dbu.insert_user(TESTUSER, TESTPASS)
    yield TESTUSER
    dbu.deactivate(TESTUSER)


@pytest.fixture(scope='function')
def temp_msg():
    temp_id = dbm.insert_message(TESTUSER, TESTROOM, TESTCONTENT)
    yield TESTUSER
    dbm.delete_message(temp_id[0])


def test_hello():
    resp = TEST_CLIENT.get(ep.HELLO_EP)
    print(f'{resp=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    assert ep.HELLO_RESP in resp_json


def test_get_endpoints():
    resp = TEST_CLIENT.get(ep.ENDPOINTS_EP)
    resp_json = resp.get_json()
    assert "Available endpoints" in resp_json
    assert isinstance(resp_json, dict)


def test_get_users(temp_user):
    resp = TEST_CLIENT.get(ep.GET_USERS_URL)
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert TESTUSER in resp_json


def test_get_chatrooms(temp_chatroom):
    resp = TEST_CLIENT.get(ep.CHATROOMS_URL)
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert TESTROOM in resp_json


def test_get_messages(temp_chatroom, temp_user, temp_msg):
    resp = TEST_CLIENT.post(
        f'{ep.MSG_URL}/{TESTROOM}/{TESTUSER}/tstcontent')
    resp = TEST_CLIENT.get(f'{ep.MSG_URL}/{TESTROOM}')
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)


@patch('db.db_users.ban', autospec=True)
@patch('db.db_users.user_exists', autospec=True)
def test_deactivate(mock_del, mock_user):
    resp = TEST_CLIENT.delete(f'{ep.DEACTIVATE_URL}/tstusrname')
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert 'message' in resp_json


@patch('db.db_chatrooms.insert_chatroom', autospec=True)
def test_insert_chatroom(mock_add):
    resp = TEST_CLIENT.post(f'{ep.CHATROOMS_URL}', json={
            dbch.NAME: TESTROOM,
            dbch.DESC: TESTDESC,
            dbch.OWNER: TESTOWNER,
        })
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert "status" in resp_json


@patch('db.db_users.insert_user', autospec=True)
def test_register(mock_add):
    resp = TEST_CLIENT.post(f'{ep.REGISTER_URL}/tstusrname/tstpass')
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert "message" in resp_json


def test_write_msg(temp_chatroom, temp_user, temp_msg):
    resp = TEST_CLIENT.post(f'{ep.MSG_URL}', json={
        dbm.USERNAME: TESTUSER,
        dbm.CHATROOM: TESTROOM,
        dbm.CONTENT: TESTCONTENT
        })
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert "Status" in resp_json


@patch('db.db_messages.message_exists', autospec=True)
@patch('db.db_messages.edit_message', autospec=True)
def test_edit_msg(mock_msg, mock_update):
    resp = TEST_CLIENT.put(f'{ep.MSG_URL}', json={
        dbm.ID: MOCK_ID,
        dbm.CONTENT: TESTUPDATEDCONTENT
    })
    assert resp.status_code == OK


@pytest.mark.skip("REWRITE")
@patch('db.db_chatrooms.delete_chatroom', autospec=True)
def test_delete_chatroom(mock_del):
    resp = TEST_CLIENT.delete(f'{ep.CHATROOMS_URL}/testroomname')
    resp_json = resp.get_json()
    assert "Chatroom Deleted" in resp_json
    assert resp.status_code == OK
    assert dbch.room_exists(TESTROOM) is None


@pytest.mark.skip("REWRITE")
@patch('db.db_messages.delete_message', autospec=True)
def test_delete_msg(mock_del):
    resp = TEST_CLIENT.delete(f'{ep.MSG_URL}/{MOCK_ID}')
    assert resp.status_code == OK
    assert dbm.message_exists(MOCK_ID) is None


@pytest.mark.skip("REWRITE")
@patch('db.db_chatrooms.update_description', autospec=True)
def test_update_chatroom_desc(mock_update):
    resp = TEST_CLIENT.put(f'{ep.CHATROOMS_URL}', json={
        dbch.NAME: TESTROOM,
        dbch.DESC: TESTDESC
    })
    assert resp.status_code == OK


@patch('db.db_users.update_password', autospec=True)
def test_update_password(mock_update):
    username = 'anyuser'
    password = 'anypass'
    dbu.insert_user(username, password)

    resp = TEST_CLIENT.put(f'{ep.UPDATE_PASS_URL}/{username}/{password}')
    assert resp.status_code == OK

    dbu.deactivate(username)


@pytest.mark.skip("REWRITE")
@patch('db.db_users.update_username', autospec=True)
def test_update_username(mock_update):
    username = 'anyuser'
    replacement = 'anynewuser'

    resp = TEST_CLIENT.put(f'{ep.UPDATE_USER_URL}/{username}/{replacement}')
    assert resp.status_code == OK


def test_login(temp_user):
    resp = TEST_CLIENT.get(f'{ep.LOGIN_URL}/{TESTUSER}/{TESTPASS}')
    resp_json = resp.get_json()
    assert resp_json['message'] == "true"


@pytest.mark.skip("NEEDS TEST")
def test_wipe():
    pass
