from threading import Thread
from .data_writer import DataWriter, DataWriterException, PlayerList
from pathlib import Path
from PIL import Image


class ScoredImageWriterException(DataWriterException):
    pass


class WriteThread(Thread):
    def __init__(self, scored_player_list: PlayerList,
                 save_dir_path: str):
        super(WriteThread, self).__init__()
        self.scored_player_list = scored_player_list
        self.save_dir_path = Path(save_dir_path)

    def run(self):
        for scored_player in self.scored_player_list:
            image = Image.open(scored_player.param)
            image.save(
                str(self.save_dir_path/f'{scored_player.score:0=3}.png'))


class ScoredImageWriter(DataWriter):
    def __init__(self, save_dir_path: str):
        self.save_dir_path = save_dir_path

        if not Path(save_dir_path).is_dir():
            raise ScoredImageWriterException(f'path is not dir')

    def write(self, scored_player_list: PlayerList):
        write_thread = WriteThread(scored_player_list, self.save_dir_path)
        write_thread.start()
