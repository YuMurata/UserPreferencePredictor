from UserPreferencePredictor.TrainDataMaker.Tournament import TournamentGame, Player, GameWin
import logging


class TestPlayer(Player):
    def __init__(self, param):
        super(TestPlayer, self).__init__(param)

    def decode(self):
        return self.param


if __name__ == "__main__":
    player_list = [TestPlayer(param) for param in [0, 0, 1, 100, 101, 102, 103, 104]]
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    game = TournamentGame(player_list, handler=handler)

    while not game.is_complete:
        left, right = game.new_match()

        if left.param > 10 and right.param > 10:
            winner = GameWin.BOTH_LOSE
        elif left.param < right.param:
            winner = GameWin.LEFT
        elif left.param > right.param:
            winner = GameWin.RIGHT
        else:
            winner = GameWin.BOTH_WIN

        game.compete(winner)

    for player in player_list:
        print(f'{player.param}: {player.score}')
