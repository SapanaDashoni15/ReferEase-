# linkedin_scrapper.py
import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

load_dotenv()

LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

def linkedin_login():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get("https://www.linkedin.com/login")
    print("🌐 Opening LinkedIn login page...")

    # Wait for login fields
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "username"))
    )

    driver.find_element(By.ID, "username").send_keys(LINKEDIN_EMAIL)
    driver.find_element(By.ID, "password").send_keys(LINKEDIN_PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Wait until login completes
    WebDriverWait(driver, 20).until(
        EC.url_contains("feed")
    )
    print("✅ Logged in successfully!")

    return driver


def open_profile_and_scrape(driver):
    driver.get("https://www.linkedin.com/in/sapana-dashoni-29a28724b/") 
    print("👩‍💼 Opening your LinkedIn profile...")
    time.sleep(5)

    # Click on 'Connections'
    try:
        connections_link = driver.find_element(By.PARTIAL_LINK_TEXT, "connections")
        connections_link.click()
        print("✅ Opened Connections page.")
    except Exception as e:
        print("⚠️ Could not open connections:", e)
        return

    time.sleep(5)

    # Scroll until all connections are loaded
    last_height = driver.execute_script("return document.body.scrollHeight")
    print("🔽 Scrolling to load all connections...")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    print("✅ Finished scrolling.")

    # Extract connection info
    names, occupations, links = [], [], []
    cards = driver.find_elements(By.CSS_SELECTOR, "li.mn-connection-card")

    for card in cards:
        try:
            name = card.find_element(By.CSS_SELECTOR, ".mn-connection-card__name").text.strip()
            occupation = card.find_element(By.CSS_SELECTOR, ".mn-connection-card__occupation").text.strip()
            link = card.find_element(By.TAG_NAME, "a").get_attribute("href").split("?")[0]
            names.append(name)
            occupations.append(occupation)
            links.append(link)
        except:
            continue

    df = pd.DataFrame({
        "Name": names,
        "Occupation": occupations,
        "Profile Link": links
    })
    df.to_csv("../output/connections.csv", index=False)
    print(f"✅ Saved {len(df)} connections to output/connections.csv")

    driver.quit()


if __name__ == "__main__":
    driver = linkedin_login()
    open_profile_and_scrape(driver)
