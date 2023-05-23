from __future__ import annotations
from pathlib import Path
from typing import ClassVar
import dataclasses

NO_DATA = 'No Data'

@dataclasses.dataclass
class SettingData:
    SETTINGFOLDER_PATH: ClassVar[Path] = Path('./Setting')
    user_email: str     = NO_DATA
    user_password: str  = NO_DATA

    #セーブフォルダの場所
    save_folder_path: Path = Path('./Save').absolute()
    
    #webdriverに関する設定
    loading_wait_time: int = 5
    
    nodes: set = None
        
    def __add__(self: SettingData, other: SettingData) -> SettingData:
        args = list(
            map(
                lambda value_1, value_2:
                    value_2 or value_1, #右の値を優先する
                vars(self).values(), vars(other).values()
            )
        )
        
        return SettingData(*args)
    
    @property
    def profile(self):
        return (self.user_email, self.user_password)
    
    @profile.setter
    def profile(self, other: tuple[str, str]):
        self.user_email = other[0]
        self.user_password = other[1]
        
    def is_current_data(self):
        return\
            not self.is_default()               and\
            self.is_current_nodes()             and\
            self.is_current_user()              and\
            int(self.loading_wait_time) >= 0    and\
            self.save_folder_path.exists()
        
    def is_current_nodes(self):
        return self.nodes != None and len(self.nodes) > 1
            
    def is_current_user(self):
        return '@' in self.user_email and len(self.user_password) > 0
            
    def is_default(self):
        return NO_DATA in self.user_email + self.user_password
    
    @staticmethod
    def profile_path():
        return Path(SettingData.SETTINGFOLDER_PATH).absolute().joinpath('./ProfileData/Profile 1')