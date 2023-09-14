import os
import sys

sys.path.append(os.path.abspath('.'))

import tkinter as tk
import unittest
from pathlib import Path

from src.data import Node, SettingData
from src.my_util import *

from .caputer import *

current_path = lambda folder: Path(__file__).parent.joinpath(folder).resolve()
IMAGE_PATH = current_path('image')
SAVE_PATH = current_path('save')
WHITE_LIST = ['SettingFrame', 'FrontFrame']

def create_placeholder(annotation):
    if annotation is tk.Misc:
        return tk.Tk(screenName='test', baseName='testbase', className='testclass', useTk=1)
    elif annotation is SettingData:
        return SettingData(save_folder_path=CommentableObj(SAVE_PATH))
    elif annotation is Node:
        return Node('key', 'url', 1)
    elif annotation is str:
        return 'test'
    elif annotation is int:
        return 1
    else:
        if len(annotation.__subclasses__()) > 0:
            for cls in annotation.__subclasses__():
                return create_placeholder(cls)
        else:
            return annotation(*map(lambda x: create_placeholder(x), annotation.__init__.__annotations__.values()))
                            
def instance_of(cls):
    args = [create_placeholder(annotation) for annotation in cls.__init__.__annotations__.values()]
    return cls(*args)

class ImageTest(unittest.TestCase):    
    def setUp(self) -> None:
        if not IMAGE_PATH.exists():
            IMAGE_PATH.mkdir()
        
    def test_caputuer(self):
        from src.gui.custum_widgets import FrontFrame, SettingFrame
        caputuer_list = [FrontFrame, SettingFrame]
        for cls in caputuer_list:
            with self.subTest(cls.__name__):
                try:
                    ins = instance_of(cls)
                    ins.pack()
                    caputuer(ins, IMAGE_PATH.joinpath(f'{cls.__name__}.png'), overwrite=True)
                    self.assertTrue(True)
                except Exception as e:
                    self.fail(e)

if __name__ == '__main__':
    unittest.main()