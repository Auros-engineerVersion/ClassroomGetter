from re import search
from typing import Callable, Iterable
from time import sleep

from selenium.common.exceptions import (InvalidSelectorException,
                                        TimeoutException)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from ..interface import *
from ..my_util import arrow

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
    
def elems_sifter(target, sifter: Callable, reg: str = ''):
    result = []
    for x in [sifter(x) for x in target]:
        if isinstance(x, str) and search(reg, x) != None:
            result.append(x)
            
    return result

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
    
def login_college_form(bc: IBrowserControlData, email: str, password: str):
    user_name = email[:email.find('@')]
    
    #1:emailの@以前をユーザー名に送る
    #2:passwordを送る
    #3:ログインボタンを押す
    search_element(bc, "//input[@id='j_username']").send_keys(user_name)
    search_element(bc, "//input[@id='j_password']").send_keys(password)
    search_element(bc, "//button[@type='submit']").click()

def login_google(bc: IBrowserControlData, email: str, password: str):
    #1:emailを入力する
    #2:続行を押す
    #3:大学のフォームにログイン
    #4:続行を押す
    search_element(bc, "//input[@type='email']")        .send_keys(email)
    search_element(bc, "//div[@id='identifierNext']")   .click()
    login_college_form(bc, email, password)
    search_element(bc, "//div[@jsname='Njthtb']")       .click()
    
def login_classroom(bc: IBrowserControlData, email: str, password: str):
    if bc.driver.current_url != ISettingData.TARGET_URL:
        move(bc, ISettingData.TARGET_URL)
    
    #1:ログイン画面に移動する
    #2:Googleにログインする
    #3:プロファイルを設定する
    move(bc, search_element(bc, "//a[@class='gfe-button gfe-button--medium-emphasis gfe-button--middle-align']").get_attribute('href'))
    login_google(bc, email, password)
    bc.wait.until(EC.url_matches(ISettingData.TARGET_URL))
    
def donwload(bc: IBrowserControlData, url: str, file_path: Path, timeout: int = 10):
    bc.driver.get(url)
    
    while not file_path.exists() and timeout > 0:
        sleep(bc.wait._poll)
        timeout -= bc.wait._poll
        
        if timeout <= 0:
            raise TimeoutError(f'Timeout: {url}')
        
        if file_path.exists():
            return file_path