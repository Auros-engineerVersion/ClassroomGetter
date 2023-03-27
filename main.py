import settings as cfg
from selenium.webdriver.common.by import By
from src.controls import Controls
from urllib.parse import urljoin
import time
from src import factory

try:
    controls = Controls(cfg.PROFILE_PATH, cfg.PROFILE_NAME)
    controls.move(cfg.TARGET_URL)
    time.sleep(10)
    hrefs = controls.hrefs(cfg.LESSON_CLASS_NAME)
    for href in hrefs:
        print(href)
        
except Exception as e:
    print('\033[31m')
    print(e)
    print('\033[0m')