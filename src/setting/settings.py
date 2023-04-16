from __future__ import annotations
import pickle
from pathlib import Path

from setting_data import SettingData
from src.gui.window import Window

class Settings:
    DefaultSaveFolderPath = Path('./Save')
    
    def encryption(self) -> Settings:
        return self
    
    @staticmethod
    def Save(data: SettingData) -> None:
        #directoryが存在していれば
        if (data.save_folder_path.exists()):
            file_name = 'save.pkl'
            with open(data.save_folder_path.joinpath(file_name), 'wb') as f:
                pickle.dump(data, f)
        else:
            data.save_folder_path.mkdir(parents=True, exist_ok=True)
            Settings.Save(data) #Directoryが無ければもう一度行う
    
    @staticmethod
    def Load(folder_path: Path) -> SettingData:
        file_path = list(folder_path.glob('save.pkl')).pop()
        if (file_path.exists()):
            with open(file_path, 'rb') as f:
                return pickle.load(f)
        else:
            data = Settings.NewData()
            Settings.Save(data)
            return data
        
    @staticmethod
    def NewData() -> SettingData:
        user_info = Window.InputForm()
        return SettingData(*user_info)