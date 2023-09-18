import tkinter as tk

from ....my_util import is_none, arrow, size_to_geometory

class ResizableFrame(tk.Frame):
    def __init__(self, **kw):
        tk.Frame.__init__(self, is_none(**kw['master'], tk.Tk()), **kw)\
            |arrow| (lambda f: f.bind('<Configure>', self.__size_change))
                            
    def __size_change(self, event):
        if event.widget.widget_name is self.widgetName:
            self.__width, self.__height = event.width, event.height
                            
    def resize(self, default_width = 400, default_height = 300):
        """
            以前のサイズを記録し、それをもとにサイズを変更する\n
            もし以前のサイズがNoneなら、デフォルトのサイズを設定する
        """
        
        #サイズ変更
        self.winfo_toplevel()\
            |arrow| (lambda r: r.resizable(width=False, height=False))\
            |arrow| (lambda r: r.geometry(is_none(
                size_to_geometory(self.__width, self.__height),
                size_to_geometory(default_width, default_height))))