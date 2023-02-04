from typing import Final

from pyteal import *
from beaker import *
from beaker.lib.storage import Mapping

class UserLeagueData(abi.NamedTuple):
    # Define all data points containing a user's participation record
    squad_data: abi.Field[abi.DynamicBytes]
    pos_number: abi.Field[abi.Uint64]
    is_winner: abi.Field[abi.Bool]
    prize_val: abi.Field[abi.Uint64]
    prize_nft_id: abi.Field[abi.Uint64]

class LeagueX3(Application):

    league_name: Final[ApplicationStateValue] = ApplicationStateValue(
        TealType.bytes, descr="Name of the league"
    )
    league_metadata: Final[ApplicationStateValue] = ApplicationStateValue(
        TealType.bytes, descr="Link to the IPFS file containing the league metadata"
    )
    competition_name: Final[ApplicationStateValue] = ApplicationStateValue(
        TealType.bytes, descr="Name of the Competition/Match which is in progress"
    )

    user_participation = Mapping(abi.Address, UserLeagueData)

    @external(authorize=Authorize.only(Global.creator_address()))
    def bootstrap(
        self,
        league_name: abi.DynamicBytes,
        league_metadata: abi.DynamicBytes,
        competition_name: abi.DynamicBytes,
    ):
        return Seq(
            # Set league_name, league_metadata and competition_name
            self.league_name.set(league_name.get()),
            self.league_metadata.set(league_metadata.get()),
            self.competition_name.set(competition_name.get()),
        )

    @external
    def participate_with_user_squad(self, squad_data: abi.DynamicBytes, *, output: abi.Bool):
        """
        Adds a new squad link to the box storage keyed by user address
        """
        return Seq(
            (empty_string := abi.String()).set(""),
            Assert(And(self.league_name.exists(), Not(self.league_name.get() == empty_string.get())), comment="The app has not been bootstraped properly. League Name missing"),
            Assert(And(self.league_metadata.exists(), Not(self.league_metadata.get() == empty_string.get())), comment="The app has not been bootstraped properly. League Metadata missing"),
            Assert(And(self.competition_name.exists(), Not(self.competition_name.get() == empty_string.get())), comment="The app has not been bootstraped properly. Compeition name missing"),
            contents := BoxGet(Txn.sender()),
            If(contents.hasValue())
            .Then(
                output.set(False)
            ).Else(
                # Add the leaderboard entry to the user_participation mapping with a dummy position
                (dummy_pos_val := abi.Uint64()).set(int(0)),
                (dummy_win_val := abi.Bool()).set(False),
                (u_leaderboard := UserLeagueData()).set(squad_data, dummy_pos_val, dummy_win_val, dummy_pos_val, dummy_pos_val),
                self.user_participation[Txn.sender()].set(u_leaderboard),
                output.set(True)
            ),
        )
    
    @create
    def create(self):
        return self.initialize_application_state()

    @update(authorize=Authorize.only(Global.creator_address()))
    def update(self):
        return Approve()

    @opt_in
    def opt_in(self):
        return Approve()

if __name__ == "__main__":
    LeagueX3(version=8).dump("./leagueX3-artifacts")


