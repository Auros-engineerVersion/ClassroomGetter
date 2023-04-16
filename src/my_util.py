from functools import wraps
from re import search
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