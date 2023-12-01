from .db_connect import insert_one, connect_db


# TODO - edit, delete msg - need to figure out
#        user friendly way to select msgs
#        get 15 recent msgs from specific room

MESSAGE_COLLECT = "messages"

# message db fields
USERNAME = "username"
CHATROOM = "chatroom_name"
CONTENT = "content"


# assumes the username and room name are already verified
def insert_message(username, room, content):
    new_msg = {}
    new_msg[USERNAME] = username
    new_msg[CHATROOM] = room
    new_msg[CONTENT] = content

    connect_db()
    _id = insert_one(MESSAGE_COLLECT, new_msg)
    return _id
