from __future__ import annotations

from dataclasses import *
from pathlib import Path
from typing import ClassVar

from .nodes import Node
from ..interface import ISettingData
from ..my_util import CommentableObj

NO_DATA = 'No Data'
TARGET_URL = 'https://classroom.google.com/' #固定値

@dataclass
class SettingData(ISettingData):
    #----------------通常のデータ------------------------
    user_email: CommentableObj = field(default_factory=lambda:CommentableObj(NO_DATA, 'ユーザーのメールアドレス'))
    user_password: CommentableObj = field(default_factory=lambda:CommentableObj(NO_DATA, 'ユーザーアカウントのパスワード'))

    #セーブフォルダの場所
    save_folder_path: CommentableObj = field(default_factory=lambda:CommentableObj(Path('./Save').absolute(), '入手したファイルを保存する場所'))
    
    #ページの読み込みを待つ時間
    loading_wait_time: CommentableObj = field(default_factory=lambda:CommentableObj(5, 'ページの読み込みを待つ時間'))
    
    web_driver_options_data: CommentableObj = field(default_factory=lambda:CommentableObj('--headless, --disable-gpu, --blink-settings=imagesEnabled=false, --ignore-certificate-error, --ignore-certificate-error', 'Web Driverが起動する際のオプション'))
    
    #----------------保存されたデータ--------------------
    nodes: set = field(default_factory=set)
    
#region 定数
    SETTINGFOLDER_PATH: ClassVar[Path] = Path('./Setting')
#endregion
        
    def __add__(self: SettingData, other: SettingData) -> SettingData:
        args = list(
            map(
                lambda value_1, value_2:
                    value_2 or value_1, #右の値を優先する
                vars(self).values(), vars(other).values()
            )
        )
        
        return SettingData(*args)
    
    def __post_init__(self):
        self.nodes.add(Node('Classroom', TARGET_URL, 0))
    
    @property
    def profile(self):
        return self.user_email, self.user_password
    
    @profile.setter
    def profile(self, other: tuple[str, str]):
        self.user_email.value = other[0]
        self.user_password.value = other[1]
        
    @property
    def web_driver_options(self):
        return CommentableObj(
            value=self.web_driver_options_data.value.replace(' ', '').replace('\n', '').split(','), 
            comment=self.web_driver_options_data.comment)
    
    @property
    def editable_data(self):
        return {
            'user_email': self.user_email,
            'user_password': self.user_password,
            'save_folder_path': self.save_folder_path,
            'loading_wait_time': self.loading_wait_time,
            'web_driver_options': self.web_driver_options_data
        }
        
    def is_current_data(self):
        return\
            not self.is_default()               and\
            self.is_current_nodes()             and\
            self.is_current_user()              and\
            self.loading_wait_time.value >= 0    and\
            self.save_folder_path.value.exists()
        
    def is_current_nodes(self):
        return self.nodes != None and len(self.nodes) > 1
            
    def is_current_user(self):
        return '@' in self.user_email.value and len(self.user_password.value) > 0
            
    def is_default(self):
        return NO_DATA in self.user_email.value + self.user_password.value
    
    @staticmethod
    def profile_path():
        return Path(SettingData.SETTINGFOLDER_PATH).absolute().joinpath('./ProfileData/Profile 1')