from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

def get_lesson_sections(soupObj: BeautifulSoup):
    time.sleep(2)
    section_class_name = 'qhnNic LBlAUc Aopndd TIunU ZoT1D idtp4e DkDwHe'
    sections = soupObj.find_all('', class_=section_class_name)

def get_lesson_link(driver: webdriver, soupObj: BeautifulSoup):
    time.sleep(2)
    base_url = soupObj.find('base')['href']
    print(base_url)
    lessons = soupObj.find_all('a', class_='onkcGd ZmqAt Vx8Sxd') #aタグを検索
    lesson_links = [urljoin(base_url, value['href']) for value in lessons]
    return lesson_links