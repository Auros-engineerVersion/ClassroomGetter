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

COLLEGE_IDENTIFIER = 'shibboleth.nihon-u.ac.jp/idp/profile/SAML2/Redirect'
COLLEGE_USER_FORM = "//input[@id='j_username']"
COLLEGE_PASS_FORM = "//input[@id='j_password']"
COLLEGE_SUBMIT_BUTTON = "//button[@type='submit']"

GOOGLE_EDU = 'workspace-for-education'
GOOGLE_EDU_URL = 'https://edu.google.com/intl/ALL_jp/workspace-for-education/classroom/'

GOOGLE_IDENTIFIER = 'accounts.google.com'
GOOGLE_IDENTIFIER_URL = 'https://accounts.google.com/ServiceLogin?continue=https%3A%2F%2Fclassroom.google.com&passive=true'
GOOGLE_EMAIL_FORM = "//input[@type='email']"
GOOGLE_SUBMIT_BUTTON = "//div[@id='identifierNext']"
GOOGLE_ASK_DO_LOGIN_URL = 'https://accounts.google.com/speedbump/samlconfirmaccount'
GOOGLE_ASK_DO_LOGIN_BUTTON = "//div[@jsname='Njthtb']"

def move(bc: IBrowserControlData, url: str):
    bc.driver.get(url)
    
def wait(bc: IBrowserControlData, url: str):
    return bc.wait.until(EC.url_matches(url))
        
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
    except TimeoutException or InvalidSelectorException:
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
            sample_buttons = search_element_all(bc, "//div[@jsmodel='RH7Ihb']")
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
    
def college_login(bc: IBrowserControlData, email: str, password: str):
    #1:emailの@以前をユーザー名に送る
    #2:passwordを送る
    #3:ログインボタンを押す
    try:
        wait(bc, COLLEGE_IDENTIFIER)
        search_element(bc, COLLEGE_USER_FORM).send_keys(email[:email.find('@')])
        search_element(bc, COLLEGE_PASS_FORM).send_keys(password)
        search_element(bc, COLLEGE_SUBMIT_BUTTON).click()
    except TimeoutException:
        return

def google_login(bc: IBrowserControlData, email: str, password: str):
    move(bc, GOOGLE_IDENTIFIER_URL)
    wait(bc, GOOGLE_IDENTIFIER)
    search_element(bc, GOOGLE_EMAIL_FORM).send_keys(email) #1:emailを入力する
    search_element(bc, GOOGLE_SUBMIT_BUTTON).click()#2:続行を押す

    college_login(bc, email, password)
    search_element(bc, GOOGLE_ASK_DO_LOGIN_BUTTON).click()

def classroom_login(bc: IBrowserControlData, email: str, password: str) -> None:
    move(bc, ISettingData.TARGET_URL)
    if ISettingData.TARGET_URL in bc.current_url:
        return #ログイン済みの場合は何もしない
    #google educationのワークスペースに飛ばされた場合
    elif GOOGLE_EDU in bc.current_url:
        google_login(bc, email, password)
    else:
        raise ConnectionError(
            'Googleのログイン画面に移動できませんでした\nログインを行う必要がないか、urlが変更された可能性があります')
    
def donwload(bc: IBrowserControlData, url: str, file_path: Path, timeout: int = 10):
    move(bc, url)
    
    while not file_path.exists() and timeout > 0:
        sleep(bc.wait._poll)
        timeout -= bc.wait._poll
        
        if timeout <= 0:
            raise TimeoutError(f'Timeout: {url}')
        
        if file_path.exists(): #ダウンロードが完了した場合
            return file_path