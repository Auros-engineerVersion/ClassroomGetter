from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from re import search

from src.factory import create_driver
from src.setting_data import SettingData

class BrowserControls:
    def __init__(self, setting: SettingData) -> None:
        self.__settings = setting
        self.driver = create_driver(*setting.profile)
        self.wait = WebDriverWait(self.driver, 3)
        pass
    
    def __del__(self):
        del self.wait
        self.driver.quit()
        del self.driver
        pass
    
    def move(self, url: str):
        self.driver.get(url)
        
    def serch(self, xpath: str) -> WebElement:
        return self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    
    def click_all_sections(self, func, locator_and_pattern: tuple):
        def __move_and_click(elem: WebElement):
            self.driver.execute_script("arguments[0].scrollIntoView(true);", elem)
            self.driver.execute_script('arguments[0].click()', elem)

        #一つめは3点ボタン、2つめは「リンクをコピー」へのxpath
        links = []
        xpathes = ["//div[@class='SFCE1b']"]
        
        try:
            buttons = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, xpathes[0])))
            
        except TimeoutException:
            return []
        
        self.wait._timeout /= 10 #ファイルの読み込みは早いため
        for button in buttons:
            __move_and_click(button)
            links.extend(func()(*locator_and_pattern))
            
        self.wait._timeout *= 10 #元に戻す
        return links
        
    def hrefs(self):
        def __get_hrefs(locator, pattern: str = ''):
            unique_links = set() #重複処理のため
            try:
                elems = self.wait.until(EC.presence_of_all_elements_located(locator))
            except TimeoutException:
                return unique_links
            
            for elem in elems:
                link = str(elem.get_attribute('href'))
                #文字列が見つかれば
                if (search(pattern, string=link) != None):
                    unique_links.add(link)
            return unique_links
        
        return __get_hrefs
    
    def profile_check(self, setting_data: SettingData):
        #profileが何も記入されていないのなら新しく入力する
        if (setting_data.profile_path == None or setting_data.profile_name == None):
            self.move('chrome://version/')
            path = self.serch("//td[@id='profile_path']").text

            profile_name = path[search('(?<=User Data.).*', path).span()[0]:]
            profile_path = path.replace(profile_name, '')[:-1] #最後のバックスラッシュを削除している
            
            setting_data.profile_path = profile_path
            setting_data.profile_name = profile_name

    
    def login_college_form(self, email: str, user_password: str):
        befor_at_index = email.find('@')
        user_name = email[:befor_at_index]
        
        #1:emailの@以前をユーザー名に送る
        #2:passwordを送る
        #3:ログインボタンを押す
        self.serch("//input[@id='j_username']").send_keys(user_name)
        self.serch("//input[@id='j_password']").send_keys(user_password)
        self.serch("//button[@type='submit']").click()
    
    def login_google(self, email: str, user_password: str):
        #1:emailを入力する
        #2:続行を押す
        #3:大学のフォームにログイン
        #4:続行を押す
        self.serch("//input[@type='email']")        .send_keys(email)
        self.serch("//div[@id='identifierNext']")   .click()
        self.login_college_form(email, user_password)
        self.serch("//div[@jsname='Njthtb']")       .click()
        
    def login_classroom(self, email: str, user_password: str):
        #1:「Classroomにログイン」のボタンを押す
        #2:Googleにログインする
        #3:プロファイルを設定する
        self.serch("//a[@class='gfe-button gfe-button--medium-emphasis gfe-button--middle-align']").click
        self.login_google(email, user_password)
        self.profile_check(self.__settings)