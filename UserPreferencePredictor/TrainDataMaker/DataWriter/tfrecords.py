import tensorflow as tf
import numpy as np
from tqdm import tqdm

from .data_writer import DataWriter, DataWriterException, PlayerList
from threading import Thread
from pathlib import Path
import typing


SIZE_TUPLE = typing.Tuple[int, int]


class TFRecordsWriterException(DataWriterException):
    pass


class Writer:
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


class WriteThread(Thread):
    def __init__(self, scored_player_list: PlayerList, save_file_path: str,
                 resized_image_size: SIZE_TUPLE):
        super(WriteThread, self).__init__()
        self.scored_player_list = scored_player_list
        self.resized_image_size = resized_image_size
        self.save_file_path = save_file_path

    def run(self):
        scored_player_length = len(self.scored_player_list)

        data_length = 0

        for left_index in range(0, scored_player_length-1):
            for right_index in range(left_index+1, scored_player_length):
                left_score = self.scored_player_list[left_index]['score']
                right_score = self.scored_player_list[right_index]['score']

                if left_score != right_score:
                    data_length += 1

        writer = Writer(self.save_file_path)
        for i in range(scored_player_length):
            self.scored_player_list[i]['player'] = \
                self.scored_player_list[i]['player'].resize(
                    self.resized_image_size)

        progress = tqdm(total=data_length, desc='write tfrecords')
        for left_index in range(0, scored_player_length-1):
            for right_index in range(left_index+1, scored_player_length):
                left_scored_player = self.scored_player_list[left_index]
                right_scored_player = self.scored_player_list[right_index]

                left_array = np.asarray(left_scored_player['player'])
                right_array = np.asarray(right_scored_player['player'])

                left_score = left_scored_player['score']
                right_score = right_scored_player['score']

                try:
                    label = self._make_label(left_score, right_score)
                    writer.write(left_array, right_array, label)
                    progress.update()
                except ValueError:
                    pass

    def _make_label(self, left_score: float, right_score: float):
        if left_score > right_score:
            return 0

        elif right_score > left_score:
            return 1

        else:
            raise ValueError('score is same')


class TFRecordsWriter(DataWriter):
    SUFFIX = '.tfrecords'

    def __init__(self, save_file_path: str, resized_image_size: SIZE_TUPLE):
        if Path(save_file_path).suffix != self.SUFFIX:
            raise TFRecordsWriterException(f'suffix is not {self.SUFFIX}')

        self.save_file_path = save_file_path
        self.resized_image_size = resized_image_size

    def write(self, scored_player_list: PlayerList):
        write_thread = WriteThread(
            scored_player_list, self.save_file_path, self.resized_image_size)
        write_thread.start()
