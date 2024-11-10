from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from SeleniumInstance import SeleniumInstance

class CookieClicker:
    
    _driver = None
    
    def __init__(self):
        driver = SeleniumInstance.get_instance().get_driver()
        driver.get("https://orteil.dashnet.org/cookieclicker/")
        time.sleep(5)
        self._driver = driver
    
    def quit_game(self):
        self._driver.quit()