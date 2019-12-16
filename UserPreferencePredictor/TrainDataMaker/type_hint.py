import typing
from .player import Player

PlayerList = typing.List[Player]
TwoPlayer = typing.Tuple[Player, Player]
ParamDiffFunc = typing.Callable[[typing.Any, typing.Any], float]