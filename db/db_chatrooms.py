import db.db_connect as dbc
import db.db_messages as dbm


CHATROOM_COLLECT = "chat rooms"
NAME = "chatroom_name"
DESC = "description"
OWNER = "owner"


def room_exists(name: str):
    dbc.connect_db()
    return dbc.fetch_one(CHATROOM_COLLECT, {NAME: name})


def insert_chatroom(name: str, desc: str = "", owner: str = ""):
    room = {}
    room[NAME] = name
    room[DESC] = desc
    room[OWNER] = owner

    dbc.connect_db()
    _id = dbc.insert_one(CHATROOM_COLLECT, room)
    return _id


def delete_chatroom(name: str):
    dbc.connect_db()
    if room_exists(name):
        msgs = dbc.client[dbc.USER_DB][dbm.MESSAGE_COLLECT]
        msgs.delete_many({dbm.CHATROOM: name})
        return dbc.del_one(CHATROOM_COLLECT, {NAME: name})
    else:
        raise ValueError(f'Could not find a room named {name}.')


def update_description(name: str, new_desc: str = ""):
    filter = {NAME: name}
    new_vals = {DESC: new_desc}

    dbc.connect_db()
    dbc.update_doc(CHATROOM_COLLECT, filter, new_vals)


def get_chatrooms():
    dbc.connect_db()
    chatrooms = dbc.fetch_all(CHATROOM_COLLECT)

    chatrooms_dict = {}
    for chatroom in chatrooms:
        chatroom_name = chatroom.get(NAME)
        chatroom_desc = str(chatroom.get(DESC, ""))
        chatroom_owner = str(chatroom.get(OWNER, ""))

        chatrooms_dict[chatroom_name] = {DESC: chatroom_desc,
                                         OWNER: chatroom_owner}

    return chatrooms_dict
