import pytest

import db.users as usrs


def test_get_users():
    users = usrs.get_users()
    assert isinstance(users, dict)
