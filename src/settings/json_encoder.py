from __future__ import annotations
from json import JSONEncoder, JSONDecoder
from datetime import datetime
from re import sub

from ..literals import *
from ..data import *


def trim_dict(dic: dict) -> dict:
    return {sub('^_.*?__', '', k): v for k, v in dic.items()}

class MyClassEncoder(JSONEncoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __dic_gen(self, o, type_name: str) -> dict:
        try:
            return {TYPE: type_name, VALUE: trim_dict(o.__dict__)}
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
        
        return super().default(o)
    
class MyClassDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)
    
    def object_hook(self, o: dict):
        if TYPE not in o:
            return o
        else:
            match o[TYPE]:
                case 'datetime':
                    return datetime.fromtimestamp(o[VALUE])
                case 'Node':
                    return Node.factory(**o[VALUE])
                case 'RoutineData':
                    return RoutineData.factory(*o[VALUE].values())

            return super().object_hook(self, o)