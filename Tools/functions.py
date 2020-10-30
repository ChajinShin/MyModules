import numpy as np
import sys
import logging
import pandas as pd
from pathlib2 import Path
from typing import Union


class ProcessBar(object):
    def __init__(self, max_iter, prefix='', suffix='', bar_length=50):
        self.max_iter = max_iter
        self.prefix = prefix
        self.suffix = suffix
        self.bar_length = bar_length
        self.iteration = 0

    def step(self, other_info: str=None):
        self.iteration += 1

        percent = 100 * self.iteration / self.max_iter
        filled_length = int(round(self.bar_length * self.iteration) / self.max_iter)
        bar = '#' * filled_length + '-' * (self.bar_length - filled_length)
        msg = '\r{} [{}] {:.1f}% {}'.format(self.prefix, bar, percent, self.suffix)
        if other_info is not None:
            msg = msg + "  |   " + other_info
        sys.stdout.write(msg)
        if self.iteration == self.max_iter:
            sys.stdout.write('\n')
        sys.stdout.flush()


class Logger(object):
    def __init__(self, logging_file_dir: Path, log_level: str = 'log'):
        self.logger = logging.getLogger('log')
        self.logger.setLevel(log_level)
        handler = logging.FileHandler(logging_file_dir)
        self.logger.addHandler(handler)

    def change_log_level(self, log_level: str):
        self.logger.setLevel(log_level)

    def set_log(self, log: str):
        self.logger.info(log)
        print(log)


class PandasRecorder(object):
    def __init__(self):
        self.csv_recorder = pd.DataFrame()

    def write_data(self, row: Union[int, str, slice], col: Union[int, str, slice], data):
        if isinstance(row, str) and isinstance(col, str):
            self.csv_recorder.loc[row, col] = data
        elif isinstance(row, int) and isinstance(col, int):
            self.csv_recorder.iloc[row, col] = data

    def to_csv(self, path: Path):
        self.csv_recorder.to_csv(path)

