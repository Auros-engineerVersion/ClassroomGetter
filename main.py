import settings as cfg
from selenium.webdriver.common.by import By
from src.controls import Controls

try:
    controls = Controls(cfg.PROFILE_PATH, cfg.PROFILE_NAME)
    controls.move(url=cfg.TARGET_URL, wait_time=10)
    #文字列の範囲を10からにすると、/archivedというpathも含まれてしまう
    #11にすれば大丈夫
    hrefs = controls.hrefs(controls.wait, '^.+/0/.{11,20}$')
    
    print(len(hrefs))
    for href in hrefs:
        print(href)
        
except Exception as e:
    print('\033[31m')
    print(e)
    
finally:
    print('\033[0m')