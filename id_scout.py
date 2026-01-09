import time
from playwright.sync_api import sync_playwright

def scout_ids():
    with sync_playwright() as p:
        print("🚀 Launching browser...")
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            print("🌐 Navigating to RoyaleAPI...")
            page.goto("https://royaleapi.com/players/leaderboard", wait_until="domcontentloaded")
            
            # Open dropdown
            print("🖱️ Clicking rows dropdown...")
            page.locator(".ui.pointing.dropdown.link.item").first.click()
            
            # Select 1000 
            print("🚀 Selecting '1000' rows...")
            page.locator("a.rowperpage.item", has_text="1000").first.click()

            # Wait for at least 500 rows to appear visually
            print("⏳ Waiting for rows to appear on screen...")
            page.wait_for_selector("#roster tr:nth-child(500)", timeout=20000)
            
            # Give it 3 extra seconds to finish rendering the remaining 287+ rows
            print("🕒 Finalizing render...")
            time.sleep(3) 

            # Extract IDs
            rows = page.locator("#roster tr[data-tag]").all()
            all_tags = [row.get_attribute("data-tag") for row in rows]
            
            if len(all_tags) > 0:
                with open("player_tags.txt", "w") as f:
                    for tag in all_tags:
                        f.write(f"{tag}\n")
                print(f"✅ Success! Captured {len(all_tags)} IDs.")
            else:
                print("❌ Failed: No tags found.")

        except Exception as e:
            print(f"❌ Failed: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    scout_ids()
