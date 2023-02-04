import json
import algosdk
from algosdk.mnemonic import *
from algosdk.atomic_transaction_composer import *
from algosdk.logic import get_application_address
from constants.constants import ROOT_ACCOUNT_MNEMONIC, ALGOD_HOST, ALGOD_TOKEN
from beaker import *
from contracts.leagueX3 import LeagueX3

# ACCOUNT_ADDRESS = to_public_key(ROOT_ACCOUNT_MNEMONIC)
ACCOUNT_SECRET = to_private_key(ROOT_ACCOUNT_MNEMONIC)
ACCOUNT_SIGNER = AccountTransactionSigner(ACCOUNT_SECRET)


class LeagueX3Client:
    """
    LeagueX3 client interfacing with the CricketDatastore deployed on the algorand blockchain
    """

    def __init__(self, app_id: int = 0):
        self._algo_client = None
        self._algo_app = None
        self._app_id = app_id
        self._app_address = None

        self.build_client(app_id)

    def get_app_id(self):
        return self._app_id

    def get_app_address(self):
        return self._app_address

    def build_algo_client(self):
        algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_HOST)
        return algod_client

    def get_algo_app_client(self, app_id: int):
        app_client = client.ApplicationClient(
            self._algo_client,
            LeagueX3(),
            signer=ACCOUNT_SIGNER,
            app_id=self._app_id,
        )
        if app_id == 0:
            # Create  an app client for our app
            app_id, app_addr, _ = app_client.create()
            print(f"Created LeagueX3 app at {app_id} {app_addr}")
            
            app_client.fund(1 * consts.algo)
            print("Funded app")
            app_client.opt_in()
            print("Opted in")
        else:
            app_addr = get_application_address(app_id)
        self._app_id = app_id
        self._app_address = app_addr
        return app_client

    def build_client(self, app_id: int):
        self._algo_client = self.build_algo_client()
        self._algo_app = self.get_algo_app_client(app_id)
        assert all(
            [
                self._algo_client,
                self._algo_app,
                self._app_id,
                self._app_address,
            ]
        )

    def get_application_state(self):
        app_state = self._algo_client.dele
        print(f"Current app state:{app_state}")
        return app_state

    def get_application_state(self):
        app_state = self._algo_app.get_application_state()
        print(f"Current app state:{app_state}")
        return app_state

    def get_application_address(self):
        app_addr = get_application_address(self._app_id)
        print(f"Current app address:{app_addr}")
        return app_addr

    def bootstrap_app_call(self, league_name: str, league_metadata: str, competition_name: str):
        sp = self._algo_client.suggested_params()
        sp.flat_fee = True
        sp.fee = 1000  # cover this and 1 inner transaction
        res = self._algo_app.call(
            LeagueX3.bootstrap,
            league_name=bytes(league_name, encoding='utf-8'),
            league_metadata=bytes(league_metadata, encoding='utf-8'),
            competition_name=bytes(competition_name, encoding='utf-8'),
            suggested_params=sp,
        )
        print("======== bootstrap_app_call res is: ", res)
        print("======== bootstrap_app_call res.return_value is: ", res.return_value)
        print("======== bootstrap_app_call res.raw_value is: ", res.raw_value)
        print("======== bootstrap_app_call res.tx_id is: ", res.tx_id)
        print("======== bootstrap_app_call res.tx_value is: ", res.tx_info)
        return res

    def participate_with_user_squad_call(self, squad_data: str):
        sp = self._algo_client.suggested_params()
        sp.flat_fee = True
        sp.fee = 1000  # cover this and 1 inner transaction
        res = self._algo_app.call(
            LeagueX3.participate_with_user_squad,
            squad_data=bytes(squad_data, encoding='utf-8'),
            suggested_params=sp,
            boxes=[[self._app_id, algosdk.encoding.decode_address(self._algo_app.sender)]]
        )
        print("======== participate_with_user_squad_call res is: ", res)
        print("======== participate_with_user_squad_call res.return_value is: ", res.return_value)
        print("======== participate_with_user_squad_call res.raw_value is: ", res.raw_value)
        print("======== participate_with_user_squad_call res.tx_id is: ", res.tx_id)
        print("======== participate_with_user_squad_call res.tx_value is: ", res.tx_info)
        return res

if __name__ == "__main__":
    league_name = "LudhianaLeague01"
    league_metadata = "ipfs://bafkreieu5hxn662idqac6htp7pyd6gmelkhopgmiw22l5dzhyfkrghy2le"
    competition_name = "LudhianaLocalMatch01"
    print(f"Starting deploy of the LeagueX3 App(SC) on Algorand with {league_name}, {league_metadata}, {competition_name}")
    # LeagueX3 appId:
    c = LeagueX3Client(156872629)
    c.get_application_state()
    c.get_application_address()
    print("================ BOOTSTRAPCALLING CALL =====================")
    c.bootstrap_app_call(league_name, league_metadata, competition_name)
    print("================ participate_with_user_squad_call CALL =====================")
    c.participate_with_user_squad_call("ipfs://bafkreieu5hxn662idqac6htp7pyd6gmelkhopgmiw22l5dzhyfkrghy2le")
    print("================ NEXT CALL =====================")