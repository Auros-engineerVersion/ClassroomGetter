import dataclasses
import json
import pickle

from src.nodes import INode

@dataclasses.dataclass
class SettingData:
    target_url: str
    user_email: str
    user_password: str
    
    #webdriverに関する設定
    loading_wait_time: int
    
    node_list: list[INode] = None
    
    #ログインしたままの状態で起動をするのならここに値をいれる
    profile_path: str = None
    profile_name: str = None
        
    def profile(self, change_profile_path: str = None, change_profile_name: str = None):
        if (change_profile_path != None or change_profile_name != None):
            self.profile_path = change_profile_path
            self.profile_name = change_profile_name
        
        return (self.profile_path, self.profile_name)