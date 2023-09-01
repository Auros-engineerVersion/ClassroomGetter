import tkcap
from tkinter import Widget
from pathlib import Path
import PIL.Image
from time import sleep

def caputuer(target: Widget, path: Path, overwrite: bool = False) -> Path:
    target.update_idletasks()
    sleep(0.2) #widgetが読み込まれて表示されるまで待機
    tkcap.CAP(target.winfo_toplevel()).capture(str(path), overwrite)
    
    return path
    
#2つの画像の差分を返す
def image_delta(path1: Path, path2: Path):
    img1 = PIL.Image.open(path1)
    img2 = PIL.Image.open(path2)
    
    if (img1.size != img2.size):
        raise ValueError('画像のサイズが異なります')
    
    width, height = img1.size
    
    delta = PIL.Image.new('RGB', (width, height))
    for x in range(width):
        for y in range(height):
            r1, g1, b1 = img1.getpixel((x, y))
            r2, g2, b2 = img2.getpixel((x, y))
            
            delta.putpixel((x, y), (abs(r1 - r2), abs(g1 - g2), abs(b1 - b2)))
    
    return delta

#image_deltaから得られた差分を画像として保存する
def save_delta(delta: PIL.Image.Image, path: Path):
    delta.save(path, 'PNG')