from __future__ import annotations
import pickle
from pathlib import Path

from src.browser.browser_controls import BrowserControl
from src.data.setting_data import SettingData
from src.data.nodes import Node

class Settings:
    TARGET_URL = 'https://classroom.google.com/' #固定値
    
    @staticmethod
    def save(folder_path: Path, data: SettingData) -> None:
        #directoryが存在していれば
        if (folder_path.exists()):
            file_name = 'save.pkl'
            with open(folder_path.joinpath(file_name), 'wb') as f:
                pickle.dump(data, f)
        else:
            folder_path.mkdir(parents=True, exist_ok=True)
            Settings.save(data) #Directoryが無ければもう一度行う
    
    @staticmethod
    def load(folder_path: Path) -> SettingData:
        #def __create_and_save() -> SettingData:
        #    data = Settings.new_data()
        #    Settings.save(data)
        #    return data
            
        data = None
        file_path = folder_path.joinpath('save.pkl')
        if file_path.exists():
            with open(file_path, 'rb') as f:
                data = pickle.load(f)

        if data == None or type(data) != SettingData:
            return SettingData()
        else:
            return data
    
    @staticmethod
    def setup_data(data: SettingData, bc: BrowserControl):
        #node_listが何も設定されていないのなら値を取りに行く
        if not data.is_current_nodes():
            #プロファイルが指定されているかどうか
            #されていなければログインして指定する
            bc.move(Settings.TARGET_URL)
            if Settings.TARGET_URL not in bc.driver.current_url and data:
                bc.login_classroom(data)

            root = Node('Classroom', Settings.TARGET_URL, 0)
            root.initialize_tree()

            data.node_list = Node.Nodes
            Settings.save(SettingData.SETTINGFOLDER_PATH, data)