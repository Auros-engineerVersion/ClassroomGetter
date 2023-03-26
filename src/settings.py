import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv()

profile_path = os.environ.get('PROFILE_PATH')
profile_name = os.environ.get('PROFILE_NAME')