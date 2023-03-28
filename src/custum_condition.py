from time import sleep

def document_state_is(condition: str, locator):
    #WebDriverWait用のCustumCondition
    #ドキュメントのreadyStateをチェックし続け、
    #指定の条件になったら探す
    def _predicate(driver):
        value = None
        #目的のコンディションになるまで繰り返す
        while (value != condition):
            value = driver.driver.execute_script('return document.readyState')
            if (value == condition): break
            sleep(0.1)
            
        driver.find_elements(*locator)
    
    return _predicate