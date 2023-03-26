from selenium.webdriver.common.by import By
from time import sleep
from src.controls import Controls
from src import settings

def main():
    controls = Controls(settings.profile_path, settings.profile_name)
    controls.move('https://classroom.google.com/u/0/h')
    
try:
    main()
except BaseException as e:
    print('\033[31m')
    print(e)
    print('\033[0m')