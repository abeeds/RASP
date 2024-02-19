from .db_connect import insert_one, connect_db
from .db_connect import fetch_one, del_one
from .db_connect import update_one, fetch_all

USER_COLLECT = "users"

# User fields
USERNAME = "username"
PASSWORD = "password"


def user_exists(username: str):
    connect_db()
    return fetch_one(USER_COLLECT, {USERNAME: username})


def userpass_check(username: str, password: str):
    connect_db()
    return fetch_one(USER_COLLECT, {USERNAME: username, PASSWORD: password})


def insert_user(username: str, password: str):
    user = {}
    user[USERNAME] = username
    user[PASSWORD] = password

    connect_db()
    _id = insert_one(USER_COLLECT, user)
    return _id


def deactivate(username: str):
    connect_db()
    if user_exists(username):
        del_one(USER_COLLECT, {USERNAME: username})


def update_username(old_name: str, new_name: str):
    filter = {USERNAME: old_name}
    new_vals = {"$set": {USERNAME: new_name}}

    connect_db()
    update_one(USER_COLLECT, filter, new_vals)


def update_password(username: str, new_pw: str):
    filter = {USERNAME: username}
    new_vals = {"$set": {PASSWORD: new_pw}}

    connect_db()
    update_one(USER_COLLECT, filter, new_vals)


def get_users():
    connect_db()
    users_data = fetch_all(USER_COLLECT)

    # Create a dictionary with usernames as keys and user details as values
    users_dict = {user[USERNAME]: {"_id": str(user["_id"])}
                  for user in users_data}

    return users_dict
