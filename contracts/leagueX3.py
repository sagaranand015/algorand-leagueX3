from typing import Final

from pyteal import *
from beaker import *
from beaker.lib.storage import Mapping

class LeaderboardPosition(abi.NamedTuple):
    # Define leaderboard position params here
    pos_number: abi.Field[abi.Uint64]
    is_winner: abi.Field[abi.Bool]
    prize_val: abi.Field[abi.Uint64]
    prize_nft_id: abi.Field[abi.Uint64]

class UserSquad(abi.NamedTuple):
    # Define Squad with with the user is participating in the league
    squad_data: abi.Field[abi.String]

class LeagueX3(Application):

    competition_name: Final[ApplicationStateValue] = ApplicationStateValue(
        TealType.bytes, descr="Name of the Competition/Match which is in progress"
    )
    competition_start_time: Final[ApplicationStateValue] = ApplicationStateValue(
        TealType.uint64, descr="Start time in UTC epoch timestamp for the competition"
    )
    competition_end_time: Final[ApplicationStateValue] = ApplicationStateValue(
        TealType.uint64, descr="End time in UTC epoch timestamp for the competition"
    )

    user_squads = Mapping(abi.Address, UserSquad)
    user_leaderboard = Mapping(abi.Address, LeaderboardPosition)


