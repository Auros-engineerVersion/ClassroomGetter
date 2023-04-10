from __future__ import annotations
from time import sleep
import sys, os
sys.path.append(os.path.abspath('.'))
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement

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
    
    def next_links(self, *xpathes: str):
        c = self.BrowserControl
        c.move(self.key)

        try:
            xpath = xpathes[self.tree_height]
            elems = c.wait.until(EC.presence_of_all_elements_located, ((By.XPATH, xpath)))
            if ('/u/1/c/' in c.driver.current_url): #授業のページだったら
                return list(map(c.link_copy_button_click, elems))
            else:
                return list(map(lambda d : d.get_attribute('href'), elems))
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
        stack: list[Node] = [parent]
        #1行目:授業へのxpath
        #2行目:各授業セクションへのxpath
        #3行目:ファイルへのxpath
        xpathes = (\
            "//a[@class='onkcGd ZmqAt Vx8Sxd']",\
            "//div[@jsmodel='PTCFbe']",\
            "//a[@class='VkhHKd e7EEH ']"\
        )
                
        while (len(stack) > 0):
            value = stack.pop()
            links = value.next_links(*xpathes)
            value.create_childs(*links)
            #"//li[contains(@class,'onkcGd eDfb1d YVvGBb Vx8Sxd') or contains(@jscontroller,'XZzUb')]"
            for child in value.edges():
                stack.append(child)