import UserPreferencePredictor.TrainDataMaker.Tournament as Tournament
import logging
import random


class NumberPlayer(Tournament.Player):
    def __init__(self, param):
        super().__init__(param)

    def decode(self):
        return self.param


def _param_diff(param, target_param):
    return 1/(abs(param-target_param)+1)


if __name__ == "__main__":
    random.seed(0)

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)

    param_list = list(range(10))
    player_list = [NumberPlayer(param) for param in param_list]

    game = Tournament.TournamentGame(player_list, handler=handler)

    while not game.is_complete:
        left, right = game.new_match()

        if left.param > 5 and right.param > 5:
            winner = Tournament.GameWin.BOTH_LOSE
        elif left.param < 3 and right.param < 3:
            winner = Tournament.GameWin.BOTH_WIN
        elif left.param < right.param:
            winner = Tournament.GameWin.LEFT
        elif left.param > right.param:
            winner = Tournament.GameWin.RIGHT

        game.compete(winner)

    print('param| score')
    for player in game.player_list:
        print(f'{player.param:>5}| {player.score:<.3f}')

    evaluator = Tournament.Evaluator(game.player_list, _param_diff)

    print('param| evaluate')
    for param in param_list:
        print(f'{param:>5}| {evaluator.evaluate(param):<.3f}')
