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
    user_email: dict = field(default_factory=lambda:{
        VALUE: NO_DATA, 
        DESCRIPTION: USER_EMAIL_DESC})
    
    user_password: dict = field(default_factory=lambda:{
        VALUE: NO_DATA, 
        DESCRIPTION: USER_PASSWORD_DESC})

    #セーブフォルダの場所
    save_folder_path: dict = field(default_factory=lambda:{
        VALUE: Path('./Save/save.json').absolute(), 
        DESCRIPTION: SAVE_FOLDER_PATH_DESC})
    
    #ページの読み込みを待つ時間
    loading_wait_time: dict = field(default_factory=lambda:{
        VALUE: 5,
        DESCRIPTION: LOADING_WAIT_TIME_DESC})
    
    web_driver_options_data: dict = field(default_factory=lambda:{
        VALUE: '--headless, --disable-gpu, --blink-settings=imagesEnabled=false, --ignore-certificate-error, --ignore-certificate-error',
        DESCRIPTION: WEB_DRIVER_OPTIONS_DESC})
    
    #----------------保存されたデータ--------------------
    nodes: MinimalistDB = field(default_factory=MinimalistDB)
        
    def __post_init__(self):
        if not isinstance(self.user_email, dict):
            self.user_email = {VALUE:self.user_email, DESCRIPTION: USER_EMAIL_DESC}
            
        if not isinstance(self.user_password, dict):
            self.user_password = {VALUE:self.user_password, DESCRIPTION: USER_PASSWORD_DESC}
            
        if not isinstance(self.save_folder_path, dict):
            self.save_folder_path = {VALUE:self.save_folder_path, DESCRIPTION: SAVE_FOLDER_PATH_DESC}
            
        if not isinstance(self.loading_wait_time, dict):
            self.loading_wait_time = {VALUE:self.loading_wait_time, DESCRIPTION: LOADING_WAIT_TIME_DESC}
            
        if not isinstance(self.web_driver_options_data, dict):
            self.web_driver_options_data = {VALUE:self.web_driver_options_data, DESCRIPTION: WEB_DRIVER_OPTIONS_DESC}
            
        if len(self.nodes) == 0:
            self.nodes.add(Node('Classroom', ISettingData.TARGET_URL, 0))
    
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
    def editable_data(self):
        return {
            'user_email': self.user_email,
            'user_password': self.user_password,
            'save_folder_path': self.save_folder_path,
            'loading_wait_time': self.loading_wait_time,
            'web_driver_options': self.web_driver_options_data}
    
    @property
    def profile_path(self):
        return ISettingData.SETTINGFOLDER_PATH.absolute().joinpath('./ProfileData/Profile 1')
        
    def is_current_data(self):
        return\
            not self.is_default()               and\
            self.is_current_nodes()             and\
            self.is_current_user()              and\
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