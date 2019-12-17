from abc import ABCMeta, abstractclassmethod
from PIL.Image import Image
import typing


class ImageGenerator(metaclass=ABCMeta):
    @abstractclassmethod
    def generate(self, param: typing.Any) -> Image:
        pass
