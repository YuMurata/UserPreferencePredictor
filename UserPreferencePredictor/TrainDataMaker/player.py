from abc import ABCMeta, abstractclassmethod
import typing


class Player(metaclass=ABCMeta):
    def __init__(self, param: typing.Any, score: int = 1):
        self.param = param
        self.score = score

    @abstractclassmethod
    def decode(self):
        pass

    def score_up(self) -> typing.NoReturn:
        self.score *= 2

    def to_dict(self) -> dict:
        return {'score': self.score, 'param': self.param}
