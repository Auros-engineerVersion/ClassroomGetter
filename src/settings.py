from setting_data import SettingData
import pickle

class Settings:
    def __init__(self, data: SettingData):
        if ('.json' in self.save_file_path):
            raise ValueError('Path is incorrect. File extension must be .json')
        self.setting_data: SettingData = data
        
    @staticmethod
    def Save(file_path: str, data: SettingData) -> None:
        with open(file_path, 'ab') as f:
            pickle.dump(data, f)
    
    @staticmethod
    def Load(file_path: str) -> SettingData:
        with open(file_path, 'rb') as f:
            return pickle.load(f)
        
    @staticmethod
    def SetData(window) -> SettingData:
        