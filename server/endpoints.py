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

import werkzeug.exceptions as wz

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
DEACTIVATE_URL = "/users/ban"
DEACTIVATE_SELF_URL = "/users/deactivate"
GET_USERS_URL = '/users'
LOGIN_URL = "/users/login"
REGISTER_URL = "/users/register"
UPDATE_USER_URL = "/users/update_username"
UPDATE_PASS_URL = "/users/update_password"

# chatroom endpoint urls
CHATROOMS_URL = '/chatrooms'

# message endpoint urls
MSG_URL = '/messages'
GET_MSGS_TEST_URL = '/messages/test'

NUKE_URL = '/wipe/<string:collection>/<string:code>'
GET_FORMS_URL = '/get_forms'
FETCH_FORMS_URL = '/forms'


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
login_fields = api.model('login', {
    dbu.USERNAME: fields.String,
    dbu.PASSWORD: fields.String,
})

update_username_fields = api.model('update_username', {
    'user': fields.String,
    'newUser': fields.String,
    'pwd': fields.String
})


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
            raise wz.Conflict(username)

        # make sure there aren't spaces in the username
        elif " " in username:
            raise wz.BadRequest(username,
                                description="Username can't have spaces")

        else:
            new_id = dbu.insert_user(username, password)
            response['inserted_id'] = str(new_id.inserted_id)
            response['message'] = 'Registration Successful.'
            return response, HTTPStatus.OK


@api.route(f'{LOGIN_URL}')
@api.expect(login_fields)
class LogInPost(Resource):
    def post(self):
        """
            Either verified that the username and password are correct
            or that the login token is correct.
            Do not include login_token if you are including
            username and password! It will not be checked!
            Copy/Paste the following line for login token specifically:
            "login_token": ""

            if a username and password are entered, this returns a token
            if a login_token is entered, it returns a
            status saying success or an error if the token was not found
        """
        data = request.json
        token = ""

        if dbu.USERNAME in data and dbu.PASSWORD not in data:
            raise wz.BadRequest(description=f"{dbu.USERNAME} was entered"
                                + f" but not {dbu.PASSWORD}")

        if dbu.PASSWORD in data and dbu.USERNAME not in data:
            raise wz.BadRequest(description=f"{dbu.PASSWORD} was entered"
                                + f" but not {dbu.USERNAME}")

        if dbu.USERNAME in data and dbu.PASSWORD in data:
            token = dbu.create_login_token(data[dbu.USERNAME],
                                           data[dbu.PASSWORD])
            if token is None:
                raise wz.Unauthorized(description="The username and"
                                      + " password don't match")
            return {"status": "success",
                    "token": token}, HTTPStatus.OK

        if dbu.LOGIN_TOKEN in data:
            if dbu.verify_login_token(data[dbu.LOGIN_TOKEN]):
                return {"status": "success"}, HTTPStatus.OK
            raise wz.BadRequest(description="The login token is not valid")

        raise wz.BadRequest("No valid fields entered")


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
            return response, HTTPStatus.OK

        # make sure there aren't spaces in the username
        else:
            raise wz.BadRequest(
                description="Username and password do not match.")


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
        if user_doc is None:
            raise wz.NotFound(username)

        if user_doc and '_id' in user_doc:
            deleted_id = str(user_doc['_id'])
            dbu.ban(username)

        response = {
            'deleted_id': deleted_id,
            'deleted_username': username,
            'message': 'Delete Successful',
        }
        return response, HTTPStatus.OK


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
        if user_doc is None:
            raise wz.NotFound(username)
        if user_doc and '_id' in user_doc:
            deleted_id = str(user_doc['_id'])
            dbu.deactivate(username)

        response = {
            'deleted_id': deleted_id,
            'deleted_username': username,
            'message': 'Account deactivated. \
                Your messages persist.',
        }

        return response


@api.route(f'{UPDATE_USER_URL}')
@api.expect(update_username_fields)
class UpdateUser(Resource):
    def put(Resource):
        """
            Updates a username from curr_username to new_username.
            First checks that the curr_username exists, and the new
            username is not taken.
        """
        curr_user = request.json['user']
        new_user = request.json['newUser']
        password = request.json['pwd']
        if curr_user == new_user:
            raise wz.BadRequest(description="same username entered twice")
        if dbu.user_exists(curr_user) is None:
            raise wz.NotFound(
                              description=f'{curr_user} does not exist')
        elif not dbu.userpass_check(curr_user, password):
            raise wz.Unauthorized(description="Username and password don't"
                                  + " match our records")
        elif dbu.user_exists(new_user):
            raise wz.Conflict(description=f'{new_user} is already taken')

        else:
            dbu.update_username(curr_user, new_user)
            response = {
                "status": "Updated Successfully"
                }
            return response, HTTPStatus.OK


@api.route(f'{UPDATE_PASS_URL}/<string:username>/<string:new_password>')
class UpdatePw(Resource):
    def put(Resource, username, new_password):
        """
            Updates the password of account with specific username.
            This endpoint will return a failure if an account with
            username does not exist.
        """

        if dbu.user_exists(username):
            dbu.update_password(username, new_password)
        else:
            raise wz.NotFound(username)

        response = {
            'Status': "Updated Successfully"
        }
        return response, HTTPStatus.OK


