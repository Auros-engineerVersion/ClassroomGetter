import dataclasses
import json
import pickle

from src.nodes import INode

@dataclasses.dataclass
class SettingData:
    target_url: str
    user_email: str
    user_password: str
    
    #ログインしたままの状態で起動をするのならここに値をいれる
    profile_path: str
    profile_name: str
    profile: tuple = (profile_path, profile_name)
    
    loading_wait_time: int
    
    node_list: list[INode]
    
    def to_json(self):
        nodes_byte = pickle.dumps(self.node_list)
        json.dumps(self)
        