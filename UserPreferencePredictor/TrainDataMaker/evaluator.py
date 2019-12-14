import typing
from .player import Player

ParamDiffFunc = typing.Callable[[typing.Any, typing.Any], float]


class Evaluator:
    def __init__(self, scored_player_list: typing.List[Player],
                 param_diff_func: ParamDiffFunc):
        self.scored_player_list = scored_player_list
        self.param_diff_func = param_diff_func

    def evaluate(self, param) -> float:
        return sum([player.score*self.param_diff_func(param, player.param)
                    for player in self.scored_player_list])
