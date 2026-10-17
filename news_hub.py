import os
import json
import urllib.request
import urllib.error

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
STATE_FILE = "state.json"

# مسارات التجربة المباشرة للأخبار والأحداث
ENDPOINTS = [
    "https://gateway.warerastats.io/api/events",
    "https://gateway.warerastats.io/api/news",
    "https://gateway.warerastats.io/trpc/event.getEventsPaginated?batch=1&input=%7B%220%22%3A%7B%22json%22%3A%7B%22page%22%3A1%2C%22limit%22%3A5%7D%7D%7D"
]

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

def main():
    print("Running War Era News Hub check...")
    state = load_state()
    
    # رسالة تأكيدية تفيد بأن النظام يعمل ويقوم بالفحص
    send_discord_embed("📡 [فحص جديد]", "جاري الاتصال بالسيرفر وجلب أحدث أخبار War Era...")

if __name__ == "__main__":
    main()
