"""
users.py: accessing "messages" from other added users
"""
import random

import db.db_connect as dbc

UNREAD_MSGS = 'unreadMessages'
OLD_MSGS = 'readMessages'
TEST_USER = 'Jamie Theuser'

USERS_COLLECT = 'users'

ID_LEN = 24
BIG_NUM = 100_000_000_000_000_000_000

MOCK_ID = '0' * ID_LEN

NAME = 'name'

users = {
    'John Messagesender': {
        UNREAD_MSGS: {
            """
            messages are in dict so the key can be used to timestamp
            """
            '2023-10-15T12:24:36': 'Hello world!',
            '2023-10-16T00:00:12': 'You up?',
        },
        OLD_MSGS: {
            '2020-07-19T12:24:36': 'This message has already been read.',
        },
    },
    TEST_USER: {
        UNREAD_MSGS: {
            '2023-10-15T12:24:36': 'Lorem ipsum dolor',
            '2023-10-16T00:00:12': 'Sit amet, consectetur adipiscing elit.',
        },
        OLD_MSGS: {
        },
    },
}


def _get_test_name():
    name = 'test'
    rand_part = random.randint(0, BIG_NUM)
    return name + str(rand_part)


def get_test_user():
    test_game = {}
    test_game[NAME] = _get_test_name()
    return test_game


def _gen_id() -> str:
    _id = random.randint(0, BIG_NUM)
    _id = str(_id)
    _id = _id.rjust(ID_LEN, '0')
    return _id


def get_users() -> dict:
    dbc.connect_db()
    return dbc.fetch_all_as_dict(NAME, USERS_COLLECT)


def get_unread_from(senderName):
    return users[senderName][UNREAD_MSGS]


def add_user(name: str) -> str:
    if not name:
        raise ValueError('A name must be input')
    users[name] = {UNREAD_MSGS: {}, OLD_MSGS: {}}
    return _gen_id()


def del_user(name: str):
    if name in users:
        del users[name]
    else:
        raise ValueError(f'Delete failure: {name} not in database.')


def exists(name: str) -> bool:
    return name in get_users()
