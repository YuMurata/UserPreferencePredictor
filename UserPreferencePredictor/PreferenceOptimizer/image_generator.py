from abc import ABCMeta, abstractclassmethod
from PIL.Image import Image


class ImageGenerator(metaclass=ABCMeta):
    @abstractclassmethod
    def generate(self, bit_list: list) -> Image:
        pass