# -------- MESSAGE RELATED ENDPOINTS --------
edit_message_fields = api.model('UpdatedMessage', {
    dbm.ID: fields.String,
    dbm.CONTENT: fields.String,
})


message_fields = api.model('NewMessage', {
    dbm.CHATROOM: fields.String,
    dbm.USERNAME: fields.String,
    dbm.CONTENT: fields.String,
})


@api.route(f'{MSG_URL}')
class Messages(Resource):
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
            raise wz.NotFound(room)
        if not dbu.user_exists(username):
            raise wz.NotFound(username)

        dbm.insert_message(username, room, content)
        return {
            "Status": "message written successfully."
        }, HTTPStatus.OK

    @api.expect(edit_message_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def put(self):
        """
        Updates a message, specified by object id, with the new content.
        You can use the get messages endpoint to retrieve an id
        """

        id = request.json[dbm.ID]
        content = request.json[dbm.CONTENT]

        if not dbm.message_exists(id):
            raise wz.NotFound(id)

        dbm.edit_message(id, content)
        return {
                "Status": "Message updated successfully."
            }, HTTPStatus.OK


@api.route(f'{MSG_URL}/<string:room_name>')
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
            raise wz.NotFound(room_name)

        messages = dbm.get_chatroom_messages(room_name)
        return messages


@api.route(f'{MSG_URL}/<string:room_name>/<string:pages>')
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
            raise wz.NotFound(room_name)

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
        return messages, HTTPStatus.OK


@api.route(f'{MSG_URL}/<string:msg_id>')
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
            raise wz.NotFound(msg_id)

        dbm.delete_message(msg_id)
        return {
            "Status": "Message deleted successfully."
        }, HTTPStatus.OK


# --------- CHATROOM RELATED ENDPOINTS ---------
chatroom_fields = api.model('NewChatroom', {
    dbch.NAME: fields.String,
    dbch.DESC: fields.String,
    dbch.OWNER: fields.String,
})

edit_chatroom_fields = api.model('UpdatedChatroom', {
    dbch.NAME: fields.String,
    dbch.DESC: fields.String,
})


@api.route(f'{CHATROOMS_URL}')
class Chatrooms(Resource):
    def get(self):
        """
        Displays all available chatrooms.
        Rooms are displayed in this format:
        Room_name: {
            description: ________
        }
        """
        return dbch.get_chatrooms()

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
            raise wz.Conflict(room_name)
        elif dbch.insert_chatroom(
                room_name, room_desc, room_owner) is not None:
            response["status"] = "Chatroom created successfully."
            return response, HTTPStatus.OK
        else:
            raise wz.InternalServerError(
                description="Chatroom creation failed")

        return response

    @api.expect(edit_chatroom_fields)
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
            raise wz.NotFound(room)
        else:
            dbch.update_description(room, description)
            response["Status"] = "Chatroom description updated successfully."
            return response, HTTPStatus.OK


@api.route(f'{CHATROOMS_URL}/<string:room_name>')
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
            raise wz.NotFound(room_name)
        else:
            dbch.delete_chatroom(room_name)
            response["Chatroom Deleted"] = room_name
            response["Status"] = "Chatroom deleted successfuly"
            return response, HTTPStatus.OK


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
            return response, HTTPStatus.OK
        else:
            raise wz.BadRequest("Permission denied")


@api.route(f'{GET_FORMS_URL}')
class GetForms(Resource):
    """
    This method returns all form entries in a dict.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.doc(params=frm.get_form_descr())
    def get(self):

        # print(f'username: {username}; fieldtype: {fieldtype}')

        form_data = frm.get_form()
        print(form_data)

        return form_data


hform_fields = api.model('HForm', {
    'user': fields.String,
    'oldpwd': fields.String,
    'newpwd': fields.String,
    'newpwdConfirm': fields.String,
})


@api.route(f'{UPDATE_PASS_URL}')
class UpdatePassword(Resource):
    @api.expect(hform_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def put(Resource):
        """
        Updates the password of account with specific username.
        """

        user = request.json['user']
        oldpwd = request.json['oldpwd']
        newpwd = request.json['newpwd']
        newpwdConfirm = request.json['newpwdConfirm']

        response = {
            "Status": ""
        }

        # ensure the userpass combo is correct
        if dbu.userpass_check(user, oldpwd):
            response['Status'] = 'User/Pass combo confirmed.'
            if newpwd == newpwdConfirm:
                dbu.update_password(user, newpwd)
                response['Status'] = 'Password updated.'
            else:
                raise wz.BadRequest(description='New passwords do not match.')
        else:
            raise wz.Unauthorized(
                description='Old password authentication failed.')

        print(response)

        return response


@api.route(f'{FETCH_FORMS_URL}/<string:form_name>')
class FetchForms(Resource):
    """
    This method returns all form entries in a dict.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self, form_name):

        form_data = frm.fetch_form(form_name)

        return form_data
