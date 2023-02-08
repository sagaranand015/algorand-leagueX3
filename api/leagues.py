from http import HTTPStatus
from flask import jsonify
from flask import jsonify, request

from utils.utils import check_api_authorization
from cricket_datastore_client import CricketDatastoreClient
from leagueX3_client import LeagueX3Client


class LeaguesApi:

    def __init__(self, ds_client: CricketDatastoreClient, league_client: LeagueX3Client) -> None:
        self.datastore_client = ds_client
        self.league_client = league_client

    def get_all_leagues(self):
        """
        Endpoints for returning all leagues data from the backend
        """
        try:
            return (
                jsonify(dict(status=True, leagues="ipfs://bafkreiebjpir2usfcjkpvwdk5lsbw5b6s2bumiulkijwicbfihk3idu4oi")),
                HTTPStatus.OK,
            )
        except Exception as e:
            return (
                jsonify(
                    jsonify(dict(status=False, message=str(e))),
                ),
                HTTPStatus.BAD_GATEWAY,
            )

    def participate_with_user_address(self):
        """
        Endpoints for returning all leagues data from the backend
        """
        try:
            auth_header = request.headers.get("Authorization")
            auth_validated, auth_token = check_api_authorization(auth_header)
            if not auth_validated:
                return (
                    jsonify(dict(status=False, message="Invalid Auth")),
                    HTTPStatus.BAD_REQUEST,
                )

            user_addr = auth_token['sub']
            req = request.get_json()
            try:
                league_data = req["league_data"]
                squad_data = req["squad_data"]
            except KeyError as e:
                return (
                    jsonify(
                        dict(
                            status=False,
                            message="Invalid Payload. Pass Leagues Data and Squad Data both",
                        )
                    ),
                    HTTPStatus.BAD_REQUEST,
                )

            resp = self.league_client.participate_with_user_squad_call(user_addr, league_data, squad_data)
            if resp and resp.return_value:
                ret_league_data = ''.join([chr(x) for x in resp.return_value[0]])
                ret_squad_data = ''.join([chr(x) for x in resp.return_value[0]])
                return (
                    jsonify(dict(status=True, league_data=ret_league_data, squad_data=ret_squad_data)),
                    HTTPStatus.OK,
                )

            print("non valid response from leagueClient: ", resp, resp.return_value)
            return (
                    jsonify(dict(status=False, league_data=None, squad_data=None)),
                    HTTPStatus.BAD_REQUEST,
                )
        except Exception as e:
            import traceback
            traceback.print_exc()
            return (
                jsonify(
                    jsonify(dict(status=False, message=str(e))),
                ),
                HTTPStatus.BAD_GATEWAY,
            )
