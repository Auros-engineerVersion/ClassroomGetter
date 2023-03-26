import os
from sys import path
from dotenv import load_dotenv
from inspect import getmembers

# この書き方をする場合、環境変数は「.env」という名前のファイルで、pythonコードと同階層、もしくは親階層に存在していること
load_dotenv()

PROFILE_PATH = os.environ.get('PROFILE_PATH')
PROFILE_NAME = os.environ.get('PROFILE_NAME')

def back_origin_enviroment():
    for v in getmembers():
        path.remove(v)