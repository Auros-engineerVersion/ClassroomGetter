from selenium import webdriver

import settings as cfg
from src.controls import Controls
from src import path_converter

class Node(object):
    BrowserControl = Controls(cfg.PROFILE_PATH, cfg.PROFILE_NAME)

    def __init__(self, observe_url: str) -> None:
        self.__edges: list[Node] = None
        self.__observe_url = observe_url
        pass
    
    def edge(self, add_value = None):
        if (add_value != None):
            self.__edges.append(add_value)
        
        return self.__edges
    
    def move(self):
        Node.BrowserControl.move(self.__observe_url)
        hrefs = Node.BrowserControl.hrefs(Node.BrowserControl.wait, '^.+/0/.{11,20}$')
        for href in hrefs:
            link = path_converter(href)
            self.__edges.append(Node(link))
        
n = Node(cfg.TARGET_URL)
n.move()