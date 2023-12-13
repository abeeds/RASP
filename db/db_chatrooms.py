import db.db_connect as dbc


CHATROOM_COLLECT = "chat rooms"
NAME = "chatroom_name"
DESC = "description"


def room_exists(name: str):
    dbc.connect_db()
    return dbc.fetch_one(CHATROOM_COLLECT, {NAME: name})


def insert_chatroom(name: str, desc: str = ""):
    if room_exists(name):
        raise ValueError(f'Chat room with that already exists: {name}')
    if not name:
        raise ValueError('Chatroom must have a name')

    room = {}
    room[NAME] = name
    room[DESC] = desc

    dbc.connect_db()
    _id = dbc.insert_one(CHATROOM_COLLECT, room)
    return _id


def delete_chatroom(name: str):
    dbc.connect_db()
    if room_exists(name):
        return dbc.del_one(CHATROOM_COLLECT, {NAME: name})
    else:
        raise ValueError(f'Could not find a room named {name}.')


def update_description(name: str, new_desc: str = ""):
    filter = {NAME: name}
    new_vals = {"$set": {DESC: new_desc}}

    dbc.connect_db()
    dbc.update_one(CHATROOM_COLLECT, filter, new_vals)


def get_chatrooms():
    dbc.connect_db()
    return dbc.fetch_all_as_dict(NAME, CHATROOM_COLLECT)
