import os
from sys import path
from dotenv import load_dotenv
from inspect import getmembers
from dataclasses import dataclass
import pickle

@dataclass(frozen=True)
class Settings:
    save_file_path: str
    
    def __post_init__(self):
        if (not '.dat' in self.save_file_path):
            raise ValueError('Path is incorrect. File extension must be .dat')
        
        Settings.Load(self.save_file_path)
        
    @staticmethod
    def Save(file_path: str, *values):
        binaries = map(pickle.dumps, values)
        with open(file_path, 'wb') as f:
            f.writelines(binaries)
    
    @staticmethod
    def Load(path: str):
        try:
            line = open(path, 'rb').readlines()
        finally:
            file.close()
        pass
    
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