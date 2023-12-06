from .db_connect import insert_one, connect_db
from .db_connect import fetch_one, del_one
from .db_connect import update_one, fetch_all


CHATROOM_COLLECT = "chat rooms"
NAME = "chatroom_name"
DESC = "description"


def room_exists(name):
    connect_db()
    return fetch_one(CHATROOM_COLLECT, {NAME: name})


def insert_chatroom(name: str, desc: str = ""):
    if room_exists(name):
        raise ValueError(f'Chat room with that already exists: {name}')
    if not name:
        raise ValueError('Chatroom must have a name')

    room = {}
    room[NAME] = name
    room[DESC] = desc

    connect_db()
    _id = insert_one(CHATROOM_COLLECT, room)
    return _id


def delete_chatroom(name: str):
    connect_db()
    if room_exists(name):
        return del_one(CHATROOM_COLLECT, {NAME: name})
    else:
        raise ValueError(f'Could not find a room named {name}.')


def update_description(name: str, new_desc: str = ""):
    filter = {NAME: name}
    new_vals = {"$set": {DESC: new_desc}}

    connect_db()
    update_one(CHATROOM_COLLECT, filter, new_vals)


def get_chatrooms():
    connect_db
    rooms = fetch_all(CHATROOM_COLLECT)

    # display rooms & descriptions using dict
    rooms_dict = {room[NAME]: {"description": str(room[DESC])}
                  for room in rooms}
    return rooms_dict
