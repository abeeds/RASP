import db.users as usrs


def test_get_users():
    users = usrs.get_users()
    assert isinstance(users, dict)
    assert len(users) > 0
    for user in users:
        assert isinstance(user, str)


def test_get_unread_from():
    messages = usrs.get_unread_from(usrs.TEST_USER)
    assert isinstance(messages, dict)


def test_add_user_blank_name():
    with pytest.raises(ValueError):
        usrs.add_user('')


ADD_NAME = "First Last"


def test_add_user():
    usrs.add_user(ADD_NAME)
    assert ADD_NAME in usrs.get_users()
