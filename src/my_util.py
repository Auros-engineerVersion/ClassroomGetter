from functools import wraps
from re import search, sub
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

def link_filter(url: str):
    #0番目が授業タブの全てのトピック, 1番目が各トピック, 2番目がファイルの正規表現
    patterns = ['^.+/0/.{11,20}$', '.*/details$', '.*file/d/.*']
    
    result = 0
    for pattern in patterns:
        result += search(pattern, url) != None
        
    if (result > 0):
        return url
    
def text_filter(value: str) -> str:
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

def has_curretn_args(func, type):
    sig = inspect.signature(func)
    for param in sig.parameters:
        if sig.parameters[param].annotation == type:
            return True
        
    return False