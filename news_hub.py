import os
import json
import urllib.request
import urllib.error

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
STATE_FILE = "state.json"
API_URL = "https://gateway.warerastats.io/"

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {"seen_ids": []}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def main():
    print("Running War Era News Hub check...")
    state = load_state()
    
    try:
        req = urllib.request.Request(API_URL, headers={"User-Agent": "WarEraBot/1.0"})
        with urllib.request.urlopen(req) as response:
            print("Successfully connected to War Era Gateway.")
    except Exception as e:
        print(f"Failed to fetch gateway: {e}")

if __name__ == "__main__":
    main()
