import os
import yaml
import pathlib
import pandas as pd


class FileUtils:
    def __init__(self):
        self.config_path = pathlib.Path(os.getcwd()).parent.joinpath('config')

    def load_yaml(self, fn):
        fp = self.config_path.joinpath(fn)
        re = yaml.load(fp.open('r'), Loader=yaml.FullLoader)
        print('+ Load Yaml: ' + fp.as_posix())
        print('+ Load Cont: ' + str(re))
        return re

    @staticmethod
    def save_pd_csv(fn, colNames, data):
        data = pd.DataFrame(data, columns=colNames)
        data.to_csv(fn, encoding="utf-8", index=False)
        print('+ Save pd to csv: ' + fn)

