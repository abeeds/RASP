from .db_connect import insert_one, connect_db
from .db_connect import fetch_one, del_one
from .db_connect import update_one

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


def deactivate(username: str):
    if user_exists(username):
        return del_one(USER_COLLECT, {"Username": username})
    else:
        raise ValueError(f'Deactivation failed: {username} does not exist')


def update_username(old_name, new_name):
    filter = {"Username": old_name}
    new_vals = {"$set": {'Username': new_name}}

    result = update_one(USER_COLLECT, filter, new_vals)

    if result > 0:
        print(f"Username updated successfully: {old_name} -> {new_name}")
    else:
        print(f"Username '{old_name}' not found.")
