from __future__ import annotations
from pathlib import Path
import dataclasses

@dataclasses.dataclass
class SettingData:
    user_email: str
    user_password: str

    #セーブフォルダの場所
    setting_folder_path: Path = Path('./Save')
    
    #webdriverに関する設定
    loading_wait_time: int = 5
    
    node_list: set = None
        
    def __add__(self: SettingData, other: SettingData) -> SettingData:
        args = list(
            map(
                lambda value_1, value_2:
                    value_1 or value_2,
                vars(self).values(), vars(other).values()
            )
        )
        
        return SettingData(*args)
        
    def is_current_data(self):
        return\
            self.node_list != None         and\
            len(self.node_list) > 1             and\
            '@' in self.user_email         and\
            len(self.user_password) > 0    and\
            self.loading_wait_time >= 0    and\
            self.setting_folder_path.exists()
        
    def profile(self) -> Path:
        return Path(self.setting_folder_path).absolute().joinpath('./ProfileData/Profile 1')