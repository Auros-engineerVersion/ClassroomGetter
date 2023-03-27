from selenium import webdriver

#WebDriverWait用のCustumCondition
class IsLoaded:
    def __call__(self, driver: webdriver) -> bool:
        value = driver.driver.execute_script('return document.readyState')
        if value == 'complete':
            return True
        else:
            return False
