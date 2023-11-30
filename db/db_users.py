from .db_connect import insert_one, connect_db
from .db_connect import fetch_one

USER_COLLECT = "users"


def user_exists(username: str):
    connect_db()
    return fetch_one(USER_COLLECT, {"Username": username})


def insert_user(username: str, password: str):
    if user_exists(username):
        raise ValueError(f'Username already exists: {username}')
    if not username:
        raise ValueError('Username cannot be blank')

    user = {}
    user["Username"] = username
    user["password"] = password

    connect_db()
    _id = insert_one(USER_COLLECT, user)
    return _id is not None
