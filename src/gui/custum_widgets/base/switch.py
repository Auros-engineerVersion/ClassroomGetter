import tkinter as tk
from tkinter import *


class Switch(tk.Button):
    def __init__(self, default_state=False, **kw) -> None:
        super().__init__(**kw)
        self.__state = default_state
        self.__active_events = []
        self.__non_active_events = []
        
        self.bind('<ButtonPress>', self.switch)
        
    @property
    def state(self):
        return self.__state
    
    def on_active(self, func):
        '''スイッチがOnの状態に呼ばれる'''
        self.__active_events.append(func)
        
    def on_not_active(self, func):
        self.__non_active_events.append(func)
        
    def switch(self, event):
        '''スイッチの状態を反転させる'''
        self.__state = not self.__state
        if self.__state:
            for func in self.__active_events:
                func()
        else:
            for func in self.__non_active_events:
                func()
                
        self.update()