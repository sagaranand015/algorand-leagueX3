import typing
from flask import Blueprint

from .health import get_health_status
from .user import new_user_registration

"""
BLUEPRINTS FOR HEALTH API ENDPOINTS
"""


def get_health_blueprint():
    """
    Returns the blueprints for all server health related endpoints
    """
    health_blueprint = Blueprint("health", __name__)

    @health_blueprint.route("/health", methods=["GET"])
    def _get_health_wrapper():
        return get_health_status()

    return health_blueprint

def get_user_blueprint():
    """
    Returns the blueprints for user related endpoints
    """
    user_blueprint = Blueprint("user", __name__)

    @user_blueprint.route("/auth", methods=["POST"])
    def _get_user_auth_wrapper():
        return new_user_registration()

    return user_blueprint


def get_all_blueprints() -> typing.List[typing.Tuple[Blueprint, str]]:
    """
    Returns a list of all constructed blueprints to the Flask server app
    """
    ret = []
    ret.append((get_health_blueprint(), "/server"))
    ret.append((get_user_blueprint(), "/user"))
    return ret
