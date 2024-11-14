from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains

import os

class SeleniumInstance:
    
    _instance = None
    _driver = None

    @classmethod 
    def get_instance(cls):
        if cls._instance is None:
            driver_path = os.environ.get('CHROME_DRIVER_PATH')
            if not driver_path:
                raise ValueError("Le chemin du ChromeDriver doit être défini dans le fichier .env avec 'CHROME_DRIVER_PATH'.")
            service = Service(driver_path)
            chrome_options = Options()
            chrome_options.add_argument("--incognito")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--no-sandbox")
            cls._driver = webdriver.Chrome(service=service)
            cls._instance = cls()
        return cls._instance

    def get_driver(self):
        if self._instance is None:
            self.get_instance()
        return self._driver

    def wait_and_get_element(cls, by, value, driver = None) -> WebElement:
        try:
            if cls._driver is None:
                cls.get_instance()
            if driver is None:
                driver = cls._driver
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, value)))
            return cls._driver.find_element(by, value)
        except Exception as e:
            raise Exception(f"An error occurred while waiting for the element: {e}")
        
    def wait_hover_and_get_element(cls, element: WebElement):
        try:
            WebDriverWait(cls._driver, 10).until(EC.visibility_of(element))
            actions = ActionChains(cls._driver)
            actions.move_to_element(element).perform()
        except Exception as e:
            raise Exception(f"An error occurred while waiting for the element to be visible: {e}")