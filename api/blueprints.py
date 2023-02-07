import typing
from flask import Blueprint

from .health import get_health_status
from .user import new_user_registration
from .leagues import LeaguesApi
from .squads import SquadsApi
from constants.constants import DATASTORE_APP_ID, LEAGUE_APP_ID

from cricket_datastore_client import CricketDatastoreClient
from leagueX3_client import LeagueX3Client

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

def get_leagues_blueprint():
    """
    Returns the blueprints for all leagues related endpoints
    """
    leagues_blueprint = Blueprint("leagues", __name__)
    ds_client = CricketDatastoreClient(int(DATASTORE_APP_ID))
    league_c = LeagueX3Client(int(LEAGUE_APP_ID))
    leagues_api = LeaguesApi(ds_client, league_c)
    
    @leagues_blueprint.route("/all", methods=["GET"])
    def _get_all_leagues_wrapper():
        return leagues_api.get_all_leagues()

    return leagues_blueprint

def get_squads_blueprint():
    """
    Returns the blueprints for all squads related endpoints
    """
    squads_blueprint = Blueprint("squads", __name__)
    ds_client = CricketDatastoreClient(int(DATASTORE_APP_ID))
    league_c = LeagueX3Client(int(LEAGUE_APP_ID))
    squads_api = SquadsApi(ds_client, league_c)

    @squads_blueprint.route("/all", methods=["GET"])
    def _get_all_user_squads_wrapper():
        return squads_api.get_all_user_squads()

    return squads_blueprint


def get_all_blueprints() -> typing.List[typing.Tuple[Blueprint, str]]:
    """
    Returns a list of all constructed blueprints to the Flask server app
    """
    ret = []
    ret.append((get_health_blueprint(), "/server"))
    ret.append((get_user_blueprint(), "/user"))
    ret.append((get_leagues_blueprint(), "/leagues"))
    ret.append((get_squads_blueprint(), "/squads"))
    return ret
