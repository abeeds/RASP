from flask import Blueprint
from flask_restx import Resource
from server.globals import USERS_EP, TYPE, DATA, TITLE, MENU
from server.globals import USER_MENU_EP, RETURN, MAIN_MENU_EP


USER_ROUTE = Blueprint('USERS_EP', __name__)


@USER_ROUTE.route(f'{USERS_EP}')
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
            DATA: {
                "Callahan":
                {
                    "level": 0, "joined": '01/01/2019',
                },
                "Reddy":
                {
                    "level": 2, "joined": '02/02/2022',
                },
            },
            MENU: USER_MENU_EP,
            RETURN: MAIN_MENU_EP,
        }
