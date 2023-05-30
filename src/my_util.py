from functools import wraps
from re import sub
from typing import Iterable, SupportsInt

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

def ratio(x: SupportsInt, y: SupportsInt, a: SupportsInt) -> tuple[SupportsInt, SupportsInt]:
    if a == 0:
        return (0, 0)
    else:
        return (x // abs(a), y // abs(a))