from __future__ import annotations

from ..interface import *
from ..my_util import identity

class MinimalistID(int, IMinimalistID):
    def value(self, db):
        return db.get(self)

class MinimalistRecode(dict, IComparable, IMinimalistRecode):
    def __init__(self, value):
        super().__init__(value=value)
        
    def __lt__(self, other):
        return self['value'] < other['value']
    
    def __eq__(self, __value: MinimalistRecode) -> bool:
        return self['value'] == __value
    
    def __hash__(self) -> int:
        return hash(self['value'])

class MinimalistDB(list[MinimalistRecode], IMinimalistDB):
    def __init__(self, initial_line = 0) -> None:
        super().__init__()
        
        #idの役割を果たす。現在どこまでレコードが追加されたか
        self.__front_line: MinimalistID = 0 + initial_line
        
    def add(self, recode: MinimalistRecode) -> MinimalistID:
        """レコードを追加する。追加したレコードのidを返す"""
        if not isinstance(recode, MinimalistRecode):
            recode = MinimalistRecode(value=recode)
        
        self.append(recode)
        id = MinimalistID(self.__front_line)
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
        
    def get_fromID(self, id: MinimalistID, id_get: Callable[[MinimalistID], MinimalistID]=lambda recode: recode['value']) -> MinimalistRecode | None:
        for recode in self:
            if id_get(recode) == id:
                return recode

    def clear(self) -> None:
        self.__front_line = 0
        return super().clear()
    
    def remove(self, id: MinimalistID, id_get: Callable[[MinimalistID], MinimalistID]=lambda recode: recode['value']):
        if isinstance(id, MinimalistID):
            return super().remove(self.get_fromID(id, id_get))
        else:
            raise TypeError(f'id must be MinimalistID, but {type(id)}')