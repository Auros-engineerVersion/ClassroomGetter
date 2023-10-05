from __future__ import annotations

import json
from pathlib import Path

from ..browser import *
from ..data import BrowserControlData, SettingData
from ..interface import *
from .json_encoder import MyClassEncoder, MyClassDecoder

TARGET_URL = 'https://classroom.google.com/' #固定値

def save(path: Path, data):
    if path.is_file():
        with open(path, 'w') as f:
            json.dump(data, f, cls=MyClassEncoder, indent=4)
    else:
        raise FileNotFoundError('指定したパスはファイルではありません')
    
def try_save(path: Path, data):
    try:
        save(path, data)
    except FileNotFoundError:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()
        save(path, data)
                
def load(path: Path) -> ISettingData:
    if not path.is_file():
        raise FileNotFoundError('指定したパスはファイルではありません')
    
    if path.exists() and path.suffix == '.json':
        with open(path, 'r') as f:
            return json.load(f, cls=MyClassDecoder)
    else:
        raise FileNotFoundError('指定したパスが存在しないか、jsonファイルではありません')
    
def try_load(path: Path) -> ISettingData:
    try:
        return load(path)
    except FileNotFoundError:
        return SettingData()