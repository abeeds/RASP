import pytest

import db.users as usrs


@pytest.fixture(scope='function')
def temp_user():
    name = usrs._get_test_name()
    usrs.add_user(name)
    yield name
    if usrs.exists(name):
        usrs.del_user(name)


def test_get_test_name():
    name = usrs._get_test_name()
    assert isinstance(name, str)
    assert len(name) > 0


def test_gen_id():
    _id = usrs._gen_id()
    assert isinstance(_id, str)
    assert len(_id) == usrs.ID_LEN


def test_get_test_user():
    assert isinstance(usrs.get_test_user(), dict)


def test_get_users(temp_user):
    users = usrs.get_users()
    assert isinstance(users, dict)
    assert len(users) > 0
    for user in users:
        assert isinstance(user, str)
    assert usrs.exists(temp_user)


def test_get_unread_from():
    messages = usrs.get_unread_from(usrs.TEST_USER)
    assert isinstance(messages, dict)


def test_add_user_blank_name():
    with pytest.raises(ValueError):
        usrs.add_user('')


ADD_NAME = "First Last"


def test_add_user():
    usrs.add_user(ADD_NAME)
    assert usrs.exists(ADD_NAME)


def test_del_user(temp_user):
    name = temp_user
    usrs.del_user(name)
    assert not usrs.exists(name)


def test_del_nonexistent_user():
    name = frozenset(usrs.get_test_user())
    with pytest.raises(ValueError):
        usrs.del_user(name)
