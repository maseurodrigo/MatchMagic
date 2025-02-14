import os # Import os for operating system functionalities

from typing import List, Dict, Tuple
from seleniumwire import webdriver  # Import webdriver with Selenium Wire for intercepting requests
from selenium.webdriver.chrome.service import Service as ChromeService  # Import service to manage ChromeDriver
from selenium.webdriver.chrome.options import Options  # Import Options to configure ChromeDriver options
from selenium.webdriver.common.by import By  # Import By to locate elements
from webdriver_manager.chrome import ChromeDriverManager  # Import ChromeDriverManager to automatically manage ChromeDriver

def ScrapeRedCards(username: str, password: str, proxy: str, stored_cards: List[Tuple[str, str]]) -> Dict[str, List[Tuple[str, str]]]:

    # Copy the stored_cards to a new list to manipulate it
    new_stored_cards = stored_cards.copy()

    # Initialize an empty string
    data_string = ""

    # Set up the proxy and SSL verification options for Selenium Wire
    seleniumwire_options = {
        "proxy":{
            # "https": 'https://user-%s:%s@%s' % (username, password, proxy),
            "https": 'https://customer-resi_denver__3Aym0-sessid-0784236650-sesstime-10:Q=Z55mxo58aX5f5pg@pr.oxylabs.io:7777',
            "verify_ssl": True,
        }
    }

    # Open Chrome
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')      # Run Chrome in headless mode (without a GUI)
    options.add_argument('--disable-gpu')   # Disable GPU acceleration (necessary for some headless environments)
    options.add_argument('--log-level=3')   # Set logging level to 3 (suppress most logs)
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')

    # Initialize the Chrome WebDriver with the specified options and proxy settings
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options, seleniumwire_options=seleniumwire_options)

    # URL of the website to be scraped
    driver.get("https://www.flashscore.com/")
    
    # Accept GDPR (General Data Protection Regulation) popup if it appears
    try:
        driver.find_element(By.CSS_SELECTOR, "button#onetrust-accept-btn-handler").click()
    except:
        # print("Cookies already closed!")
        pass

    # Try to open the Live tab
    try:
        driver.find_element(By.CSS_SELECTOR, "div#live-table > div.filters > div.filters__group > div:nth-child(2)").click()
    except:
        # print("Can't Open Live Matches!")
        pass

    # Try to expand the all competitions within the live matches
    try:
        hide_comps = driver.find_elements(By.CSS_SELECTOR, "div#live-table div.wclLeagueHeader--noCheckBox")

        for comp in hide_comps:
            comp.find_element(By.CSS_SELECTOR, "button[data-testid='wcl-accordionButton']").click()
    except:
        # print("Can't Open Competition!")
        pass

    # Look for live matches that have a red card incident and print the teams involved
    try:
        all_games = driver.find_elements(By.CSS_SELECTOR, "div.event__match--live")

        for game in all_games:
            if game.find_elements(By.CSS_SELECTOR, "svg[data-testid='wcl-icon-incidents-red-card']"):
                home_team = game.find_element(By.CSS_SELECTOR, 'div.event__homeParticipant > span').get_attribute('innerHTML')
                away_team = game.find_element(By.CSS_SELECTOR, 'div.event__awayParticipant > span').get_attribute('innerHTML')

                # Check if either home_team or away_team is equal to "GOAL"
                if home_team == "GOAL" or away_team == "GOAL":
                    pass
                else:
                    # Define the specific pair (home & away teams) to search for
                    current_Teams = (home_team, away_team)

                    # Check if the exact key-value pair is present in the array
                    teams_present = current_Teams in new_stored_cards

                    if teams_present:
                        pass
                    else:
                        new_stored_cards.append(current_Teams) # Add new pair to the array
                        data_string += f"""\n🚩 Red Card: {home_team} vs {away_team}!"""
    except:
        pass

    # Close the browser and end the WebDriver session
    driver.quit()

    # Create the results dictionary with the data_string as the key
    toReturn = {data_string: new_stored_cards}
    
    return toReturn if data_string else {"": new_stored_cards}


def ScrapeExtraTimes(username: str, password: str, proxy: str, stored_extra_times: List[Tuple[str, str]]) -> Dict[str, List[Tuple[str, str]]]:

    # Copy the stored_extra_times to a new list to manipulate it
    new_stored_extra_times = stored_extra_times.copy()

    # Initialize an empty string
    data_string = ""

    # Set up the proxy and SSL verification options for Selenium Wire
    seleniumwire_options = {
        "proxy":{
            "https": 'https://user-%s:%s@%s' % (username, password, proxy),
            "verify_ssl": True,
        }
    }

    # Open Chrome
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')      # Run Chrome in headless mode (without a GUI)
    options.add_argument('--disable-gpu')   # Disable GPU acceleration (necessary for some headless environments)
    options.add_argument('--log-level=3')   # Set logging level to 3 (suppress most logs)
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')

    # Initialize the Chrome WebDriver with the specified options and proxy settings
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options, seleniumwire_options=seleniumwire_options)

    # URL of the website to be scraped
    driver.get("https://www.flashscore.com/")
    
    # Accept GDPR (General Data Protection Regulation) popup if it appears
    try:
        driver.find_element(By.CSS_SELECTOR, "button#onetrust-accept-btn-handler").click()
    except:
        # print("Cookies already closed!")
        pass

    # Try to open the Live tab
    try:
        driver.find_element(By.CSS_SELECTOR, "div#live-table > div.filters > div.filters__group > div:nth-child(2)").click()
    except:
        # print("Can't Open Live Matches!")
        pass

    # Try to expand the all competitions within the live matches
    try:
        hide_comps = driver.find_elements(By.CSS_SELECTOR, "div#live-table div.wclLeagueHeader--noCheckBox")

        for comp in hide_comps:
            comp.find_element(By.CSS_SELECTOR, "button[data-testid='wcl-accordionButton']").click()
    except:
        # print("Can't Open Competition!")
        pass

    # Look for live matches that are in extra time and print the teams involved
    try:
        all_games = driver.find_elements(By.CSS_SELECTOR, "div.event__match--live")

        for game in all_games:

            current_game = game.find_element(By.CSS_SELECTOR, "div.event__stage > div").get_attribute('innerHTML')

            if "Extra Time" in current_game:  
                home_team = game.find_element(By.CSS_SELECTOR, 'div.event__homeParticipant > span').get_attribute('innerHTML')
                away_team = game.find_element(By.CSS_SELECTOR, 'div.event__awayParticipant > span').get_attribute('innerHTML')
                
                # Define the specific pair (home & away teams) to search for
                current_Teams = (home_team, away_team)

                # Check if the exact key-value pair is present in the array
                teams_present = current_Teams in new_stored_extra_times

                if teams_present:
                    pass
                else:
                    new_stored_extra_times.append(current_Teams) # Add new pair to the array
                    data_string += f"""\n⏰ Extra Time: {home_team} vs {away_team}!"""
            else:
                pass    
    except:
        pass

    # Close the browser and end the WebDriver session
    driver.quit()

    # Create the results dictionary with the data_string as the key
    toReturn = {data_string: new_stored_extra_times}
    
    return toReturn if data_string else {"": new_stored_extra_times}