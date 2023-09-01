import sys
from functools import wraps
from re import sub
from random import choice
from string import ascii_letters, digits
import types
from typing import Any, Callable, Iterable, SupportsInt
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

def iterable_depth(x) -> int:
    if not x:
        return 0
    else:
        if type(x) is list:
            return 1 + max(map(iterable_depth, x))
        else:
            return 0
    
def flatten(x, depth = 0) -> Iterable:
    if iterable_depth(x) <= depth:
        return x
    else:
        for i in x:
            if type(i) is list:
                yield from flatten(i, depth)
            else:
                yield i

def public_vars(x) -> filter:
    return filter(lambda x: '__' not in x[0], vars(x).items())

def randstr(length: SupportsInt) -> str:
    return ''.join(choice(ascii_letters + digits) for _ in range(length))

def get_geometory(widget) -> str:
    return f'{widget.winfo_width()}x{widget.winfo_height()}'

def size_to_geometory(width: int, height: int) -> str:
    return f'{width}x{height}'

class Infix:
    def __init__(self, function):
        self.function = function

    def __ror__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))

    def __or__(self, other):
        return self.function(other)

    def __rlshift__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))

    def __rshift__(self, other):
        return self.function(other)

    def __call__(self, value1, value2):
        return self.function(value1, value2)
            
pipe = Infix(lambda x, func: func(x))
arrow = Infix(lambda x, func: identity(x)(func))

class CommentableObj:
    def __init__(self, value, comment = '') -> None:
        super().__init__()
        self.__value = value
        self.__comment = comment
    
    def __eq__(self, other):
        return self.__value == other

    def __or__(self, other):
        return self.__value or other

    @property
    def value(self):
        return self.__value    

    @property
    def comment(self) -> str:
        return self.__comment