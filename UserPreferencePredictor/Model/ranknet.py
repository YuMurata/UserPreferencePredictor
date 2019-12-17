import tensorflow as tf
from pathlib import Path
import numpy as np
from PIL.Image import Image
from .grad_cam import GradCam
from .evaluate_network import build_evaluate_network
from .type_hint import ShapeTuple
import typing

ImageList = typing.List[Image]


class RankNet:
    SCOPE = 'predict_model'
    TRAINABLE_MODEL_FILE_NAME = 'trainable_model.h5'

    class ImageInfo:
        def __init__(self, image_shape: ShapeTuple):
            self.shape = image_shape
            self.width, self.height, self.channel = image_shape
            self.size = (self.width, self.height)

    def __init__(self, image_shape: ShapeTuple, *, use_vgg16: bool = False):
        self.image_info = RankNet.ImageInfo(image_shape)

        with tf.name_scope(RankNet.SCOPE):
            evaluate_network = build_evaluate_network(
                image_shape, use_vgg16=use_vgg16)
            self.grad_cam = GradCam(evaluate_network, self.image_info.size)

            left_input = tf.keras.Input(shape=image_shape)
            right_input = tf.keras.Input(shape=image_shape)

            left_output = evaluate_network(left_input)
            right_output = evaluate_network(right_input)

            concated_output = \
                tf.keras.layers.Concatenate()([left_output, right_output])

            with tf.name_scope('predictable_model'):
                self.predictable_model = tf.keras.Model(inputs=left_input,
                                                        outputs=left_output)
            with tf.name_scope('trainable_model'):
                self.trainable_model = tf.keras.Model(inputs=[left_input,
                                                              right_input],
                                                      outputs=concated_output)

            loss = \
                tf.keras.losses.SparseCategoricalCrossentropy(
                    from_logits=True)
            self.trainable_model.compile(optimizer='adam', loss=loss)

    def train(self, dataset: tf.data.Dataset, *,
              log_dir_path: str,
              valid_dataset: tf.data.Dataset, epochs: int = 10,
              steps_per_epoch: int = 30):
        callbacks = tf.keras.callbacks

        cb = []

        cb.append(tf.keras.callbacks.ModelCheckpoint(
            log_dir_path+'/weights.{epoch:02d}-{loss:.2f}-{val_loss:.2f}.h5',
            save_weights_only=True, monitor='val_loss', save_best_only=True))

        if log_dir_path is not None:
            cb.append(callbacks.TensorBoard(log_dir=log_dir_path,
                                            write_graph=True))

        self.trainable_model.fit(dataset, epochs=epochs,
                                 steps_per_epoch=steps_per_epoch,
                                 callbacks=cb, validation_data=valid_dataset,
                                 validation_steps=10)

    def save(self, save_dir_path: str):
        save_dir_path = Path(save_dir_path)
        save_dir_path.mkdir(parents=True, exist_ok=True)

        self.trainable_model.save_weights(
            str(Path(save_dir_path) /
                RankNet.TRAINABLE_MODEL_FILE_NAME))

    def load(self, load_file_path: str):
        self.trainable_model.load_weights(load_file_path)

    def save_model_structure(self, save_dir_path: str):
        save_dir_path = Path(save_dir_path)
        save_dir_path.mkdir(parents=True, exist_ok=True)

        tf.keras.utils.plot_model(self.predictable_model,
                                  str(save_dir_path/'predictable_model.png'),
                                  show_shapes=True)

        tf.keras.utils.plot_model(self.trainable_model,
                                  str(save_dir_path/'trainable_model.png'),
                                  show_shapes=True)

    def _image_to_array(self, image: Image):
        resized_image = image.resize(self.image_info.size)
        return np.asarray(resized_image).astype(np.float32)/255

    def predict(self, data_list: ImageList):
        image_array_list = np.array([self._image_to_array(data)
                                     for data in data_list])

        return self.predictable_model.predict(image_array_list)
