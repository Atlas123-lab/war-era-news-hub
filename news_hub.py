import os
import json
import urllib.request
import urllib.error

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
STATE_FILE = "state.json"

# رابط الـ Gateway الرسمي لـ War Era tRPC
API_URL = "https://gateway.warerastats.io/trpc/event.getEventsPaginated"

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
            print(f"Webhook status: {response.status}")
    except Exception as e:
        print(f"Error sending embed: {e}")

def fetch_events():
    payload = json.dumps({"json": {"page": 1, "limit": 5}}).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    )
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                # استخراج القائمة من استجابة tRPC
                events = data.get("result", {}).get("data", {}).get("json", {}).get("items", [])
                return events
    except Exception as e:
        print(f"Error fetching gateway: {e}")
    return []

def main():
    print("Checking for new War Era events...")
    state = load_state()
    seen_ids = set(state.get("seen_ids", []))
    
    events = fetch_events()
    new_events_count = 0
    
    for ev in events:
        ev_id = str(ev.get("id") or ev.get("_id"))
        if not ev_id or ev_id in seen_ids:
            continue
        
        title = ev.get("title") or ev.get("name") or "حدث جديد في War Era ⚔️"
        description = ev.get("description") or ev.get("content") or "تم تسجيل حدث جديد باللعبة."
        
        send_discord_embed(f"⚔️ {title}", description)
        seen_ids.add(ev_id)
        new_events_count += 1
    
    state["seen_ids"] = list(seen_ids)
    save_state(state)
    print(f"Finished check. New events sent: {new_events_count}")

if __name__ == "__main__":
    main()
