"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.

CTRL + F to jump to these sections:
    USER RELATED ENDPOINTS
    MESSAGE RELATED ENDPOINTS
    CHATROOM RELATED ENDPOINTS
"""

from http import HTTPStatus

from flask import Flask, request
from flask_restx import Resource, Api, fields
# import db.db_connect as dbc
from flask_cors import CORS

# import werkzeug.exceptions as wz

import db.db_connect as dbc
import db.db_users as dbu
import db.db_messages as dbm
import db.db_chatrooms as dbch
import forms.form as frm


app = Flask(__name__)
api = Api(app)
CORS(app)


DEFAULT = 'Default'
HELLO_EP = '/hello'
HELLO_RESP = 'hello'
ENDPOINTS_EP = '/endpoints'

# user endpoint urls
DEACTIVATE_URL = "/ban"
DEACTIVATE_SELF_URL = "/deactivate"
GET_USERS_URL = '/get_users'
LOGIN_URL = "/login"
REGISTER_URL = "/register"
UPDATE_USER_URL = "/update_username"
UPDATE_PASS_URL = "/update_password"

# chatroom endpoint urls
DELETE_CHATROOM_URL = '/delete_chatroom'
GET_CHATROOMS_URL = '/get_chatrooms'
INSERT_CHATROOM_URL = '/insert_chatroom'
UPDATE_CR_DESC_URL = '/update_chatroom_desc'

# message endpoint urls
DEL_MSG_URL = '/delete_msg/<string:msg_id>'
GET_MSGS_URL = '/get_msgs'
GET_MSGS_PG_URL = '/get_msgs_pg'
GET_MSGS_TEST_URL = '/get_msgs_test_version'
# WRITE_MSG_URL = '/write_msg/<string:room>/<string:username>/<string:content>'
WRITE_MSG_URL = '/write_msg'

NUKE_URL = '/wipe/<string:collection>/<string:code>'
GET_FORMS_URL = '/get_forms'


@api.route(HELLO_EP)
class HelloWorld(Resource):
    """
    The purpose of the HelloWorld class is to have a simple test to see if the
    app is working at all.
    """
    def get(self):
        """
        A trivial endpoint to see if the server is running.
        It just answers with "hello world."
        """
        return {HELLO_RESP: 'world'}


@api.route(ENDPOINTS_EP)
class Endpoints(Resource):
    """
    This class will serve as live, fetchable documentation of what
    endpoints are available in the system.
    """
    def get(self):
        """
        The `get()` method will return a list of available endpoints.
        """
        endpoints = sorted(rule.rule for rule
                           in api.app.url_map.iter_rules())
        return {"Available endpoints": endpoints}


# ----------- USER RELATED ENDPOINTS -----------
@api.route(f'{GET_USERS_URL}')
class GetUsers(Resource):
    def get(self):
        """
        This method returns all users.
        Returned in this format:
        {"Username": {"_id": id}}
        """
        users_data = dbu.get_users()

        return users_data


@api.route(f'{REGISTER_URL}/<string:username>/<string:password>')
class Register(Resource):
    def post(self, username, password):
        """
        Endpoint for inserting users.
        username can't have spaces in it.
        usernames must also be unique.
        Passwords are hashed.
        """
        response = {
            'inserted_id': None,
            'message': ""
        }

        # ensure the username is not taken
        if dbu.user_exists(username):
            response['message'] = 'Username is already taken.'

        # make sure there aren't spaces in the username
        elif " " in username:
            response['message'] = "Username cannot have a space"

        else:
            new_id = dbu.insert_user(username, password)
            response['inserted_id'] = str(new_id.inserted_id)
            response['message'] = 'Registration Successful.'
        return response


@api.route(f'{LOGIN_URL}/<string:username>/<string:password>')
class LogIn(Resource):
    def get(self, username, password):
        """
        Endpoint for userpass check.
        username can't have spaces in it.
        usernames must also be unique.
        """
        response = {
            'message': ""
        }

        # ensure the userpass combo is correct
        if dbu.userpass_check(username, password):
            response['message'] = 'true'

        # make sure there aren't spaces in the username
        else:
            response['message'] = "false"

        return response


@api.route(f'{DEACTIVATE_URL}/<string:username>')
class DeactivateUser(Resource):
    def delete(self, username):
        """
        Endpoint for banning users.
        The user is deleted and all messages they have
        written are also deleted.
        The user is identified by the username.
        """
        deleted_id = ""
        user_doc = dbu.user_exists(username)
        if user_doc and '_id' in user_doc:
            deleted_id = str(user_doc['_id'])
            dbu.ban(username)

        response = {
            'deleted_id': deleted_id if deleted_id
            else None,
            'deleted_username': username if deleted_id
            else None,
            'message': 'Delete Successful' if deleted_id
            else "Username does not exist.",
        }

        return response


@api.route(f'{DEACTIVATE_SELF_URL}/<string:username>/<string:password>')
class DeactivateSelf(Resource):
    def delete(self, username, password):
        """
        Endpoint for deleting users.
        The user is identified by the username.
        Password is verified.
        """
        deleted_id = ""
        user_doc = dbu.userpass_check(username, password)
        if user_doc and '_id' in user_doc:
            deleted_id = str(user_doc['_id'])
            dbu.deactivate(username)

        response = {
            'deleted_id': deleted_id if deleted_id
            else None,
            'deleted_username': username if deleted_id
            else None,
            'message': 'Account deactivated. \
                Your messages persist.' if deleted_id
            else "User/pass combo does not exist.",
        }

        return response


@api.route(f'{UPDATE_USER_URL}/<string:curr_username>/<string:new_username>')
class UpdateUser(Resource):
    def put(Resource, curr_username, new_username):
        """
            Updates a username from curr_username to new_username.
            First checks that the curr_username exists, and the new
            username is not taken.
        """
        response = {
            "Status": ""
        }
        if not dbu.user_exists(curr_username):
            response["Status"] = "The current username doesn't exist."

        elif dbu.user_exists(new_username):
            response["Status"] = "The new username is already taken."

        else:
            dbu.update_username(curr_username, new_username)
            response['Status'] = "Updated Successfully"
        return response


@api.route(f'{UPDATE_PASS_URL}/<string:username>/<string:new_password>')
class UpdatePw(Resource):
    def put(Resource, username, new_password):
        """
            Updates the password of account with specific username.
            This endpoint will return a failure if an account with
            username does not exist.
        """
        updateStatus = False

        if dbu.user_exists(username):
            updateStatus = True
            dbu.update_password(username, new_password)

        response = {
            'Status': "Updated Successfully" if updateStatus
            else "The provided username does not exist."
        }
        return response


# -------- MESSAGE RELATED ENDPOINTS --------
@api.route(f'{GET_MSGS_URL}/<string:room_name>')
class GetMsgs(Resource):
    def get(self, room_name):
        """
        This endpoint returns all messages from a specified room.
        This endpoint checks that the room is valid.
        Use the get_chatrooms endpoint to see all valid rooms.
        The format of each returned message is:
        id: {
            "Chatroom": ______,
            "User": ______,
            "Timestamp: ______,
            "Content": ______
        }
        """
        if not dbch.room_exists(room_name):
            return {
                "Status": "Room does not exist."
            }

        messages = dbm.get_chatroom_messages(room_name)
        return messages


@api.route(f'{GET_MSGS_PG_URL}/<string:room_name>/<int:pages>')
class GetMsgsLim(Resource):
    def get(self, room_name, pages):
        """
        Returns a certain amount of messages from a specific room.
        Each page is 10 messages
        This endpoint checks that the room is valid.
        Use the get_chatrooms endpoint to see all valid rooms.
        The format of each returned message is:
        id: {
            "Chatroom": ______,
            "User": ______,
            "Timestamp: ______,
            "Content": ______
        }
        """
        if not dbch.room_exists(room_name):
            return {
                "Status": "Room does not exist."
            }

        messages = dbm.get_chatroom_messages(room_name, pages)
        return messages


@api.route(f'{GET_MSGS_TEST_URL}/<string:room_name>')
class GetMsgsTestVer(Resource):
    def get(self, room_name):
        """
        This endpoint returns all messages from a specified room.
        The format of each returned message is:
        id: {
            "Chatroom": ______,
            "User": ______,
            "Timestamp: ______,
            "Content": ______
        }

        This endpoint does not check if the room is valid.
        This is to allow for checking whether messages
        associated with a deleted room still exist.
        """

        messages = dbm.get_chatroom_messages(room_name)
        return messages


message_fields = api.model('NewMessage', {
    dbm.CHATROOM: fields.String,
    dbm.USERNAME: fields.String,
    dbm.CONTENT: fields.String,
})


@api.route(f'{WRITE_MSG_URL}')
class WriteMessage(Resource):
    @api.expect(message_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self):
        """
        Writes a message to the specified room from the specified user.
        room specifies the chatroom
        username specifies the user
        content specifies the content of the message
        This field checks that the user and room are valid.
        Please use the get endpoints to see values you can
        use.
        """
        room = request.json[dbm.CHATROOM]
        username = request.json[dbm.USERNAME]
        content = request.json[dbm.CONTENT]
        if not dbch.room_exists(room):
            return {
                "Status": "A room with that name does not exist."
            }

        if not dbu.user_exists(username):
            return {
                "Status": "User with that username does not exist."
            }

        dbm.insert_message(username, room, content)
        return {
            "Status": "message written successfully."
        }


@api.route(f'{DEL_MSG_URL}')
class DeleteMsg(Resource):
    def delete(self, msg_id):
        """
        This endpoint deletes messages.
        Messages are identified with their id (_id in mongodb)
        because this is the only way to completely identify them.
        Message ids can be found using the get_msgs endpoint.
        They are the keys in the response to that endpoint.
        """
        if not dbm.message_exists(msg_id):
            return {
                "Status": "A message with that ID does not exist."
            }

        dbm.delete_message(msg_id)
        return {
            "Status": "Message deleted successfully."
        }


# --------- CHATROOM RELATED ENDPOINTS ---------
chatroom_fields = api.model('NewChatroom', {
    dbch.NAME: fields.String,
    dbch.DESC: fields.String,
    dbch.OWNER: fields.String,
})


@api.route(f'{GET_CHATROOMS_URL}')
class GetChatrooms(Resource):
    def get(self):
        """
        Displays all available chatrooms.
        Rooms are displayed in this format:
        Room_name: {
            description: ________
        }
        """
        return dbch.get_chatrooms()


@api.route(f'{INSERT_CHATROOM_URL}')
class InsertChatroom(Resource):
    @api.expect(chatroom_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self):
        """
        Inserts a chatroom.
        room_name specifies the name.
        room_desc specifies the description.
        """
        room_name = request.json[dbch.NAME]
        room_desc = request.json[dbch.DESC]
        room_owner = request.json[dbch.OWNER]
        response = {
            "status": ""
        }
        if dbch.room_exists(room_name):
            response["status"] = "A chatroom with this name already exists"
        elif dbch.insert_chatroom(
                room_name, room_desc, room_owner) is not None:
            response["status"] = "Chatroom created successfully."
        else:
            response["status"] = "Chatroom creation failed."

        return response


@api.route(f'{DELETE_CHATROOM_URL}/<string:room_name>')
class DeleteChatroom(Resource):
    def delete(self, room_name):
        """
        Endpoint for deleting chatrooms identified by room_name.
        This endpoint also deletes all messages associated with it.
        """
        response = {
            "Chatroom Deleted": "",
            "Status": ""
        }
        if not dbch.room_exists(room_name):
            response["Status"] = "Chatroom with that name doesn't exist"
        else:
            dbch.delete_chatroom(room_name)
            response["Chatroom Deleted"] = room_name
            response["Status"] = "Chatroom deleted successfuly"

        return response


@api.route(f'{UPDATE_CR_DESC_URL}')
class UpdateCrDesc(Resource):
    @api.expect(chatroom_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def put(Resource):
        """
        This endpoint updates the chatroom's description.
        The chatroom is specified with the room_name parameter.
        The new description is entered in the new_desc parameter.
        """

        room = request.json[dbch.NAME]
        description = request.json[dbch.DESC]

        response = {
            "Status": ""
        }

        if not dbch.room_exists(room):
            response["Status"] = "A room with that name does not exist."
        else:
            dbch.update_description(room, description)
            response["Status"] = "Chatroom description updated successfully."
        return response


@api.route(f'{NUKE_URL}')
class DeleteAllInCollection(Resource):
    def delete(self, collection, code):
        """
        Endpoint for wiping all docs in a collection.
        """
        response = {
            "Status": ""
        }

        if code == "4253":
            dbc.del_all_in_collection(collection)
            response["Status"] = "Code accepted."
        else:
            response["Status"] = "Permission denied."
        return response


@api.route(f'{GET_FORMS_URL}')
class GetForms(Resource):
    """
    This method returns all form entries in a dict.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.doc(params=frm.get_form_descr())
    def get(self):

        form_data = frm.get_form_descr()

        return form_data
