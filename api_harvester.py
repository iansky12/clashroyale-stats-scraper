import json
import os
import time
import clashroyale
from dotenv import load_dotenv

# 1. Load security credentials from your .env file
load_dotenv()
token = os.getenv("CLASH_API_TOKEN")

# 2. Connect to the API (Using the RoyaleAPI proxy for stability)
client = clashroyale.OfficialAPI(token, url="https://proxy.royaleapi.dev/v1")

def harvest():
    try:
        # Load the 789 IDs we scouted
        with open("player_tags.txt", "r") as f:
            tags = [line.strip().replace("#", "") for line in f.readlines()]
    except FileNotFoundError:
        print("❌ Error: player_tags.txt not found! Run id_scout.py first.")
        return

    results = []
    total = len(tags)
    print(f"🚀 Starting harvest of {total} players...")

    for i, tag in enumerate(tags):
        try:
            # Request the full profile from Supercell
            profile = client.get_player(tag)
            
            # Extract the current deck
            deck = [card.name for card in profile.current_deck]
            
            player_data = {
                "rank": i + 1,
                "tag": f"#{tag}",
                "name": profile.name,
                "trophies": profile.trophies,
                "deck": deck
            }
            results.append(player_data)
            
            # Show progress every 50 players
            if (i + 1) % 50 == 0 or (i + 1) == total:
                print(f"📦 Progress: {i + 1}/{total} players harvested...")
            
            # Respect the API (10 requests per second max)
            time.sleep(0.1) 

        except Exception as e:
            # If one player fails, we don't want to stop the whole script
            print(f"⚠️ Skipping {tag} (Error: {e})")
            continue

    # 3. Save the final high-quality dataset
    with open("ml_clash_data.json", "w") as f:
        json.dump(results, f, indent=4)
    
    print(f"\n✅ DONE! Your AI-ready dataset is saved to ml_clash_data.json")

if __name__ == "__main__":
    harvest()