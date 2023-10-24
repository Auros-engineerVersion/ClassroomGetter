from pathlib import Path
from time import sleep
from tkinter import Widget

import tkcap


def caputuer(target: Widget, path: Path, overwrite: bool = False) -> Path:
    target.update_idletasks()
    sleep(0.3) #widgetが読み込まれて表示されるまで待機
    tkcap.CAP(target.winfo_toplevel()).capture(str(path), overwrite)
    
    return path