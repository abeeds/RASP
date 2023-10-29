"""
users.py: accessing "messages" from other added users
"""

UNREAD_MSGS = 'unreadMessages'

users = {
    'John Messagesender': {
        UNREAD_MSGS: {
            """
            messages are in dict so the key can be used to timestamp
            """
            '2023-10-15T12:24:36': 'Hello world!',
            '2023-10-16T00:00:12': 'You up?',
        },
    },
    'Jamie Theuser': {
        UNREAD_MSGS: {
            '2023-10-15T12:24:36': 'Lorem ipsum dolor',
            '2023-10-16T00:00:12': 'Sit amet, consectetur adipiscing elit.',
        },
    },
}


def get_users() -> dict:
    return users
