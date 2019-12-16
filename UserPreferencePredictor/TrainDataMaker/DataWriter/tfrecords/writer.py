import tensorflow as tf
import numpy as np


class TFRecordsWriter:
    def __init__(self, save_file_path: str):
        self.writer = tf.io.TFRecordWriter(save_file_path)

    def write(self, left_array: np.array, right_array: np.array, label: int):
        features = \
            tf.train.Features(
                feature={
                    'label':
                    tf.train.Feature(
                        int64_list=tf.train.Int64List(value=[label])),
                    'left_image':
                    tf.train.Feature(bytes_list=tf.train.BytesList(
                        value=[left_array.tobytes()])),
                    'right_image':
                    tf.train.Feature(bytes_list=tf.train.BytesList(
                        value=[right_array.tobytes()]))
                }
            )

        example = tf.train.Example(features=features)
        record = example.SerializeToString()
        self.writer.write(record)
