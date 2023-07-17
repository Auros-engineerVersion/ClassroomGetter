import sys, os
sys.path.append(os.path.abspath('.'))

import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
import caputer

from my_util import *
from src.data.setting_data import SettingData
from src.data.nodes import Node

IMAGE_PATH = Path('test/gui_tests/images')
SAVE_PATH = Path('test/gui_tests/save')
WHITE_LIST = ['SettingFrame', 'FrontFrame']

class ImageTest(unittest.TestCase):
    @staticmethod
    def __create_placeholder(annotation):
        if annotation is tk.Misc:
            return tk.Tk()
        elif annotation is SettingData:
            return SettingData(save_folder_path=SAVE_PATH.absolute())
        elif annotation is Node:
            return Node('key', 'url', 1)
        elif annotation is str:
            return 'test'
        elif annotation is int:
            return 1
        else:
            if len(annotation.__subclasses__()) > 0:
                for cls in annotation.__subclasses__():
                    return ImageTest.__create_placeholder(cls)
            else:
                return annotation(*map(lambda x: ImageTest.__create_placeholder(x), annotation.__init__.__annotations__.values()))
        
    def setUp(self) -> None:
        if not IMAGE_PATH.exists():
            IMAGE_PATH.mkdir()
        
    def test_caputuer(self):
        for cls in filter(lambda cls: cls.__name__ in WHITE_LIST, all_class_in_dir(Path('src/gui'))):
            ins = cls(*map(lambda x: self.__create_placeholder(x), cls.__init__.__annotations__.values()))
            ins.pack()
            caputer.caputuer(ins, IMAGE_PATH.joinpath(f'{cls.__name__}.png'), overwrite=True)
                
if __name__ == '__main__':
    unittest.main()