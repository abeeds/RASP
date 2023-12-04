from http.client import OK, NOT_FOUND, FORBIDDEN, NOT_ACCEPTABLE, BAD_REQUEST

from unittest.mock import patch

import pytest

import db.users as usrs
import db.db_users as dbu

import server.endpoints as ep

TEST_CLIENT = ep.app.test_client()


def test_hello():
    resp = TEST_CLIENT.get(ep.HELLO_EP)
    print(f'{resp=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    assert ep.HELLO_RESP in resp_json


def test_list_users():
    resp = TEST_CLIENT.get(ep.USERS_EP)
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert ep.TITLE in resp_json
    assert ep.TYPE in resp_json
    assert ep.DATA in resp_json


@patch('db.db_users.insert_user', side_effect=ValueError(), autospec=True)
def test_users_bad_add(mock_add):
    resp = TEST_CLIENT.post(ep.USERS_EP, json=
        {"user": "test user", "pass":  "test pass"})
    assert resp.status_code == NOT_ACCEPTABLE


@patch('db.db_users.insert_user', return_value=usrs.MOCK_ID, autospec=True)
def test_users_add(mock_add):
    resp = TEST_CLIENT.post(ep.USERS_EP, json=
        {"username": "test username", "password": "test password"})
    assert resp.status_code == OK
