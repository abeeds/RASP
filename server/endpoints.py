"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

from http import HTTPStatus

from flask import Flask, request
from flask_restx import Resource, Api, fields
import db.db_connect as dbc

import werkzeug.exceptions as wz

import db.users as usrs

from .forms import LOGIN, REGISTRATION

app = Flask(__name__)
api = Api(app)


DEFAULT = 'Default'
MENU = 'menu'
MAIN_MENU_EP = '/MainMenu'
MAIN_MENU_NM = "Welcome to Text Game!"
HELLO_EP = '/hello'
HELLO_RESP = 'hello'
# USERS = 'users'
USERS_EP = '/users'
USER_MENU_EP = '/user_menu'
USER_MENU_NM = 'User Menu'
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
REG = "REGISTERING"
MODE = OUT


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
            global MODE
            if MODE == OUT:
                return {TITLE: MAIN_MENU_NM,
                        DEFAULT: 1,
                        'Choices': {
                            '1': {'url': '/login', 'method': 'get',
                                  'text': 'Log In'},
                            '2': {'url': '/register', 'method': 'get',
                                  'text': 'Register'},
                            '3': {'url': '/test',
                                  'method': 'get',
                                  'text': 'Testing DB Connection'},
                            '4': {'url': '/test_form',
                                  'method': 'get',
                                  'text': 'Test Form'},
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


# only for testing purpose
@api.route('/test')
class Test(Resource):
    def get(self):
        dbc.connect_db()
        out = "Success"
        if (dbc.client is None):
            out = "Fail"
        return {
            TYPE: DATA,
            TITLE: 'TEST',
            DATA: {
                "Route":
                {
                    "Connection": out,
                }
            },
        }


@api.route('/register')
class Register(Resource):
    """
    Endpoint for handling the registration process.
    """
    def get(self):
        dbc.connect_db()
        return REGISTRATION


@api.route('/login')
class LogIn(Resource):
    """
    Endpoint for handling the login process.
    """
    def get(self):
        dbc.connect_db()
        return LOGIN


@api.route('/test_form')
class TestForm(Resource):
    def get(self):
        return REGISTRATION
