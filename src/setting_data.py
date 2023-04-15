from __future__ import annotations
from os import sep
from pathlib import Path
import dataclasses

@dataclasses.dataclass
class SettingData:
    user_email: str
    user_password: str

    #セーブフォルダの場所
    save_folder_path: Path = Path('./Save')
    
    #webdriverに関する設定
    loading_wait_time: int = 5
    
    node_list: list = None
        
    def _add_(self: SettingData, other: SettingData) -> SettingData:
        args = list(
            map(
                lambda value_1, value_2:
                    value_1 or value_2,
                vars(self).values(), vars(other).values()
            )
        )
        
        return SettingData(*args)
        
    def profile(self) -> Path:
        return Path(self.save_folder_path).absolute().joinpath('./ProfileData/Profile 1')