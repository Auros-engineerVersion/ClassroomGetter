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
        with open(path.parent, 'w') as f:
            json.dump(data, f, cls=MyClassEncoder, indent=4)
    else:
        raise FileNotFoundError('指定したパスはファイルではありません')
                
def load(path: Path) -> ISettingData:
    if not path.is_file():
        raise FileNotFoundError('指定したパスはファイルではありません')
    
    if path.exists() and path.suffix is '.json':
        return json.load(path, cls=MyClassDecoder)
    else:
        raise ValueError('指定したパスが存在しないか、jsonファイルではありません')
    
def try_load(path: Path = ISettingData.SETTINGFOLDER_PATH) -> ISettingData:
    try:
        return load(path.joinpath('setting.json'))
    except FileNotFoundError:
        return SettingData()
    
def setup_state(cfg: ISettingData):
    bc_data = BrowserControlData(cfg)
    if not cfg.is_current_nodes():
        #プロファイルが指定されているかどうか
        #されていなければログインして指定する
        move(bc_data, TARGET_URL)
        if TARGET_URL not in bc_data.driver.current_url and not cfg.is_default():
            login_classroom(bc_data, cfg)
            
    return cfg