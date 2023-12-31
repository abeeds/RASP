import pytest

import db.users as usrs


@pytest.fixture(scope='function')
def temp_user():
    name = usrs._get_test_name()
    usrs.add_user(name)
    yield name
    if usrs.exists(name):
        usrs.del_user(name)


@pytest.mark.skip('parent file defunct')
def test_get_test_name():
    name = usrs._get_test_name()
    assert isinstance(name, str)
    assert len(name) > 0


@pytest.mark.skip('parent file defunct')
def test_gen_id():
    _id = usrs._gen_id()
    assert isinstance(_id, str)
    assert len(_id) == usrs.ID_LEN


@pytest.mark.skip('parent file defunct')
def test_get_test_user():
    assert isinstance(usrs.get_test_user(), dict)


@pytest.mark.skip('parent file defunct')
def test_get_users(temp_user):
    users = usrs.get_users()
    assert isinstance(users, dict)
    if len(users) > 0:
        for user in users:
            assert isinstance(user, str)


@pytest.mark.skip('parent file defunct')
def test_get_unread_from():
    messages = usrs.get_unread_from(usrs.TEST_USER)
    assert isinstance(messages, dict)


@pytest.mark.skip('parent file defunct')
def test_add_user_blank_name():
    with pytest.raises(ValueError):
        usrs.add_user('')


ADD_NAME = "First Last"


@pytest.mark.skip('parent file defunct')
def test_add_user():
    usrs.add_user(ADD_NAME)
    assert usrs.exists(ADD_NAME)


@pytest.mark.skip('parent file defunct')
def test_del_user(temp_user):
    name = temp_user
    usrs.del_user(name)
    assert not usrs.exists(name)


@pytest.mark.skip('parent file defunct')
def test_del_nonexistent_user():
    name = frozenset(usrs.get_test_user())
    with pytest.raises(ValueError):
        usrs.del_user(name)
