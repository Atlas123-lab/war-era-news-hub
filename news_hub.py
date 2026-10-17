import os
import json
import urllib.request
import urllib.error

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
API_URL = "https://gateway.warerastats.io/"

def send_discord(msg):
    if not DISCORD_WEBHOOK_URL:
        return
    data = json.dumps({"content": msg}).encode("utf-8")
    req = urllib.request.Request(
        DISCORD_WEBHOOK_URL,
        data=data,
        headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    )
    try:
        urllib.request.urlopen(req)
    except Exception as e:
        print(f"Error: {e}")

def main():
    print("Testing Gateway Response...")
    req = urllib.request.Request(API_URL, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req) as response:
            raw_data = response.read().decode("utf-8")
            
            # اقتطاع أول 1000 حرف من الاستجابة لإرسالها للتأكد
            preview = raw_data[:1000] if len(raw_data) > 1000 else raw_data
            
            send_discord(f"📊 **استجابة War Era Gateway الفعلية:**\n```json\n{preview}\n```")
    except Exception as e:
        send_discord(f"❌ تعذر جلب البيانات من Gateway: {e}")

if __name__ == "__main__":
    main()
