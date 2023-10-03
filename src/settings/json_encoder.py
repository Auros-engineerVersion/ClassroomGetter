from __future__ import annotations
from json import JSONEncoder, JSONDecoder
from datetime import datetime
from re import sub

from ..literals import *
from ..data import *

encode_decode_format = {
    #builtin types
    'datetime': {
        ENCODE: lambda o: dic_gen(o.timestamp(), o.__class__.__name__),
        DECODE: lambda o: datetime.fromtimestamp(o)},
    
    'Path': {
        ENCODE: lambda o: dic_gen(str(o), o.__class__.__name__),
        DECODE: lambda o: Path(o)},
    
    'WindowsPath': {
        ENCODE: lambda o: dic_gen(str(o), o.__class__.__name__),
        DECODE: lambda o: Path(o)},
    
    'MacPath': {
        ENCODE: lambda o: dic_gen(str(o), o.__class__.__name__),
        DECODE: lambda o: Path(o)},
    
    #my types
    'Node': {
        ENCODE: lambda o: dic_gen(o),
        DECODE: lambda o: Node.factory(**o)},
    
    'RoutineData': {
        ENCODE: lambda o: dic_gen(o),
        DECODE: lambda o: RoutineData.factory(*o.values())},
    
    'SettingData': {
        ENCODE: lambda o: dic_gen(o),
        DECODE: lambda o: SettingData(**o)}}

def trim_dict(dic: dict) -> dict:
    return {sub('^_.*?__', '', k): v for k, v in dic.items()}

def dic_gen(o, name=None) -> dict:
    '''
        オブジェクトをtypeとvalueのペアとなった辞書に変換する
        Args:
            o: 変換するオブジェクト
            name: typeとして使用する名前。これは渡されるoと実際のtypeが異なる場合に使用する。\n
                  例えば、oがdatetime.datetime型の場合、typeとしてはdatetime.datetimeとなるが、\n
                  decodeの関係上、timestampによりfloat型へと変換される。
    '''
    if name is None:
        name = o.__class__.__name__

    if getattr(o, '__dict__', False):
        return {TYPE: name, VALUE: trim_dict(o.__dict__)}
    elif isinstance(o, list):
        return {TYPE: name, VALUE: min(o)}
    else:
        return {TYPE: name, VALUE: o}

class MyClassEncoder(JSONEncoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def default(self, o):
        params = encode_decode_format.get(o.__class__.__name__)
        #キーが無ければ
        if params is None:
            return super().default(o)
        else:
            return params[ENCODE](o)
    
class MyClassDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
    
    def object_hook(self, o: dict):
        if TYPE not in o:
            if isinstance(o, int):
                return int(o)
            else:
                return o
        else:
            params = encode_decode_format.get(o[TYPE])
            if params is None:
                return o
            else:
                return params[DECODE](o[VALUE])