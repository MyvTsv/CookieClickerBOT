import re

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from CookieString import CookieString
from CookieUpgrade import CookieUpgrade
from SeleniumInstance import SeleniumInstance

class CookieUpgradeManager:
    
    _upgrades = {}
    _driver: WebDriver | None = None
    _cookie_clicker = None
    
    def __init__(self, driver, cookie_clicker):
        self._driver = driver
        self._cookie_clicker = cookie_clicker
        
    def get_upgrades(self) -> dict:
        return self._upgrades

    def verify_upgrades(self):
        def filter_upgrade_items(item: WebElement):
            return re.match(r"^product\d+$", item.get_attribute("id"))
        try:
            upgrades = list(filter(filter_upgrade_items, self.get_upgrade_menu_items()))
            for upgrade in upgrades:
                self.verify_upgrade(upgrade)
        except NoSuchElementException as e:
            raise Exception("The upgrade elements were not found on the page.") from e
        except Exception as e:
            raise Exception(f"An unexpected error occurred while verifying the upgrades: {e}")

    def verify_upgrade(self, upgrade: WebElement):
        upgrade_id = upgrade.get_attribute("id").split("product")[1]
        if upgrade_id not in self._upgrades:
            upgrade_name = upgrade.find_element(By.ID, "productName" + upgrade_id).get_attribute("innerText")
            self._upgrades[upgrade_id] = CookieUpgrade(upgrade_id, upgrade_name)
        tooltip = self.get_upgrade_tooltip_info(upgrade)
        if not tooltip:
            return False
        upgrade_item = self.get_upgrade_item(upgrade_id)
        upgrade_cost = self._driver.find_element(By.ID, "productPrice" + upgrade_id).get_attribute("innerText")
        upgrade_cost = CookieString.format_number(CookieString, upgrade_cost)
        upgrade_item.set_cost(upgrade_cost)
        print(upgrade_item)
    
    def get_upgrade_tooltip_info(self, upgrade: WebElement) -> bool:
        try:
            upgrade_id = upgrade.get_attribute("id").split("product")[1]
            upgrade_item = self.get_upgrade_item(upgrade_id)
            upgrade_classes = upgrade.get_attribute("class")
            if "disabled" in upgrade_classes:
                return False
            if upgrade_item.get_level() == 0:
                return False
            SeleniumInstance.wait_hover_and_get_element(SeleniumInstance, upgrade)
            tooltip = SeleniumInstance.wait_and_get_element(SeleniumInstance, By.XPATH, "//*[contains(@id, 'tooltip')]")
            upgrade_cps = SeleniumInstance.wait_and_get_element(SeleniumInstance, By.XPATH, ".//div[contains(@class, 'descriptionBlock')]", tooltip)
        except Exception as e:
            print(f"Erreur lors de la récupération des informations de l'upgrade : {e}")
            return False
        return True

    
    def get_upgrade_menu_items(self) -> list[WebElement]:
        try:
            WebDriverWait(self._driver, 10).until(EC.presence_of_element_located((By.ID, "products")))
            upgrades_menu = self._driver.find_element(By.ID, "products")
            return upgrades_menu.find_elements(By.XPATH, ".//div[contains(@id, 'product')]")
        except NoSuchElementException as e:
            raise Exception("The upgrades menu was not found on the page.") from e
        except Exception as e:
            raise Exception(f"An unexpected error occurred while getting the upgrades menu items: {e}")
        
    def get_upgrade_item(self, upgrade_id) -> CookieUpgrade:
        try:
            return self._upgrades[upgrade_id]
        except KeyError as e:
            raise Exception(f"No upgrade found with id: {upgrade_id}") from e
        except Exception as e:
            raise Exception(f"An unexpected error occurred while getting the upgrade: {e}")
        
    def buy_upgrade(self, upgrade_id):
        try:
            if upgrade_id not in self._upgrades:
                raise Exception(f"No upgrade found with id: {upgrade_id}")
            cookie_count = int(self._cookie_clicker.get_number_of_cookies())
            upgrade_item = self.get_upgrade_item(upgrade_id)
            upgrade_cost = int(upgrade_item.get_cost())
            print(f"Cookie count: {cookie_count} | Upgrade cost: {upgrade_cost}")
            if cookie_count >= upgrade_cost:
                upgrade = self._driver.find_element(By.ID, "product" + upgrade_id)
                upgrade.click()
                upgrade_item.set_level(upgrade_item.get_level() + 1)
                return True
            return False
        except NoSuchElementException as e:
            raise Exception("The upgrade element was not found on the page.") from e
        except ElementClickInterceptedException as e:
            raise Exception("The upgrade element could not be clicked, another element may be blocking it.") from e
        except Exception as e:
            raise Exception(f"An unexpected error occurred while buying the upgrade: {e}")
