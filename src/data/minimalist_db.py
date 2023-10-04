from __future__ import annotations

from ..interface import *

class MinimalistID(int, IMinimalistID):
    def value(self, db):
        return db.get(self)

class MinimalistRecode(dict, IComparable, IMinimalistRecode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def __lt__(self, other):
        return self['value'] < other['value']
    
    def __eq__(self, __value: MinimalistRecode) -> bool:
        return self['value'] == __value
    
    def __hash__(self) -> int:
        return hash(self['value'])
    
class EmptyRecode(MinimalistRecode):
    def __init__(self) -> None:
        super().__init__(value=None)
        
    def __lt__(self, other):
        return False

class MinimalistDB(list[MinimalistRecode], IMinimalistDB):
    def __init__(self, initial_line = 0) -> None:
        super().__init__()
        
        #idの役割を果たす。現在どこまでレコードが追加されたか
        self.__front_line: MinimalistID = 0 + initial_line
        
    def __len__(self) -> int:
        length = 0
        for recode in self:
            if isinstance(recode, EmptyRecode):
                continue
            else:
                length += 1
        return length
        
    def add(self, recode: MinimalistRecode) -> MinimalistID:
        """レコードを追加する。追加したレコードのidを返す"""
        if not isinstance(recode, MinimalistRecode):
            recode = MinimalistRecode(value=recode)
        
        self.append(recode)
        id = MinimalistID(self.__front_line)
        self.__front_line += 1
        return id
    
    def get(self, id) -> MinimalistRecode:
        return self[max(id, 0)]
        
    def remove(self, id):
        self[max(id, 0)] = EmptyRecode()
        
    def remove_target(self, target: MinimalistRecode) -> None:
        for i, recode in enumerate(self):
            if recode == target:
                self[i] = EmptyRecode()
                break
            
    def clear(self) -> None:
        self.__front_line = 0
        return super().clear()