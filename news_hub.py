import os
import json
import urllib.request
import urllib.error

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
STATE_FILE = "state.json"

# رابط API الأحداث والأخبار لـ War Era
API_URL = "https://gateway.warerastats.io/trpc/event.getEventsPaginated?batch=1&input=%7B%220%22%3A%7B%22json%22%3A%7B%22page%22%3A1%2C%22limit%22%3A10%7D%7D%7D"

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"seen_ids": []}

def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

def send_discord_embed(title, description, color=0x3498db):
    if not DISCORD_WEBHOOK_URL:
        print("Error: DISCORD_WEBHOOK_URL not set.")
        return
    
    payload = {
        "embeds": [
            {
                "title": title,
                "description": description,
                "color": color,
                "footer": {"text": "War Era News Hub • Automated Bot"}
            }
        ]
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        DISCORD_WEBHOOK_URL,
        data=data,
        headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    )
    try:
        with urllib.request.urlopen(req) as response:
            print(f"Webhook sent: {response.status}")
    except Exception as e:
        print(f"Error sending embed: {e}")

def fetch_events():
    req = urllib.request.Request(API_URL, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                raw_data = response.read().decode("utf-8")
                data = json.loads(raw_data)
                
                if isinstance(data, list) and len(data) > 0:
                    items = data[0].get("result", {}).get("data", {}).get("json", {}).get("items", [])
                    return items
                elif isinstance(data, dict):
                    items = data.get("result", {}).get("data",
