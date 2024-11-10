from dotenv import load_dotenv

from CookieClicker import CookieClicker

load_dotenv(".env")

cookie_clicker = CookieClicker()

cookie_clicker.quit_game()