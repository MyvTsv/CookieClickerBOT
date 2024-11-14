from dotenv import load_dotenv

from CookieClicker import CookieClicker

load_dotenv(".env")

cookie_clicker = CookieClicker()

def main():
    if cookie_clicker.start_game():
        while cookie_clicker.game_is_running():
            cookie_clicker.click_cookie()
            cookie_clicker.verify_upgrades()
            cookie_clicker.buy_upgrade("0")
            #cookie_clicker.quit_game()
    print("The game is over.")
    
if __name__ == "__main__":
    main()