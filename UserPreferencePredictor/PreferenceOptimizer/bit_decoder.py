from abc import ABCMeta, abstractclassmethod
import typing


class BitDecoder(metaclass=ABCMeta):
    @abstractclassmethod
    def decode(self, bit_list: list) -> typing.Any:
        pass
