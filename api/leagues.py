from http import HTTPStatus
from flask import jsonify


class LeaguesApi:

    def __init__(self, ds_client, league_client) -> None:
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
