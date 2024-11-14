from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from CookieString import CookieString
from CookieUpgradeManager import CookieUpgradeManager
from SeleniumInstance import SeleniumInstance

class CookieClicker:
    
    _driver: WebDriver | None = None
    _is_running: bool = False
    _upgrade_manager: CookieUpgradeManager | None  = None
    
    def __init__(self):
        driver = SeleniumInstance.get_instance().get_driver()
        driver.get("https://orteil.dashnet.org/cookieclicker/")
        self._driver = driver
        
    def start_game(self):
        try:
            WebDriverWait(self._driver, 10).until(EC.visibility_of_element_located((By.XPATH, "(//p[normalize-space()='Consent'])[1]")))  
            website_cookie = self._driver.find_element(By.XPATH, "(//p[normalize-space()='Consent'])[1]")
            website_cookie.click()
            WebDriverWait(self._driver, 10).until(EC.visibility_of_element_located((By.XPATH, "(//div[@id='langSelect-FR'])[1]")))
            language_selector = self._driver.find_element(By.XPATH, "(//div[@id='langSelect-FR'])[1]")
            language_selector.click()
            WebDriverWait(self._driver, 10).until(EC.visibility_of_element_located((By.ID, "bigCookie")))
            self._is_running = True
            self._upgrade_manager = CookieUpgradeManager(self._driver, self)
            return True
        except Exception as e:
            raise Exception(f"The game shouldn't to lauch: {e}")
    
    def click_cookie(self):
        try:
            cookie = SeleniumInstance.wait_and_get_element(SeleniumInstance, By.ID, "bigCookie")
            cookie.click()
        except NoSuchElementException as e:
            raise Exception("The cookie element was not found on the page.") from e
        except ElementClickInterceptedException as e:
            raise Exception("The cookie element could not be clicked, another element may be blocking it.") from e
        except Exception as e:
            raise Exception(f"An unexpected error occurred while clicking the cookie: {e}")
        return True
    
    def get_number_of_cookies(self):
        try:
            cookie_count = self._driver.find_element(By.XPATH, "//*[@id='cookies']")
            return CookieString.format_number(CookieString, cookie_count.get_attribute("innerText").split()[0])
        except NoSuchElementException as e:
            raise Exception("The cookie count element was not found on the page.") from e
        except Exception as e:
            raise Exception(f"An unexpected error occurred while getting the number of cookies: {e}")
    
    def cookie_per_second(self):
        try:
            cookie_per_second = self._driver.find_element(By.XPATH, "//*[@id='cookies']").text
            return cookie_per_second.split("par seconde :")[-1].strip()
        except NoSuchElementException as e:
            raise Exception("The cookie per second element was not found on the page.") from e
        except Exception as e:
            raise Exception(f"An unexpected error occurred while getting the number of cookies per second: {e}")
    
    def game_is_running(self):
        return self._is_running
    
    def verify_upgrades(self):
        self._upgrade_manager.verify_upgrades()
        
    def buy_upgrade(self, upgrade_id):
        return self._upgrade_manager.buy_upgrade(upgrade_id)

    def quit_game(self):
        self._is_running = False
        self._driver.quit()