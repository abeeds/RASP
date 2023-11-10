"""
users.py: accessing "messages" from other added users
"""

UNREAD_MSGS = 'unreadMessages'
OLD_MSGS = 'readMessages'
TEST_USER = 'Jamie Theuser'

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


def get_users() -> dict:
    return users


def get_unread_from(senderName):
    return users[senderName][UNREAD_MSGS]


def add_user(name: str):
    if not name:
        raise ValueError('A name must be input')
    users[name] = {UNREAD_MSGS: {}, OLD_MSGS: {}}
