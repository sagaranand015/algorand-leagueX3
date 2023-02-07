from http import HTTPStatus
from flask import jsonify

from flask import jsonify, request

from utils.utils import check_api_authorization

class SquadsApi:

    def __init__(self, ds_client, league_client) -> None:
        self.datastore_client = ds_client
        self.league_client = league_client

    def get_all_user_squads(self):
        """
        Endpoints for returning all user's squads data from the backend
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
            return (
                jsonify(dict(status=True, squads="ipfs://bafkreiebjpir2usfcjkpvwdk5lsbw5b6s2bumiulkijwicbfihk3idu4oi")),
                HTTPStatus.OK,
            )
        except Exception as e:
            return (
                jsonify(
                    jsonify(dict(status=False, message=str(e))),
                ),
                HTTPStatus.BAD_GATEWAY,
            )
