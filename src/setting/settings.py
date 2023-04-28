from __future__ import annotations
import pickle
from pathlib import Path

from src.browser.browser_controls import BrowserControl
from src.data.setting_data import SettingData
from src.data.nodes import Node
from src.gui.window import Window

class Settings:
    TARGET_URL = 'https://classroom.google.com/' #固定値
    DEFAULT_SAVEFOLDER_PATH = Path('./Save')
    
    def encryption(self) -> Settings:
        return self
    
    @staticmethod
    def save(data: SettingData) -> None:
        #directoryが存在していれば
        if (data.setting_folder_path.exists()):
            file_name = 'save.pkl'
            with open(data.setting_folder_path.joinpath(file_name), 'wb') as f:
                pickle.dump(data, f)
        else:
            data.setting_folder_path.mkdir(parents=True, exist_ok=True)
            Settings.save(data) #Directoryが無ければもう一度行う
    
    @staticmethod
    def load(folder_path: Path) -> SettingData:
        def __create_and_save() -> SettingData:
            data = Settings.new_data()
            Settings.save(data)
            return data
            
        data = None
        file_path = folder_path.joinpath('save.pkl')
        if file_path.exists():
            with open(file_path, 'rb') as f:
                data = pickle.load(f)
                
        if data == None or type(data) != SettingData:
            return __create_and_save()
        else:
            return data
        
    @staticmethod
    def new_data() -> SettingData:
        user_info = Window.InputForm()
        return SettingData(*user_info)
    
    @staticmethod
    def validate_data(data: SettingData, bc: BrowserControl):
        #node_listが何も設定されていないのなら値を取りに行く
        if not data.is_current_data():
            #プロファイルが指定されているかどうか
            #されていなければログインして指定する
            bc.move(Settings.TARGET_URL)
            if (Settings.TARGET_URL not in bc.driver.current_url):
                bc.login_classroom(data)

            root = Node('Classroom', Settings.TARGET_URL, 0)
            root.initialize_tree()

            data.node_list = Node.Nodes
            Settings.save(data)