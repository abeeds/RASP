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


app = Flask(__name__)
api = Api(app)


DEFAULT = 'Default'
MENU = 'menu'
MAIN_MENU_EP = '/MainMenu'
MAIN_MENU_NM = "RASP"
HELLO_EP = '/hello'
HELLO_RESP = 'hello'
# USERS = 'users'
USERS_EP = '/users'
USER_MENU_EP = '/user_menu'
USER_MENU_NM = 'User Menu'
REGISTER_URL = "/register"
deactivate_url = "/deactivate"
USER_ID = 'User ID'
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


user_fields = api.model('NewUser', {
    dbu.USERNAME: fields.String,
    dbu.PASSWORD: fields.String
    })


@api.route(f'{USERS_EP}')
class Users(Resource):
    """
    This class supports fetching a list of all users.
    """
    def get(self):
        """
        This method returns all users.
        """
        return {
            TYPE: DATA,
            TITLE: 'Current Users',
            DATA: dbu.get_users(),
            MENU: USER_MENU_EP,
            RETURN: MAIN_MENU_EP,
        }

    @api.expect(user_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self):
        """
        Add a user.
        """
        requser = request.json
        try:
            username = requser[dbu.USERNAME]
            userpass = requser[dbu.PASSWORD]
            dbu.insert_user(username, userpass)
            return 200
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@api.route(f'{USER_MENU_EP}')
class UserMenu(Resource):
    """
    This will deliver our user menu.
    """
    def get(self):
        """
        Gets the user menu.
        """
        return {
                   TITLE: USER_MENU_NM,
                   DEFAULT: '0',
                   'Choices': {
                       '1': {
                                'url': '/',
                                'method': 'get',
                                'text': 'Get User Details',
                       },
                       '0': {
                                'text': 'Return',
                       },
                   },
               }


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


registration_response_model = api.model('RegistrationResponse', {
    'inserted_id': fields.String,
    'message': fields.String,
})


@api.route(f'{REGISTER_URL}/<string:username>/<string:password>')
class Register(Resource):
    def post(self, username, password):
        """
        Endpoint for handling the registration process.
        """
        new_id = dbu.insert_user(username, password)
        response = {
            'inserted_id': str(new_id.inserted_id)
            if new_id.inserted_id else None,

            'message': 'Registration Successful.'
            if new_id.inserted_id
            else "Registration Failed."
        }

        return response


deactivate_response_model = api.model('DeactivateResponse', {
    'deleted_id': fields.String,
    'deleted_username': fields.String,
    'message': fields.String,
})


@api.route(f'{deactivate_url}/<string:username>')
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
            else "Delete Failed.",
        }

        return response
# -------- END OF USER RELATED ENDPOINTS --------


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
        return {
            TYPE: DATA,
            TITLE: 'Current Messages',
            DATA: dbm.get_all_messages(),
            MENU: USER_MENU_EP,  # fix this later!
            RETURN: MAIN_MENU_EP,
        }

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
        return {
            TYPE: DATA,
            TITLE: 'Current Messages',
            DATA: dbm.get_chatroom_messages(roomname),
            MENU: USER_MENU_EP,  # fix this later!
            RETURN: MAIN_MENU_EP,
        }
