from __future__ import annotations

from abc import ABCMeta, abstractmethod, abstractproperty
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait


class IBrowserControlData(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, setting, driver = None, wait = None) -> None:
        pass
        
    @abstractproperty
    def driver(self) -> WebDriver:
        raise NotImplementedError
    
    @abstractproperty
    def wait(self) -> WebDriverWait:
        raise NotImplementedError