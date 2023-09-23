from __future__ import annotations
from json import JSONEncoder
from datetime import datetime

from ..literals import *
from ..data import *


class MyClassEncoder(JSONEncoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __dic_gen(self, o, type_name: str) -> dict:
        try:
            return {TYPE: type_name, VALUE: o.__dict__}
        except AttributeError: #set等の__dict__を持たないオブジェクトの場合
            try:
                return {TYPE: type_name, VALUE: min(o)}
            except TypeError: #Atomの場合
                return {TYPE: type_name, VALUE: o}
    
    def default(self, o):
        match o:
            case datetime():
                return self.__dic_gen(o.timestamp(), 'datetime')
            case Node():
                return self.__dic_gen(o, 'Node')
            case RoutineData():
                return self.__dic_gen(o, 'RoutineData')
            
        return super().default(self, o)