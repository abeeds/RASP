from .db_connect import insert_one, connect_db
from .db_connect import fetch_one, fetch_all_as_dict, fetch_many
from datetime import datetime
from bson import objectid


# TODO - edit, delete msg - need to figure out
#        user friendly way to select msgs
#
#        get 15 recent msgs from specific room
#
#        function that deletes all msgs associated
#        with a specific room - used when that room
#        is deleted

MESSAGE_COLLECT = "messages"

# message db fields
USERNAME = "username"
TIMESTAMP = "timestamp"
CHATROOM = "chatroom_name"
CONTENT = "content"


# assumes the username and room name are already verified
def insert_message(username, room, content):
    new_msg = {}
    new_msg[USERNAME] = username
    new_msg[TIMESTAMP] = datetime.now().timestamp()
    new_msg[CHATROOM] = room
    new_msg[CONTENT] = content

    connect_db()
    _id = insert_one(MESSAGE_COLLECT, new_msg)
    return _id, new_msg[TIMESTAMP]


def get_all_messages():
    connect_db()
    return fetch_all_as_dict(TIMESTAMP, MESSAGE_COLLECT)


def get_chatroom_messages(chatroom: str):
    connect_db()
    return fetch_many(MESSAGE_COLLECT, {CHATROOM: chatroom})


def message_exists(id):
    obID = objectid(id)
    connect_db()
    return fetch_one(MESSAGE_COLLECT, {"_id": obID})
