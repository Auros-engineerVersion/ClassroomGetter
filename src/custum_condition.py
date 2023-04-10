from time import sleep

class document_state_is(object):
    def __init__(self, locator) -> None:
        self.__locator = locator
        pass
    
    def __call__(self, driver):
        value = driver.execute_script('return document.readyState')
        print(value)
        if (value == 'complete'):
            return driver.find_elements(*self.__locator)
        else:
            sleep(0.5)
            return False