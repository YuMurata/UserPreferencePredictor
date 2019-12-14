from threading import Thread
import json
from .data_writer import DataWriter, DataWriterException, PlayerList
from pathlib import Path


class ScoredParamWriterException(DataWriterException):
    pass


class WriteThread(Thread):
    def __init__(self, scored_player_list: PlayerList,
                 save_file_path: str):
        super(WriteThread, self).__init__()
        self.scored_player_list = scored_player_list
        self.save_file_path = save_file_path

    def run(self):
        save_list = [player.to_dict()
                     for player in self.scored_player_list]

        with open(self.save_file_path, 'w') as fp:
            json.dump(save_list, fp, indent=4)


class ScoredParamWriter(DataWriter):
    SUFFIX = '.json'

    def __init__(self, save_file_path: str):
        if Path(save_file_path).suffix != self.SUFFIX:
            raise ScoredParamWriterException(f'suffix is not {self.SUFFIX}')

        self.save_file_path = save_file_path

    def write(self, scored_player_list: PlayerList):
        write_thread = WriteThread(scored_player_list, self.save_file_path)
        write_thread.start()
