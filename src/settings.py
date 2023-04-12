import os
from sys import path
from dotenv import load_dotenv
from inspect import getmembers
from src.setting_data import SettingData
import pickle

class Settings:
    def __init__(self, data: SettingData):
        if ('.json' in self.save_file_path):
            raise ValueError('Path is incorrect. File extension must be .json')
        self.setting_data: SettingData = data
        
    @staticmethod
    def Save(file_path: str, *values):
        with open(file_path, 'ab') as f:
            pickle.dump([*values], f)
    
    @staticmethod
    def Load(path: str):
        with open(path, 'rb') as f:
            return pickle.load(f)
    
# この書き方をする場合、環境変数は「.env」という名前のファイルで、pythonコードと同階層、もしくは親階層に存在していること
load_dotenv()

PROFILE = (os.environ.get('PROFILE_PATH'), os.environ.get('PROFILE_NAME'))
TARGET_URL = os.environ.get('TARGET_URL')
LESSON_CLASS_NAME = os.environ.get('LESSON_CLASS_NAME')
SECTION_CLASS_NAME = os.environ.get('SECTION_CLASS_NAME')

WEBDRIVER_WAITTIME = os.environ.get('WEBDRIVER_WAITTIME')

def back_origin_enviroment():
    for v in getmembers():
        path.remove(v)