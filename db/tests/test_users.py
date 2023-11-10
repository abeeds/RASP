import db.users as usrs


def test_get_users():
    users = usrs.get_users()
    assert isinstance(users, dict)


def test_get_unread_from():
    messages = usrs.get_unread_from(usrs.TEST_USER)
    assert isinstance(messages, dict)
