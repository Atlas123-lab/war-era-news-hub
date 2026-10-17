import os
import json
import urllib.request
import urllib.error

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
STATE_FILE = "state.json"
API_URL = "https://gateway.warerastats.io/events"  # أو رابط الأحداث الخاص بالـ Gateway

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
        headers={"Content-Type": "application/json", "User-Agent": "WarEraBot/1.0"}
    )
    try:
        with urllib.request.urlopen(req) as response:
            print(f"Notification sent successfully: {response.status}")
    except Exception as e:
        print(f"Error sending embed to Discord: {e}")

def fetch_gateway_data():
    req = urllib.request.Request(API_URL, headers={"User-Agent": "WarEraBot/1.0"})
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                data = response.read().decode("utf-8")
                return json.loads(data)
    except Exception as e:
        print(f"Error fetching data from Gateway: {e}")
    return None

def main():
    print("Checking for new War Era events...")
    state = load_state()
    seen_ids = set(state.get("seen_ids", []))
    
    events_data = fetch_gateway_data()
    
    if not events_data:
        print("No new data fetched or connection failed.")
        return

    # معالجة الأحداث الجديدة
    new_events_found = 0
    # افترضنا هنا أن الاستجابة مصفوفة من الأحداث أو كائن يحتوي على events
    events_list = events_data if isinstance(events_data, list) else events_data.get("events", [])

    for event in events_list:
        event_id = str(event.get("id"))
        if not event_id or event_id in seen_ids:
            continue
        
        # استخراج تفاصيل الحدث
        title = event.get("title", "حدث جديد في War Era ⚔️")
        description = event.get("description", "تفاصيل الحدث غير متوفرة حالياً.")
        
        # إرسال التنبيه لـ Discord
        send_discord_embed(title, description)
        
        seen_ids.add(event_id)
        new_events_found += 1

    # حفظ الأحداث المعالجة
    state["seen_ids"] = list(seen_ids)
    save_state(state)
    print(f"Processed {new_events_found} new events.")

if __name__ == "__main__":
    main()
