from dotenv import load_dotenv

from CookieClicker import CookieClicker

load_dotenv(".env")

cookie_clicker = CookieClicker()

def main():
    if cookie_clicker.start_game():
        while cookie_clicker.game_is_running():
            cookie_clicker.click_cookie()
            print(cookie_clicker.get_number_of_cookies())
            print(cookie_clicker.cookie_per_second())
    print("The game is over.")
    
if __name__ == "__main__":
    main()