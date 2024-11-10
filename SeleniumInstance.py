from selenium import webdriver
from selenium.webdriver.chrome.service import Service
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
            cls._driver = webdriver.Chrome(service=service)
            cls._instance = cls()

        return cls._instance

    def get_driver(self):
        if self._instance is None:
            self.get_instance()
        return self._driver