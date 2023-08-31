import sys, os
sys.path.append(os.path.abspath('.'))

import unittest
from pathlib import Path
import tkinter as tk

from .caputer import caputuer
from src.my_util import all_class_in_dir
from src.data import SettingData, Node

current_path = lambda folder: Path(__file__).parent.joinpath(folder).resolve()
IMAGE_PATH = current_path('image')
SAVE_PATH = current_path('save')
WHITE_LIST = ['SettingFrame', 'FrontFrame']

class ImageTest(unittest.TestCase):
    @staticmethod
    def __create_placeholder(annotation):
        if annotation is tk.Misc:
            return tk.Tk(screenName='test', baseName='testbase', className='testclass', useTk=1)
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
            caputuer(ins, IMAGE_PATH.joinpath(f'{cls.__name__}.png'), overwrite=True)
                            
if __name__ == '__main__':
    unittest.main()