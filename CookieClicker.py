from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from SeleniumInstance import SeleniumInstance

class CookieClicker:
    
    _driver = None
    _is_running = False
    
    def __init__(self):
        driver = SeleniumInstance.get_instance().get_driver()
        driver.get("https://orteil.dashnet.org/cookieclicker/")
        self._driver = driver
        
    def start_game(self):
        try:     
            website_cookie = self._driver.find_element(By.XPATH, "(//p[normalize-space()='Consent'])[1]")
            website_cookie.click()
            language_selector = self._driver.find_element(By.XPATH, "(//div[@id='langSelect-FR'])[1]")
            language_selector.click()
            if self.waiting_game_load():
                self._is_running = True
                return True
            else:
                raise Exception("The game did not load in time.")
        except Exception as e:
            raise Exception(f"The game shouldn't to lauch: {e}")
    
    def waiting_game_load(self):
        try:
            WebDriverWait(self._driver, 10).until(EC.presence_of_element_located((By.ID, "bigCookie")))
            return True
        except NoSuchElementException as e:
            return False
        except Exception as e:
            raise Exception(f"An unexpected error occurred while waiting for the game to load: {e}")
    
    def click_cookie(self):
        try:
            cookie = self._driver.find_element(By.ID, "bigCookie")
            cookie.click()
        except NoSuchElementException as e:
            raise Exception("The cookie element was not found on the page.") from e
        except ElementClickInterceptedException as e:
            raise Exception("The cookie element could not be clicked, another element may be blocking it.") from e
        except Exception as e:
            raise Exception(f"An unexpected error occurred while clicking the cookie: {e}")
        return True
    
    def game_is_running(self):
        return self._is_running
    
    def quit_game(self):
        self._is_running = False
        self._driver.quit()