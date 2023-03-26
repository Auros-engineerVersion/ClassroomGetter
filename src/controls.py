from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .factory import create_driver

class Controls:
    def __init__(self, profile_path: str, profile_name: str) -> None:
        self._driver = create_driver(profile_path, profile_name)
        self._wait = WebDriverWait(self._driver, 30)
        pass
    
    def move(self, url: str):
        self._driver.get(url)
        self._wait.until(EC.presence_of_all_elements_located)
        self._current_html = self._driver.page_source.encode('utf-8')
        
        return self # Linqライクにするため
        
    # classroomに入った時点に表示される科目のurlを取得する
    def lesson_links(self, class_name: str = 'onkcGd ZmqAt Vx8Sxd'):
        base_url = self._driver.find_element(By.__name__, 'base')
        print(base_url)
        