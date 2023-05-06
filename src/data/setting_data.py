from __future__ import annotations
from pathlib import Path
import dataclasses

NO_DATA = 'No Data'
@dataclasses.dataclass
class SettingData:
    user_email: str     = NO_DATA
    user_password: str  = NO_DATA

    #セーブフォルダの場所
    save_folder_path: Path = Path('./Save')

    #設定フォルダの場所
    setting_folder_path: Path = Path('./Save')
    
    #webdriverに関する設定
    loading_wait_time: int = 5
    
    node_list: set = None
        
    def __add__(self: SettingData, other: SettingData) -> SettingData:
        args = list(
            map(
                lambda value_1, value_2:
                    value_2 or value_1, #右の値を優先する
                vars(self).values(), vars(other).values()
            )
        )
        
        return SettingData(*args)
        
    def is_current_data(self):
        return\
            self.is_current_nodes()             and\
            not self.is_default()               and\
            self.is_current_user()              and\
            int(self.loading_wait_time) >= 0    and\
            self.setting_folder_path.exists()
        
    def is_current_nodes(self):
        return self.node_list != None and len(self.node_list) > 1
            
    def is_current_user(self):
        return '@' in self.user_email and len(self.user_password) > 0
            
    def is_default(self):
        return self.user_email + self.user_password in NO_DATA
        
    def profile(self) -> Path:
        return Path(self.setting_folder_path).absolute().joinpath('./ProfileData/Profile 1')