from time import sleep

class document_state_is(object):
    def __init__(self, locator, condition) -> None:
        self.__locator = locator
        self.__condition = condition
        pass
    
    def __call__(self, driver):
        value = driver.execute_script('return document.readyState')
        if (value == self.__condition):
            return driver.find_elements(*self.__locator)
        else:
            return False