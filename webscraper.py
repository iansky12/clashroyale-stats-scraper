# Webscraper to pull from statsroyale.com top royales, top 1000 ish players.
# grab the id's of the image id's for the cards, and then use those id's to pull the card data from the statsroyale.com/api endpoint.
# Use the id's to pull the card data from the statsroyale.com/api endpoint.
# Store the data in a JSON file for further analysis.
# Use the id's to pull the card data from the statsroyale.com/api endpoint.

#testing if everything installed correctly

from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.google.com")
    print(f"Successfully navigated to {page.title()}")
    browser.close()