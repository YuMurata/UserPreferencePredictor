from enum import Enum, auto
from random import sample
import logging
from .type_hint import PlayerList, TwoPlayer
import typing


class TournamentException(Exception):
    pass


class RoundException(TournamentException):
    pass


class MatchException(TournamentException):
    pass


class CompeteException(TournamentException):
    pass


class GameWin(Enum):
    LEFT = auto()
    RIGHT = auto()
    BOTH_WIN = auto()
    BOTH_LOSE = auto()


class Tournament:
    def __init__(self, player_list: PlayerList, *,
                 handler: logging.StreamHandler = None):
        self.logger = logging.getLogger('Tournament')
        self.logger.setLevel(logging.INFO)

        if handler is not None:
            self.logger.addHandler(handler)

        self.player_list = player_list
        self.current_player_index_list = list(range(len(player_list)))
        self.old_player_num = len(player_list)

        self.current_player_index_list = \
            sample(self.current_player_index_list,
                   len(self.current_player_index_list))

        self.next_player_index_list = []

        self.is_match = False
        self.is_complete = False

        self.round_count = 1
        self.match_count = 0

        self.logger.debug('init')

        self.logger.info(f'--- game start ---')
        self._log_start_round()

    def _log_start_round(self):
        self.logger.info(f'start {self.round_count}th round')
        self.logger.info(
            f'--- current player index: {self.current_player_index_list} ---')
        score_list = [player.score for player in self.player_list]
        self.logger.info(f'--- score: {score_list} ---')

    def _new_round(self):
        if len(self.current_player_index_list) >= 2:
            raise RoundException

        for index in self.current_player_index_list:
            self.player_list[index].score_up()

        self.next_player_index_list.extend(self.current_player_index_list)
        self.current_player_index_list = \
            sample(self.next_player_index_list,
                   len(self.next_player_index_list))
        self.next_player_index_list.clear()

        self.old_player_num = len(self.current_player_index_list)

        self.round_count += 1
        self.match_count = 0

        self._log_start_round()

    def new_match(self) -> TwoPlayer:
        if self.is_match:
            raise MatchException('match is already ready')

        if self.is_complete:
            raise MatchException('game is already over')

        self.logger.info(f'--- new match start ---')

        if len(self.current_player_index_list) >= 2:
            self.left_player_index = self.current_player_index_list.pop()
            self.right_player_index = self.current_player_index_list.pop()
            self.is_match = True

            self.match_count += 1

            left_player = \
                self.player_list[self.left_player_index]
            right_player = \
                self.player_list[self.right_player_index]

            self.logger.info(
                f'--- left player index: {self.left_player_index} ---')
            self.logger.info(
                f'--- right player index: {self.right_player_index} ---')

            return left_player, right_player

        else:
            self._new_round()
            return self.new_match()

    def compete(self, winner: GameWin) -> typing.NoReturn:
        if not self.is_match:
            raise CompeteException('match is not ready yet')

        if self.is_complete:
            raise CompeteException('game is already over')

        def _win(winner_index: int):
            self.player_list[winner_index].score_up()
            self.next_player_index_list.append(winner_index)

        if winner == GameWin.BOTH_WIN:
            _win(self.left_player_index)
            _win(self.right_player_index)
        elif winner == GameWin.LEFT:
            _win(self.left_player_index)
        elif winner == GameWin.RIGHT:
            _win(self.right_player_index)

        self.logger.info(f'--- winner: {winner.name} ---')
        self.is_match = False

        is_no_current_player = len(self.current_player_index_list) == 0
        is_only_one_winner = len(self.next_player_index_list) == 1
        is_championship = is_no_current_player and is_only_one_winner

        remaining_player_num = len(
            self.next_player_index_list)+len(self.current_player_index_list)
        is_player_no_change = remaining_player_num == self.old_player_num

        if is_championship or is_player_no_change:
            self.is_complete = True

            if is_player_no_change:
                for index in self.current_player_index_list:
                    self.player_list[index].score_up()

    @property
    def get_match_num(self):
        current_match_num = len(self.current_player_index_list)-1
        next_match_num = len(self.next_player_index_list)
        return current_match_num+next_match_num
