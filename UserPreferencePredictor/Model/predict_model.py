from abc import ABCMeta, abstractmethod
import typing
from PIL.Image import Image
import numpy as np


ShapeTuple = typing.Tuple[int, int, int]
ImageList = typing.List[Image]


class PredictModel(metaclass=ABCMeta):
    class ImageInfo:
        def __init__(self, image_shape: ShapeTuple):
            self.shape = image_shape
            self.width, self.height, self.channel = image_shape
            self.size = (self.width, self.height)

    def __init__(self, image_shape: ShapeTuple):
        self.image_info = PredictModel.ImageInfo(image_shape)

    def _image_to_array(self, image: Image) -> np.array:
        resized_image = image.resize(self.image_info.size)
        return np.asarray(resized_image).astype(np.float32)/255

    @abstractmethod
    def predict(self, data_list: ImageList) -> np.array:
        pass
