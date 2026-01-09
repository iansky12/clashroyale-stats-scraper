import json
import os
import time
import clashroyale
from dotenv import load_dotenv

# 1. Load security credentials from your .env file
load_dotenv()
token = os.getenv("CLASH_API_TOKEN")

# 2. Connect to the API (Using the RoyaleAPI proxy for stability)
# The authorization happens here: the library attaches your token to every request.
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
            
            # The 'current_deck' is a list of Card objects
            deck_cards = profile.current_deck
            
            # FEATURE 1: Average Elixir Calculation
            avg_elixir = sum([card.elixir_cost for card in deck_cards]) / 8
            
            # FEATURE 2: Rarity Breakdown
            # We count how many of each rarity are in the 8-card deck
            rarities = [card.rarity for card in deck_cards]
            rarity_counts = {
                "common": rarities.count("common"),
                "rare": rarities.count("rare"),
                "epic": rarities.count("epic"),
                "legendary": rarities.count("legendary"),
                "champion": rarities.count("champion")
            }
            
            player_data = {
                "rank": i + 1,
                "tag": f"#{tag}",
                "name": profile.name,
                "trophies": profile.trophies,
                "avg_elixir": round(avg_elixir, 2),
                "rarity_counts": rarity_counts,
                "deck": [card.name for card in deck_cards]
            }
            results.append(player_data)
            
            # Progress tracker
            if (i + 1) % 50 == 0 or (i + 1) == total:
                print(f"📦 Progress: {i + 1}/{total} players harvested...")
            
            # Stay under the rate limit (10 requests per second)
            time.sleep(0.1) 

        except Exception as e:
            print(f"⚠️ Skipping {tag} (Error: {e})")
            continue

    # 3. Save the final high-quality dataset
    with open("ml_clash_data.json", "w") as f:
        json.dump(results, f, indent=4)
    
    print(f"\n✅ DONE! Saved {len(results)} player profiles to ml_clash_data.json")

if __name__ == "__main__":
    harvest()