from abc import ABCMeta
from pathlib import Path


class ISettingData(metaclass=ABCMeta):
    SETTING_FOLDER_PATH = Path('./Setting')
    TARGET_URL = 'https://classroom.google.com/' #固定値