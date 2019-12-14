from .ranknet import RankNet
from .dataset import make_dataset, DatasetException
from .exception import ModelException
from argparse import ArgumentParser

from datetime import datetime
from pathlib import Path
from UserPreferencePredictor.config.tfrecords \
    import SUFFIX, DATASET_TYPE_LIST, TRAIN, VALIDATION


class TrainModelException(ModelException):
    pass


def _make_summary_dir(summary_dir_path: str):
    now = datetime.now()
    path = Path(summary_dir_path)/'{0:%m%d}'.format(now)/'{0:%H%M}'.format(now)

    if path.exists():
        path = Path(str(path)+'_{0:%S}'.format(now))

    path.mkdir(parents=True)

    return str(path)


def _make_dataset_path_dict(dataset_dir_path: str):
    dataset_dir_path = Path(dataset_dir_path)

    if not dataset_dir_path.exists():
        raise FileNotFoundError('フォルダが見つかりませんでした')
    elif not dataset_dir_path.is_dir():
        raise NotADirectoryError

    dataset_path_dict = \
        {key: str(dataset_dir_path/(key+SUFFIX))
         for key in DATASET_TYPE_LIST}
    return dataset_path_dict


def _get_args():
    parser = ArgumentParser()

    parser.add_argument('-d', '--dataset_dir_path', required=True)
    parser.add_argument('-s', '--summary_dir_path', required=True)
    parser.add_argument('-l', '--load_dir_path')
    parser.add_argument('-j', '--use_jupyter', action='store_true')

    args = parser.parse_args()

    for arg in vars(args):
        print(f'{str(arg)}: {str(getattr(args, arg))}')

    return args


def train_model(get_summary_dir_path_func, dataset_dir_path: str, image_shape: tuple, *, batch_size: int = 100, epochs: int = 20, load_dir_path=None):
    trainable_model = RankNet(image_shape)

    if load_dir_path:
        try:
            trainable_model.load(load_dir_path)
        except ValueError as e:
            raise TrainModelException(e)

    dataset_path_dict = _make_dataset_path_dict(dataset_dir_path)

    try:
        dataset = {key: make_dataset(dataset_path_dict[key], batch_size, key, image_shape)
                   for key in [TRAIN, VALIDATION]}
    except DatasetException as e:
        raise TrainModelException(e)

    summary_dir_path = get_summary_dir_path_func()
    trainable_model.train(dataset[TRAIN], log_dir_path=summary_dir_path,
                          valid_dataset=dataset[VALIDATION], epochs=epochs, steps_per_epoch=30)

    trainable_model.save(summary_dir_path)

