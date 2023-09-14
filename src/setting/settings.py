from __future__ import annotations

import pickle
from pathlib import Path

from ..browser import *
from ..data import BrowserControlData, SettingData
from ..interface import *

TARGET_URL = 'https://classroom.google.com/' #固定値
    
def save(folder_path: Path, data: ISettingData) -> None:
    #directoryが存在していれば
    if (folder_path.exists()):
        file_name = 'save.pkl'
        with open(folder_path.joinpath(file_name), 'wb') as f:
            pickle.dump(data, f)
    else:
        folder_path.mkdir(parents=True, exist_ok=True)
        save(data) #Directoryが無ければもう一度行う
    
def load(folder_path: Path) -> ISettingData:
    data = None
    file_path = folder_path.joinpath('save.pkl')
    if file_path.exists():
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
            
    if data == None or data.is_current_data() or isinstance(data, ISettingData) == False:
        raise TypeError('データが不正です')
    else:
        return data
    
def try_load(folder_path: Path = ISettingData.SETTINGFOLDER_PATH) -> ISettingData:
    try:
        return load(folder_path)
    except TypeError:
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