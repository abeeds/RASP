from .db_connect import insert_one, connect_db, del_one
from .db_connect import fetch_one, fetch_all_as_dict, fetch_many
from .db_connect import del_many, update_one
from datetime import datetime
from bson import ObjectId


# TODO - delete msg - need to figure out
#        user friendly way to select msgs
#
#        function that deletes all msgs associated
#        with a specific room - used when that room
#        is deleted

MESSAGE_COLLECT = "messages"

# message db fields
USERNAME = "username"
TIMESTAMP = "timestamp"
LAST_EDITED = "last_edited"
CHATROOM = "chatroom_name"
CONTENT = "content"
ID = "_id"


# assumes the username and room name are already verified
def insert_message(username: str, room: str, content: str):
    new_msg = {}
    new_msg[USERNAME] = username
    new_msg[TIMESTAMP] = datetime.now().timestamp()
    new_msg[CHATROOM] = room
    new_msg[CONTENT] = content

    connect_db()
    _id = insert_one(MESSAGE_COLLECT, new_msg).inserted_id
    return _id, new_msg[TIMESTAMP]


def get_all_messages():
    connect_db()
    return fetch_all_as_dict(TIMESTAMP, MESSAGE_COLLECT)


def get_chatroom_messages(chatroom: str, pages="ALL"):
    connect_db()
    if pages == "ALL":
        messages = fetch_many(MESSAGE_COLLECT,
                              {CHATROOM: chatroom},
                              sort_by=TIMESTAMP)
    else:
        pages = int(pages)
        messages = fetch_many(MESSAGE_COLLECT,
                              {CHATROOM: chatroom},
                              pages * 10,
                              TIMESTAMP)

    message_dict = {str(msg[ID]):
                    {
                        "Chatroom": msg[CHATROOM],
                        "User": msg[USERNAME],
                        "Timestamp": msg[TIMESTAMP],
                        **({"Last Edited": msg[LAST_EDITED]} if LAST_EDITED in msg else {}),
                        "Content": msg[CONTENT]
                    }
                    for msg in messages}

    return message_dict


def message_exists(id: str):
    obID = ObjectId(id)
    connect_db()
    return fetch_one(MESSAGE_COLLECT, {ID: obID})


def delete_message(id: str):
    obID = ObjectId(id)

    connect_db()
    if message_exists(id):
        del_one(MESSAGE_COLLECT, {ID: obID})


def del_msgs_from_user(username: str):
    connect_db()
    del_many(MESSAGE_COLLECT, {USERNAME: username})


def edit_message(id: str, new_msg: str):
    filter = {ID:  ObjectId(id)}
    new_vals = {"$set": {
        CONTENT: new_msg,
        LAST_EDITED: datetime.now().timestamp()
        }}

    connect_db()
    if message_exists(id):
        update_one(MESSAGE_COLLECT, filter, new_vals)
