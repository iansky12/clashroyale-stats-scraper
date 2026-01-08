import json
import time
import random
from playwright.sync_api import sync_playwright

def save_player_data(data):
    filename = "clash_data.json"
    try:
        with open(filename, "r") as f:
            file_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        file_data = []
    file_data.append(data)
    with open(filename, "w") as f:
        json.dump(file_data, f, indent=4)

def run_scraper():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()
        page.set_default_timeout(60000)

        print("--- Step 1: Scouting Leaderboard ---")
        page.goto("https://royaleapi.com/players/leaderboard", wait_until="domcontentloaded")
        page.wait_for_selector("#roster")
        
        player_rows = page.locator("#roster tr[data-tag]").all()
        tags = [row.get_attribute("data-tag") for row in player_rows if row.get_attribute("data-tag")]
        print(f"Scouted {len(tags)} IDs. Starting the Harvest...")

        for tag in tags[:100]:
            try:
                print(f"Scraping {tag}...")
                page.goto(f"https://royaleapi.com/player/{tag}/decks", wait_until="domcontentloaded")
                
                # Wait for the first deck segment to appear
                page.wait_for_selector("#deck_0", timeout=15000)
                
                # Target images specifically inside the first deck that have the data-card-key
                card_elements = page.locator("#deck_0 img[data-card-key]").all()

                if len(card_elements) >= 8:
                    # Extract the card keys for the first 8 cards
                    deck = [card_elements[i].get_attribute("data-card-key") for i in range(8)]
                    save_player_data({"player_id": tag, "deck": deck})
                    print(f"  ✅ Saved Deck: {deck[:3]}...")
                else:
                    print(f"  ⚠️ Only found {len(card_elements)} cards for {tag}")

                time.sleep(random.uniform(2, 4))
            except Exception as e:
                print(f"  ❌ Error on {tag}: Element not found")

        browser.close()
    print("\n--- ALL DONE ---")

if __name__ == "__main__":
    run_scraper()

