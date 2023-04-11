from __future__ import annotations
from time import sleep
import sys, os
sys.path.append(os.path.abspath('.'))
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from re import search

import settings as cfg
from src.controls import Controls
from src import my_util
from src import custum_condition as MyEC

class Node:
    BrowserControl = None
    Nodes = [] #全てのノードを列挙する

    def __init__(self, key: str, tree_height: int) -> None:
        self.__edges: list[Node] = []
        self.key = key
        self.tree_height = tree_height
            
        #クラス変数の宣言と同時に定義を行わないのは、変数が勝手に起動してしまうため
        #つまり、BrowserControlはWebDrivreを有しているため、Chromeが勝手に起動してしまう
        if (Node.BrowserControl == None):
            Node.BrowserControl = Controls(cfg.PROFILE_PATH, cfg.PROFILE_NAME)
            
        Node.Nodes.append(self)
        pass
    
    def __del__(self):
        Node.Nodes.remove(self)
    
    #getter/setterを兼ねたもの
    def edges(self, add_value: Node = None):
        if (add_value != None):
            self.__edges.append(add_value)
            Node.Nodes.append(add_value)
        
        return self.__edges
    
    def next_links(self) -> list[str]:
        c = self.BrowserControl
        c.move(self.key)

        try:
            #ホームなら
            if ('/u/0/h' in self.key):
                locator = (By.XPATH, "//a[@class='onkcGd ZmqAt Vx8Sxd']")
                pattern = '^.*/u/0/./{12, 18}$'
                return c.hrefs(locator, pattern)
            #授業のタブなら
            elif ('/u/0/c' in self.key):
                return [my_util.to_all_tab_link(self.key)]
            
            #「全てのトピック」なら
            elif ('/t/all' in self.key):
                c.click_all_sections()
                locator = (By.XPATH, "//a[@class='VkhHKd e7EEH ']")
                pattern = '^.*/file/d/.*$'
                return c.hrefs(locator, pattern)
            
            #ファイルのurlなら
            else:
                return []
                
        except TimeoutError:
            return []
            
    def create_childs(self, *keys: str):
        for key in keys:
            child = Node(key, self.tree_height + 1)
            self.edges(child)
            
        return self

    @staticmethod
    def ShowTree(parent: Node):
        def __indent(indent_size: int):
            result: str = ''
            for i in range(0, indent_size):
                result += '    ' #半角スペース4つはpythonと同じインデントである
            return result
        
        if (parent == None):
            return
            
        offset = parent.tree_height
        print(__indent(offset) + parent.key)
        for node in parent.edges():
            Node.ShowTree(node)
                
    #幅優先探索
    @staticmethod
    def InitializeTree(parent: Node):            
        queue: list[Node] = [parent]
                
        while (len(queue) > 0):
            value = queue.pop()
            links = value.next_links()
            
            if (len(links) > 0):
                value.create_childs(*links)
                
            for child in value.edges():
                queue.append(child)