from abc import ABCMeta, abstractclassmethod
from UserPreferencePredictor.TrainDataMaker import Player
import typing

PlayerList = typing.List[Player]


class DataWriterException(Exception):
    pass


class DataWriter(metaclass=ABCMeta):
    @abstractclassmethod
    def write(self, scored_player_list: PlayerList):
        pass
