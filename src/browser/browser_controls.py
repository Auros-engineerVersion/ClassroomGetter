from typing import Callable, Iterable
from re import search
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import InvalidSelectorException
from selenium.webdriver.support import expected_conditions as EC

from ..interface import *
from ..data import *

def move(bc: IBrowserControlData, url: str):
    bc.driver.get(url)
    
def search_element(bc: IBrowserControlData, xpath: str) -> WebElement:
    try:
        return bc.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    except TimeoutException:
        raise ValueError(f'Not found xpath: {xpath}')
    except InvalidSelectorException:
        raise ValueError(f'Invalid xpath: {xpath}')

def search_element_all(bc: IBrowserControlData, xpath: str) -> list[WebElement]:
    try:
        return bc.wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
    except TimeoutException:
        return []
    except InvalidSelectorException:
        return []
    
def elements_filter(filter_func: Callable, pattern: str = ''):
    def __get_hrefs(target: Iterable) -> list:
        current_values = filter(
            lambda string: search(pattern, string=str(string)) != None,
            filter(
                lambda obj: type(obj) == str,
                map(filter_func, target)
            )
        )
        
        return list(current_values)
    return __get_hrefs

def click_all_sections(bc: IBrowserControlData):
    def __check_loaded(xpath) -> bool:
        def __predictate(driver):
            sample_buttons = search_element_all(bc, By.XPATH, "//div[@jsmodel='RH7Ihb']")
            if all([x.get_attribute('data-controller-loaded') == 'true' for x in sample_buttons]):
                return driver.find_elements(By.XPATH, xpath)
            else:
                return False
        return __predictate
        
    try:
        xpath = "//div[@jsname='rQC7Ie' and @role='button']"
        buttons = bc.wait.until(__check_loaded(xpath))
        
        action = ActionChains(bc.driver)
        for button in buttons:
            action.move_to_element(button).click(button).pause(bc.wait._poll).perform()
            
    except TimeoutException:
        return
    
def login_college_form(bc: IBrowserControlData, setting: SettingData):
    befor_at_index = setting.user_email.find('@')
    user_name = setting.user_email[:befor_at_index]
    
    #1:emailの@以前をユーザー名に送る
    #2:passwordを送る
    #3:ログインボタンを押す
    search(bc, "//input[@id='j_username']").send_keys(user_name)
    search(bc, "//input[@id='j_password']").send_keys(setting.user_password)
    search(bc, "//button[@type='submit']").click()

def login_google(bc: IBrowserControlData, setting: SettingData):
    #1:emailを入力する
    #2:続行を押す
    #3:大学のフォームにログイン
    #4:続行を押す
    search(bc, "//input[@type='email']")        .send_keys(setting.user_email)
    search(bc, "//div[@id='identifierNext']")   .click()
    login_college_form(bc, setting)
    search(bc, "//div[@jsname='Njthtb']")       .click()
    
def login_classroom(bc: IBrowserControlData, setting: SettingData):
    #1:ログイン画面に移動する
    #2:Googleにログインする
    #3:プロファイルを設定する
    move(bc, search(bc, "//a[@class='gfe-button gfe-button--medium-emphasis gfe-button--middle-align']").get_attribute('href'))
    login_google(bc, setting)