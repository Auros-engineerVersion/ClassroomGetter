from __future__ import annotations
import pickle
from pathlib import Path

from src.setting.setting_data import SettingData
from src.gui.window import Window

class Settings:
    DefaultSaveFolderPath = Path('./Save')
    
    def encryption(self) -> Settings:
        return self
    
    @staticmethod
    def save(data: SettingData) -> None:
        #directoryが存在していれば
        if (data.save_folder_path.exists()):
            file_name = 'save.pkl'
            with open(data.save_folder_path.joinpath(file_name), 'wb') as f:
                pickle.dump(data, f)
        else:
            data.save_folder_path.mkdir(parents=True, exist_ok=True)
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