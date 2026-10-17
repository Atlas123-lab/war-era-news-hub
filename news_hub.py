def main():
    print("Checking for new War Era events...")
    state = load_state()
    seen_ids = set(state.get("seen_ids", []))
    
    events = fetch_events()
    
    # إلى لقيتِ أحداث فـ Gateway ولكن كلها مسجلة فـ state.json، صيفط تنبيه تأكيدي
    if not events:
        send_discord_embed("📡 [فحص Gateway]", "تم الاتصال بالواجهة ولكن لا توجد أحداث حصرية حالياً.")
    else:
        send_discord_embed("📡 [تم جلب البيانات]", f"تم العثور على {len(events)} حدثاً في سيرفر اللعبة!")
