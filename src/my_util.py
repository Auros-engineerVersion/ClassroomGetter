from functools import wraps
from re import sub
from random import choice
from string import ascii_letters, digits
from typing import Callable, Iterable, SupportsInt
from pathlib import Path
import inspect

#末尾再帰の最適化
def tail_recursion(func):
    firstcall = True
    params = ((), {})
    result = func
    
    @wraps(func)
    def wrapper(*args, **kwd):
        nonlocal firstcall, params, result
        params = args, kwd
        if firstcall:
            firstcall = False
            try:
                while result is func:
                    result = func(*args, **kwd) # call wrapper
                    args, kwd = params
            finally:
                firstcall = True
                return result
        else:
          return func
    
    return wrapper
    
def text_filter(value: str) -> str:
    @tail_recursion
    def __remove(value: str, patterns: list[str], pattern_count: int = 0) -> str:
        if pattern_count == len(patterns):
            return value
        
        removeed_value = sub(patterns[pattern_count], '', value)
        return __remove(removeed_value, patterns, pattern_count + 1)
        
    brackets_pattern = '[\(（].+?[\)）]' #括弧とその中のものが指定される
    year_pattern = '[A-Z一-龠]?.*[0-9一二三四五六七八九十]' #HogeHoge令和五年度HogeHogeでは、令和五のみ指定される
    nendo_pattern = '[年度]'
    space_pattern = '[\s　]' #半角全角スペースが指定される
    
    all_pattern = [brackets_pattern, year_pattern, nendo_pattern, space_pattern]
    
    if any([x in value for x in ['.pdf', '.mp3', '.mp4', '.jpg', '.png', '.mov']]):
        return value
    else:
        return __remove(value, all_pattern)
    
def to_tab_link(url: str):
    return str(url).replace('/c/', '/w/')

def to_all_tab_link(url: str):
    return to_tab_link(url) + '/t/all'

def convert_to_tuple(list_1: Iterable, list_2: Iterable) -> list[tuple]:
    return list(
        map(
            lambda x, y: (x, y),
            list_1, list_2
        )
    )
    
def do_nothing(x):
    return x
    
def identity(x):
    def func(f):
        f(x)
        return x
    return func

def public_vars(x) -> filter:
    return filter(lambda x: '__' not in x[0], vars(x).items())

def randstr(length: SupportsInt) -> str:
    return ''.join(choice(ascii_letters + digits) for _ in range(length))

def get_geometory(widget) -> str:
    return f'{widget.winfo_width()}x{widget.winfo_height()}'

def size_to_geometory(width: int, height: int) -> str:
    return f'{width}x{height}'

#exec関数を用いて指定したフォルダ内のすべてのファイルをimportする
#importした後、クラスを名前とペアでdictとして返す関数
def __directory_import(path: Path) -> dict[str, object]:
    '''戻り値: {ファイル名: モジュール}'''
    from importlib import machinery
    
    #pathがフォルダでない場合はエラーを返す
    if not path.is_dir():
        raise ValueError('pathはフォルダである必要があります')
    
    modules = {}
    #path内のファイルをすべてimportする
    for file in path.iterdir():
        if file.suffix == '.py':
            module_name = file.stem
            module = machinery.SourceFileLoader(module_name, str(file)).load_module()
            modules[module_name] = module
            
    return modules

def __menbers(module) -> list[str]:
    return [name for name, _ in inspect.getmembers(module, inspect.isclass)]

def __get_class(module: object, class_name: str, *args, **kwargs) -> object:
    cls = getattr(module, class_name)
    return cls

def all_class_in_dir(path: Path):
    result = []
    for v in __directory_import(path).items():
        for name in __menbers(v[1]):
            result.append(__get_class(v[1], name))
        
    return result

def argments_size(func):
    return len(inspect.signature(func).parameters)