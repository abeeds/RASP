"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

from http import HTTPStatus

from flask import Flask, request
from flask_restx import Resource, Api, fields
# import db.db_connect as dbc

import werkzeug.exceptions as wz

import db.db_users as dbu
import db.db_messages as dbm
import db.db_chatrooms as dbch


app = Flask(__name__)
api = Api(app)


DEFAULT = 'Default'
MENU = 'menu'
MAIN_MENU_EP = '/MainMenu'
MAIN_MENU_NM = "RASP"
HELLO_EP = '/hello'
HELLO_RESP = 'hello'
# USERS = 'users'
USER_MENU_EP = '/user_menu'
USER_MENU_NM = 'User Menu'
REGISTER_URL = "/register"
DEACTIVATE_URL = "/deactivate"
UPDATE_USER_URL = "/update_username"
UPDATE_PASS_URL = "/update_password"
USER_ID = 'User ID'
GET_CHATROOMS_URL = '/get_chatrooms'
INSERT_CHATROOM_URL = '/insert_chatroom'
MSGS_EP = '/messages'
TYPE = 'Type'
FORM = "Form"
DATA = 'Data'
TITLE = 'Title'
RETURN = 'Return'


URL = "url"
METHOD = "method"
TEXT = "text"
SUBMIT = "Submit"


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

    @api.route('/endpoints')
    class Endpoints(Resource):
        """
        This class will serve as live, fetchable documentation of what
        endpoints
        are available in the system.
        """
        def get(self):
            """
            The `get()` method will return a list of available endpoints.
            """
            endpoints = sorted(rule.rule for rule
                               in api.app.url_map.iter_rules())
            return {"Available endpoints": endpoints}

    @api.route(f'{MAIN_MENU_EP}')
    class MainMenu(Resource):
        """
        This will deliver our main menu.
        """
        def get(self):
            """
            Gets the main game menu.
            """
            global MODE, USERNAME_FORM

            return {TITLE: MAIN_MENU_NM,
                    DEFAULT: 1,
                    'Choices': {
                        '1': {'url': '/login', 'method': 'get',
                              'text': 'Log In'},
                        '2': {'url': f'{REGISTER_URL}', 'method': 'get',
                              'text': 'Register'},
                        '3': {'url': '/get_users',
                              'method': 'get',
                              'text': 'Display Users'},
                        'X': {'text': 'Exit'},
                    }}


# ----------- USER RELATED ENDPOINTS -----------
@api.route('/get_users')
class GetUsers(Resource):
    def get(self):
        """
        This method returns all users.
        """
        users_data = dbu.get_users()

        return {
            TYPE: DATA,
            TITLE: 'User List',
            DATA: users_data,
        }


@api.route(f'{REGISTER_URL}/<string:username>/<string:password>')
class Register(Resource):
    def post(self, username, password):
        """
        Endpoint for handling the registration process
        (Inserting Users)
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


@api.route(f'{DEACTIVATE_URL}/<string:username>')
class DeactivateUser(Resource):
    def post(self, username):
        """
        Endpoint for deleting users.
        """
        deleted_id = ""
        user_doc = dbu.user_exists(username)
        if user_doc and '_id' in user_doc:
            deleted_id = str(user_doc['_id'])
            dbu.deactivate(username)

        response = {
            'deleted_id': deleted_id if deleted_id
            else None,
            'deleted_username': username if deleted_id
            else None,
            'message': 'Delete Successful' if deleted_id
            else "Username does not exist.",
        }

        return response


@api.route(f'{UPDATE_USER_URL}/<string:curr_username>/<string:new_username>')
class UpdateUser(Resource):
    def put(Resource, curr_username, new_username):
        """
            Updates a username from curr_username to new_username.
            First checks that the curr_username exists, and the new one
            does not.
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
            Updates the password of the account with the provided
            username.
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
# -------- END OF USER RELATED ENDPOINTS --------


# -------- MESSAGE RELATED ENDPOINTS --------
message_fields = api.model('NewMessage', {
    dbm.USERNAME: fields.String,
    dbm.CHATROOM: fields.String,
    dbm.CONTENT: fields.String,
})


@api.route(f'{MSGS_EP}')
class Messages(Resource):
    """
    This class supports fetching a list of all messages.
    """
    def get(self):
        """
        This method returns all messages.
        """
        return dbm.get_all_messages()

    @api.expect(message_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self):
        """
        Add a messages.
        """
        reqmsg = request.json
        try:
            msgname = reqmsg[dbm.USERNAME]
            msgroom = reqmsg[dbm.CHATROOM]
            msgcontent = reqmsg[dbm.CONTENT]
            dbm.insert_message(msgname, msgroom, msgcontent)
            return 200
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@api.route(f'{MSGS_EP}/<string:roomname>')
class RoomMessages(Resource):
    """
    This class supports fetching a list of all messages from a chatroom.
    """
    def get(self, roomname):
        """
        This method returns all messages.
        """
        return dbm.get_chatroom_messages(roomname),


# CHATROOM RELATED ENDPOINTS
@api.route(f'{GET_CHATROOMS_URL}')
class GetChatrooms(Resource):
    def get(self):
        """
        Displays all available chatrooms.
        """
        return dbch.get_chatrooms()


@api.route(f'{INSERT_CHATROOM_URL}/<string:room_name>/<string:room_desc>')
class InsertChatroom(Resource):
    def post(self, room_name, room_desc=""):
        """
        Inserts a chatroom
        """
        response = {
            "status": ""
        }
        if dbch.room_exists(room_name):
            response["status"] = "A chatroom with this name already exists"
        elif dbch.insert_chatroom(room_name, room_desc) is not None:
            response["status"] = "Chatroom created successfully."
        else:
            response["status"] = "Chatroom creation failed."

        return response
