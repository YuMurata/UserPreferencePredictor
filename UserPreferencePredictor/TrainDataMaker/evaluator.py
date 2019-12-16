from .type_hint import PlayerList, ParamDiffFunc


class Evaluator:
    def __init__(self, scored_player_list: PlayerList,
                 param_diff_func: ParamDiffFunc):
        self.scored_player_list = scored_player_list
        self.param_diff_func = param_diff_func

    def evaluate(self, param) -> float:
        return sum([player.score*self.param_diff_func(param, player.param)
                    for player in self.scored_player_list])
