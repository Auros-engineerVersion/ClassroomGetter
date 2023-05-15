from __future__ import annotations
import gc
import tkinter as tk
from datetime import timedelta
from pathlib import Path

from src.interface.i_node import INode
from src.data.routine_data import RoutineData


TEXT_VARIABLE = 'textvariable'

def box_factory(key_name, value, width: int):
    if type(value) == str:
        return lambda master: InputBox(master, width=width, entry_or_spinbox=True, title=key_name)
    elif type(value) == int:
        return lambda master: InputBox(master, width=width, entry_or_spinbox=False, title=key_name)
    elif type(value) == None or type(value) == set:
        return lambda master: None #この使われていないmasterは他のlambda関数と規格を合わせるために必要である
    else: #Pathなら
        return lambda master: DialogInput(master, width=width, default_path=value, title=key_name)