"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

from http import HTTPStatus

from flask import Flask, request, redirect
from flask_restx import Resource, Api, fields
import db.db_connect as dbc

import werkzeug.exceptions as wz

import db.users as usrs
from db.db_users import get_users, insert_user, deactivate

from .forms import USERNAME_FORM, FLDS, USERNAME, VALUE

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
USER_ID = 'User ID'
TYPE = 'Type'
FORM = "Form"
DATA = 'Data'
TITLE = 'Title'
RETURN = 'Return'


URL = "url"
METHOD = "method"
TEXT = "text"
SUBMIT = "Submit"

# using to pick main menu mode
OUT = "OUT"
IN = "IN"
MODE = OUT
VERIFYING = "Verify"

V_MODE = "Verification Mode"
V_LOGIN = "VERIFYING LOGIN"
V_REGISTER = "VERIFYING REGISTER"


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
            if MODE == OUT:
                print("C")
                updated_username = USERNAME_FORM[FLDS][USERNAME][VALUE]
                print(f"Updated username: {updated_username}")
                print("D")
                return {TITLE: MAIN_MENU_NM,
                        DEFAULT: 1,
                        'Choices': {
                            '1': {'url': '/login', 'method': 'get',
                                  'text': 'Log In'},
                            '2': {'url': f'{REGISTER_URL}', 'method': 'post',
                                  'text': 'Register'},
                            '3': {'url': '/get_users',
                                  'method': 'get',
                                  'text': 'Display Users'},
                            '4': {'url': '/test',
                                  'method': 'get',
                                  'text': 'Testing DB Connection'},
                            '5': {'url': '/test_insert',
                                  'method': 'get',
                                  'text': 'Insert Some Users'},
                            '6': {'url': '/test_delete',
                                  'method': 'get',
                                  'text': 'Delete Test Users'},
                            'X': {'text': 'Exit'},
                        }}
            if MODE == IN:
                {TITLE: MAIN_MENU_NM,
                    DEFAULT: 1,
                    'Choices': {
                        '1': {'url': '/', 'method': 'get',
                              'text': 'PLACEHOLDER'},
                        'X': {'text': 'Exit'},
                    }}

            if MODE == VERIFYING:
                print("Login: VERIFYING USERNAME")

                print("A")
                updated_username = USERNAME_FORM[FLDS][USERNAME][VALUE]
                print(f"Updated username: {updated_username}")
                print("B")

                MODE = OUT
                return redirect(f'{MAIN_MENU_EP}')


user_fields = api.model('NewUser', {
    usrs.NAME: fields.String,
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
            DATA: usrs.get_users(),
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
        name = request.json[usrs.NAME]
        try:
            new_id = usrs.add_user(name)
            return {USER_ID: new_id}
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


@api.route('/get_users')
class GetUsers(Resource):
    def get(self):
        """
        This method returns all users.
        """
        users_data = get_users()

        return {
            TYPE: DATA,
            TITLE: 'User List',
            DATA: users_data,
        }


# only for testing purpose
@api.route('/test')
class Test(Resource):
    def get(self):
        """
        This method returns all users.
        """
        users_data = get_users()

        return {
            TYPE: DATA,
            TITLE: 'User List',
            DATA: users_data,
            MENU: USER_MENU_EP,
            RETURN: MAIN_MENU_EP,
        }


@api.route(f'{REGISTER_URL}')
class Register(Resource):
    def get(self):
        """
        Endpoint for handling the registration process.
        """
        dbc.connect_db()
        return USERNAME_FORM


@api.route('/login')
class LogIn(Resource):
    def get(self):
        """
        Endpoint for handling the login process.
        """
        dbc.connect_db()
        # return LOGIN_FORM


USERNAME1 = "john"
USERNAME2 = "sal"
USERNAME3 = "luis"


@api.route('/test_insert')
class TestInsert(Resource):
    def get(self):
        insert_user(USERNAME1, "password")
        insert_user("ajsbdkasd", "password")
        msg = {"Users": "Inserted"}

        return {
            TYPE: DATA,
            TITLE: 'Inserting Users',
            DATA: msg,
        }


@api.route('/test_delete')
class TestDelete(Resource):
    def get(self):
        deactivate("ajsbdkasd")
        msg = {"Users": "Deleted"}

        return {
            TYPE: DATA,
            TITLE: 'Inserting Users',
            DATA: msg,
        }
