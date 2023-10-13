from __future__ import annotations

from dataclasses import *
from pathlib import Path

from ..literals import *
from ..interface import ISettingData
from .nodes import Node
from .minimalist_db import MinimalistDB

@dataclass
class SettingData(ISettingData):
    #----------------通常のデータ------------------------
    user_email: dict = NO_DATA
    user_password: dict = NO_DATA

    #セーブフォルダの場所
    save_folder_path: dict = field(default_factory=Path('./Save').absolute)
    
    #探索を行う際の深度
    search_depth: int = field(default=1)
    
    #ページの読み込みを待つ時間
    loading_wait_time: dict = 5

    web_driver_options_data: dict = '--headless=new, --window-size=1280,720'
    
    #----------------保存されたデータ--------------------
    nodes: MinimalistDB = field(default_factory=MinimalistDB)
        
    def __post_init__(self):
        if not isinstance(self.user_email, dict):
            self.user_email = {VALUE:self.user_email, DESCRIPTION: USER_EMAIL_DESC}
            
        if not isinstance(self.user_password, dict):
            self.user_password = {VALUE:self.user_password, DESCRIPTION: USER_PASSWORD_DESC}
            
        if not isinstance(self.save_folder_path, dict):
            self.save_folder_path = {VALUE:Path(self.save_folder_path), DESCRIPTION: SAVE_FOLDER_PATH_DESC}
            
        if not isinstance(self.search_depth, dict):
            self.search_depth = {VALUE:int(self.search_depth), DESCRIPTION: SEARCH_DEPTH_DESC}
            
        if not isinstance(self.loading_wait_time, dict):
            self.loading_wait_time = {VALUE:int(self.loading_wait_time), DESCRIPTION: LOADING_WAIT_TIME_DESC}
            
        if not isinstance(self.web_driver_options_data, dict):
            self.web_driver_options_data = {VALUE:self.web_driver_options_data, DESCRIPTION: WEB_DRIVER_OPTIONS_DESC}
            
        #深度を設定する
        Node.SearchDepth = self.search_depth[VALUE]
            
        if len(self.nodes) == 0:
            self.nodes = Node.Nodes
            
        #ノードが存在しない場合は、デフォルトのノードを作成する
        if len(Node.Nodes) == 0:
            Node('Classroom', ISettingData.TARGET_URL, 0)
    
    @property
    def profile(self):
        return self.user_email[VALUE], self.user_password[VALUE]
    
    @profile.setter
    def profile(self, other: tuple[str, str]):
        self.user_email[VALUE] = other[0]
        self.user_password[VALUE] = other[1]
        
    @property
    def web_driver_options(self):
        return {
            VALUE: self.web_driver_options_data[VALUE].replace(' ', '').replace('\n', '').split(','), 
            DESCRIPTION: WEB_DRIVER_OPTIONS_DESC}
    
    @property
    def normal(self):
        """
        通常の設定と思われるものをヘッダ付きで返す
        
        return: (str, dict)
        """
        return NORMAL_DATA, {
            USER_EMAIL: self.user_email,
            USER_PASSWORD: self.user_password,
            SAVE_FOLDER_PATH: self.save_folder_path,
            SEARCH_DEPTH: self.search_depth}
    
    @property 
    def advanced(self):
        """
        通常であればさわらないような設定をヘッダ付きで返す
        
        return: (str, dict)
        """
        return ADVANCED_DATA, {
            LOADING_WAIT_TIME: self.loading_wait_time,
            WEB_DRIVER_OPTIONS: self.web_driver_options
        }
    
    @property
    def profile_path(self):
        return ISettingData.SETTING_FOLDER_PATH.absolute().joinpath('./ProfileData/Profile 1')
        
    def is_current_data(self):
        return\
            not self.is_default()                 and\
            self.is_current_nodes()               and\
            self.is_current_user()                and\
            self.loading_wait_time[VALUE] >= 0    and\
            self.save_folder_path[VALUE].exists()
        
    def is_current_nodes(self):
        return self.nodes != None and len(self.nodes) > 1
            
    def is_current_user(self):
        return '@' in self.user_email[VALUE] and len(self.user_password[VALUE]) > 0
            
    def is_default(self):
        return NO_DATA in self.user_email[VALUE] + self.user_password[VALUE]
    
    def is_guest(self):
        return self.user_email[VALUE] == 'guest' and self.user_password[VALUE] == 'guest'