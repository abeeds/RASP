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


def test_get_endpoints():
    resp = TEST_CLIENT.get(ep.ENDPOINTS_EP)
    resp_json = resp.get_json()
    assert "Available endpoints" in resp_json
    assert isinstance(resp_json, dict)


def test_get_users():
    resp = TEST_CLIENT.get(ep.GET_USERS_URL)
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)


def test_get_chatrooms():
    resp = TEST_CLIENT.get(ep.GET_CHATROOMS_URL)
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)


def test_get_messages():
    resp = TEST_CLIENT.get(ep.GET_MSGS_URL)
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)

