from __future__ import annotations

from ..interface import *
from ..my_util import identity

class MinimalistRecode(dict, IComparable, IMinimalistRecode):
    def __init__(self, value):
        super().__init__(value=value)
        
    def __lt__(self, other):
        return self['value'] < other['value']
    
    def __eq__(self, other: MinimalistRecode) -> bool:
        if not isinstance(other, MinimalistRecode):
            return False
        else:
            return self['value'] == other['value']
    
    def __hash__(self) -> int:
        return hash(self['value'])

class MinimalistDB(list[MinimalistRecode], IMinimalistDB):
    def __init__(self, initial_line = 0) -> None:
        super().__init__()
        
        #idの役割を果たす。現在どこまでレコードが追加されたか
        self.__front_line = 0 + initial_line
        
    def add(self, recode: MinimalistRecode) -> int:
        """レコードを追加する。追加したレコードのidを返す"""
        if not isinstance(recode, MinimalistRecode):
            recode = MinimalistRecode(value=recode)
        
        self.append(recode)
        id = self.__front_line
        self.__front_line += 1
        return id
    
    def add_with_unique(self, recode: MinimalistRecode):
        """
        このメソッドは、recodeのvalueが既に存在する場合は、そのレコードを返す。
        そのため、同値のレコードが複数存在することはない。
        """
        if recode not in self:
            return self.add(recode)
        else:
            return self.index(recode)
        
    def get_fromID(self, id:int, id_get: Callable[[int], int]=lambda recode: recode['value']) -> MinimalistRecode | None:
        for recode in self:
            if id_get(recode) == id:
                return recode

    def clear(self) -> None:
        self.__front_line = 0
        return super().clear()
    
    def remove(self, id: int, id_get: Callable[[int], int]=lambda recode: recode['value']):
        if isinstance(id, int):
            return super().remove(self.get_fromID(id, id_get))
        else:
            raise TypeError('id must be int')