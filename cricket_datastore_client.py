import json
import algosdk
from algosdk.mnemonic import *
from algosdk.atomic_transaction_composer import *
from algosdk.logic import get_application_address
from constants.constants import ROOT_ACCOUNT_MNEMONIC, ALGOD_HOST, ALGOD_TOKEN
from beaker import *
from contracts.cricket_datastore import CricketDatastore

# ACCOUNT_ADDRESS = to_public_key(ROOT_ACCOUNT_MNEMONIC)
ACCOUNT_SECRET = to_private_key(ROOT_ACCOUNT_MNEMONIC)
ACCOUNT_SIGNER = AccountTransactionSigner(ACCOUNT_SECRET)

WAIT_DELAY = 11


class CricketDatastoreClient:
    """
    Cricket Datastore client interfacing with the CricketDatastore deployed on the algorand blockchain
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
            CricketDatastore(),
            signer=ACCOUNT_SIGNER,
            app_id=self._app_id,
        )
        if app_id == 0:
            # Create  an app client for our app
            app_id, app_addr, _ = app_client.create()
            print(f"Created Cricket Datastore app at {app_id} {app_addr}")
            
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

    def get_team_members_call(self, team: str):
        sp = self._algo_client.suggested_params()
        sp.flat_fee = True
        sp.fee = 2000  # cover this and 1 inner transaction

        res = self._algo_app.call(
            CricketDatastore.get_team_players,
            team=bytes(team, encoding='utf-8'),
            suggested_params=sp,
            boxes=[(0, bytes(team, encoding='utf8'))]
        )
        print("======== get_team_members_call res is: ", res)
        print("======== get_team_members_call res.return_value is: ", res.return_value)
        print("======== get_team_members_call res.raw_value is: ", res.raw_value)
        print("======== get_team_members_call return string val is: ", type(res.raw_value), res.raw_value.decode())
        print("======== get_team_members_call res.tx_id is: ", res.tx_id)
        print("======== get_team_members_call res.tx_value is: ", res.tx_info)
        return res

    def set_team_members_call(self, team: str, player_data: str):
        sp = self._algo_client.suggested_params()
        sp.flat_fee = True
        sp.fee = 2000  # cover this and 1 inner transaction

        res = self._algo_app.call(
            CricketDatastore.add_team_players,
            team=bytes(team, encoding='utf-8'),
            player_data=bytes(player_data, encoding='utf-8'),
            suggested_params=sp,
            boxes=[(0, bytes(team, encoding='utf8'))]
        )
        print("======== set_team_members_call res is: ", res)
        print("======== set_team_members_call res.return_value is: ", res.return_value)
        print("======== set_team_members_call res.raw_value is: ", res.raw_value)
        print("======== set_team_members_call res.tx_id is: ", res.tx_id)
        print("======== set_team_members_call res.tx_value is: ", res.tx_info)
        return res

    def add_user_squad_call(self, squad_data: str):
        sp = self._algo_client.suggested_params()
        sp.flat_fee = True
        sp.fee = 2000  # cover this and 1 inner transaction

        # print("======= app addr is: ", addr, )

        res = self._algo_app.call(
            CricketDatastore.add_user_squad,
            squad_data=bytes(squad_data, encoding='utf-8'),
            suggested_params=sp,
            boxes=[[self._app_id, algosdk.encoding.decode_address(self._algo_app.sender)]]
        )
        print("======== add_user_squad_call res is: ", res)
        print("======== add_user_squad_call res.return_value is: ", res.return_value)
        print("======== add_user_squad_call res.raw_value is: ", res.raw_value)
        print("======== add_user_squad_call res.tx_id is: ", res.tx_id)
        print("======== add_user_squad_call res.tx_value is: ", res.tx_info)
        return res

    def get_user_squad_call(self):
        sp = self._algo_client.suggested_params()
        sp.flat_fee = True
        sp.fee = 2000  # cover this and 1 inner transaction

        res = self._algo_app.call(
            CricketDatastore.get_user_squads,
            suggested_params=sp,
            boxes=[[self._app_id, algosdk.encoding.decode_address(self._algo_app.sender)]]
        )
        print("======== get_user_squad_call res is: ", res)
        print("======== get_user_squad_call res.return_value is: ", res.return_value)
        print("======== get_user_squad_call res.raw_value is: ", res.raw_value)
        print("======== get_user_squad_call return string val is: ", type(res.raw_value), res.raw_value.decode())
        print("======== get_user_squad_call res.tx_id is: ", res.tx_id)
        print("======== get_user_squad_call res.tx_value is: ", res.tx_info)
        return res

if __name__ == "__main__":
    print("Starting deploy of the Cricket Datastore App(SC) on Algorand...")
    # cricketDatastore appId:156785317
    c = CricketDatastoreClient(156788073)
    c.get_application_state()
    c.get_application_address()
    print("================ STARTING METHOD CALLS =====================")
    c.set_team_members_call("team01", "ipfs://bafkreieu5hxn662idqac6htp7pyd6gmelkhopgmiw22l5dzhyfkrghy2le")
    print("================ NEXT CALL =====================")
    c.get_team_members_call("team01")
    print("================ NEXT CALL =====================")
    c.add_user_squad_call("ipfs://bafkreieu5hxn662idqac6htp7pyd6gmelkhopgmiw22l5dzhyfkrghy2le")
    print("================ NEXT CALL =====================")
    c.get_user_squad_call()
    print("================ NEXT CALL =====================")
    # c.get_emissions_rule()
    # print("================ CHANGE =====================")
    # try:
    #     c.is_business_compliant()
    # except Exception as e:
    #     print("============ EXCEPTION: ", e)
    #
    # try:
    #     c.create_compliance_token("SZ3K22H6MZ3A3ORYIVTAYMQMMBWVFOMJWXR3QCODNMJBQRIKBXN5PXX6AI")
    # except Exception as e:
    #     print("========= EXCEPTION IN CREATING COMPLIANCE NFT...", e)
    #     import traceback
    #     traceback.print_exc()

    # try:
    #     c.transfer_compliance_token_to_business("SZ3K22H6MZ3A3ORYIVTAYMQMMBWVFOMJWXR3QCODNMJBQRIKBXN5PXX6AI", 120023374)
    # except Exception as e:
    #     print("========= EXCEPTION IN TRANSFERRING TO BUSINESS...", e)
    #     import traceback
    #     traceback.print_exc()

    # try:
    #     c.print_asset_holding("SZ3K22H6MZ3A3ORYIVTAYMQMMBWVFOMJWXR3QCODNMJBQRIKBXN5PXX6AI", 120019312)
    # except Exception as e:
    #     print("========= EXCEPTION IN GETTING ACCOUNT INFO...", e)
    #     import traceback
    #     traceback.print_exc()

    # """
    # Reward Token interactions below!
    # """
    # # c.create_reward_tokens_supply()
    # try:
    #     c.transfer_reward_token_to_business(
    #         "C25IIJNW7VRRPNPEBKNBU2TR4SGIIH22EGYGE6FWXLGOV4GDQMN5VGTWB4",
    #         120027897,
    #     )
    # except Exception as e:
    #     print("========= EXCEPTION IN TRANSFERRING TO BUSINESS...", e)
    #     import traceback
    #
    #     traceback.print_exc()
