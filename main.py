import settings as cfg
from selenium.webdriver.common.by import By
from src.controls import Controls

try:
    controls = Controls(cfg.PROFILE_PATH, cfg.PROFILE_NAME)
    controls.move(cfg.TARGET_URL)
    hrefs = controls.hrefs()
    
    print(len(hrefs))
    for href in hrefs:
        print(href)
        
except Exception as e:
    print('\033[31m')
    print(e)
    print('\033[0m')