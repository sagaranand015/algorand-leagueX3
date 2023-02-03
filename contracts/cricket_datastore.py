from typing import Final
from typing import Literal

from pyteal import *
from beaker import *
from beaker.lib.storage import Mapping

class PlayerRecord(abi.NamedTuple):
    all_players: abi.Field[abi.String]

class CricketDatastore(Application):

    sport: Final[ApplicationStateValue] = ApplicationStateValue(
        TealType.bytes, descr="Name of the Sport to which this datastore belongs", default=Bytes("CRICKET")
    )

    SEPARATOR = ";;;"
    team_records = Mapping(abi.DynamicBytes, PlayerRecord)

    @external(authorize=Authorize.only(Global.creator_address()))
    def add_team_players(self, team: abi.DynamicBytes,
        player_data: abi.DynamicBytes):
        """
        Adds a new team member to the team box
        """
        return Seq(
            (SEP := abi.String()).set(self.SEPARATOR),
            (final_p := abi.String()).set(Concat(player_data.get(), SEP.get())),
            contents := BoxGet(team.get()),
            BoxPut(team.get(), contents.value()),
            (new_data := abi.String()).set(Concat(contents.value(), final_p.get())),
            Assert(BoxDelete(team.get())),
            BoxPut(team.get(), new_data.get()),
        )

    @external(authorize=Authorize.only(Global.creator_address()))
    def get_team_players(self, team: abi.DynamicBytes, *, output: PlayerRecord):
        """
        Adds a new team member to the team box
        """
        return Seq(
            contents := BoxGet(team.get()),
            output.decode(contents.value()),
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
    CricketDatastore(version=8).dump("./artifacts")
