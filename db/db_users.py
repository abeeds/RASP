from .db_connect import insert_one, connect_db
from .db_connect import fetch_one, del_one
from .db_connect import update_doc, fetch_all
from .db_messages import del_msgs_from_user
import bcrypt
from datetime import datetime
import random

USER_COLLECT = "users"

# User fields
USERNAME = "username"
PASSWORD = "password"
ID = "_id"
MEMBERSHIP = "membership"
SPECIALCHARS = "!@#$%^&*()-=_+}{[]|;':,./<>?"


def user_exists(username: str):
    connect_db()
    return fetch_one(USER_COLLECT, {USERNAME: username})


def userpass_check(username: str, password: str):
    connect_db()
    user = fetch_one(USER_COLLECT, {USERNAME: username})

    # checks password with the hashed version in the database
    if (user is not None
        and bcrypt.checkpw(password.encode('utf-8'),
                           user[PASSWORD].encode('utf-8'))):
        return user
    return None


def insert_user(username: str, password: str):
    user = {}
    user[USERNAME] = username
    user[PASSWORD] = bcrypt.hashpw(password.encode('utf-8'),
                                   bcrypt.gensalt()).decode('utf-8')
    user[MEMBERSHIP] = []

    connect_db()
    _id = insert_one(USER_COLLECT, user)
    return _id


def deactivate(username: str):
    connect_db()
    if user_exists(username):
        del_one(USER_COLLECT, {USERNAME: username})


def ban(username: str):
    connect_db()
    if user_exists(username):
        del_one(USER_COLLECT, {USERNAME: username})
        del_msgs_from_user(username)


def update_username(old_name: str, new_name: str):
    filter = {USERNAME: old_name}
    new_vals = {USERNAME: new_name}

    connect_db()
    update_doc(USER_COLLECT, filter, new_vals)


def update_password(username: str, new_pw: str):
    filter = {USERNAME: username}
    hashed_pw = bcrypt.hashpw(new_pw.encode('utf-8'),
                              bcrypt.gensalt()).decode('utf-8')
    new_vals = {PASSWORD: hashed_pw}

    connect_db()
    update_doc(USER_COLLECT, filter, new_vals)


def get_users():
    connect_db()
    users_data = fetch_all(USER_COLLECT)

    # Create a dictionary with usernames as keys and user details as values
    users_dict = {}
    for user in users_data:
        user_name = user.get(USERNAME)
        user_membership = list(user.get(MEMBERSHIP, []))

        users_dict[user_name] = {USERNAME: user_name,
                                 MEMBERSHIP: user_membership}

    return users_dict


def create_login_token(username, password):
    user = userpass_check(username, password)
    if user is None:
        return None

    user_id = str(user[ID])
    time = str(datetime.now().timestamp())
    random_chars = ""
    rand_len = random.randrange(1, 5)
    for x in range(rand_len):
        random_chars += random.choice(SPECIALCHARS)

    token = user_id + random_chars + time
    return token
