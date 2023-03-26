from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from time import sleep
import factory
import browser_control
from controls import Controls

def main():
    profile_path = r'C:\Users\kkyan\Documents\Code\Projects\Application\Classroom\chromeData'
    profile_name = 'Profile 1'
    controls = Controls(profile_path, profile_name)
    
    controls.move('https://classroom.google.com/u/0/h')
    
try:
    main()
except BaseException as e:
    print('\033[31m')
    print(e)
    print('\033[0m')