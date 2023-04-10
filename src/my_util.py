from functools import wraps
from re import search

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
    
def __to_tab_link(url: str):
    return str(url).replace('/u/0/c/', '/w/')

def __to_all_tab_link(url: str):
    return __to_tab_link(url) + '/t/all'

#tree_heightにより正しいurlを返す
def current_link(url: str, tree_height: int) -> str:
    link = None
    if (tree_height == 0):
        link = __to_all_tab_link(url)
    elif (tree_height == 1):
        link = __to_tab_link(url)
    else:
        link = url
        
    return link