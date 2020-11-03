import os
import yaml
import pathlib

class FileUtils():
    def __init__(self):
        self.config_path = pathlib.Path(os.getcwd()).parent.joinpath('config')

    def load_yaml(self, fn):
        fp = self.config_path.joinpath(fn)
        re = yaml.load(fp.open('r'), Loader=yaml.FullLoader)
        print('+ Load Yaml: ' + fp.as_posix())
        print('+ Load Cont: ' + str(re))
        return re

