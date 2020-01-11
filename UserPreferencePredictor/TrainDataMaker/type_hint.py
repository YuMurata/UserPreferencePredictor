import typing
from .Tournament.Tournament import Player

PlayerList = typing.List[Player]
ParamDiffFunc = typing.Callable[[typing.Any, typing.Any], float]