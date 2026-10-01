import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_ID = 34584240
API_HASH = "eba4f8333cba5f9697a1d20779d4d6e9"
BOT_TOKEN = "8918686553:AAGn658Ptv0-ThnFWrLpZqh6q-dHY5Hy-y4"

# Herdû ID-yێن Owner (Admin)
ADMINS = [7904656691, 7643191802]  
CHANNEL_USERNAME = "MX_VIDEO_DOWNLOAD"
BOT_USERNAME = "MX_Download_Bot" # ناڤێ بۆتا خۆ لێرە بنڤیسە (بێ @)

app = Client("MX_Download_Bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# DB-یا سادە بۆ خاڵ و زمانان
users_data = {}

async def check_subscription(client, user_id):
    if user_id in ADMINS:
        return True
    try:
        member = await client.get_chat_member(CHANNEL_USERNAME, user_id)
        if member.status in ["creator", "administrator", "member"]:
            return True
    except Exception as e:
        print(f"Subscription check error: {e}")
        return False
    return False

# Textên ب هەمی زمانان دگەل دوگمەیێن نوو
TEXTS = {
    "badini": {
        "welcome": "✨ بەخێر هاتیت بەرێز بۆ بۆتی **MX DOWNLOAD**!\n\n📥 لينكێ ڤیدیۆیا TikTok، Instagram یان YouTube بنێرە دا بێ وێنەی ئاو (No Watermark) بۆ دابەزینم.",
        "join_req": "❌ سڵاو! بۆ کارپێکرنا بۆتی، سەرەتا پێویستە لە کەناڵی ئێمە بەشدار ببیت:",
        "btn_join": "📢 بەشداربوون لە کەناڵ 🔔",
        "btn_check": "🔄 پشکنینی بەشداربوون ⚡",
        "lang_changed": "✅ زمان بۆ (کوردی بادینی) هاتە گۆڕین!",
        "profile_text": "👤 **پڕۆفایلا تە:**\n\n🆔 ئایدی: `{}`\n⭐ خاڵێن تە: `{}`\n🌐 زمان: **Badînî**\n🔗 لینکێ بانگەوازێ: `https://t.me/{}?start={}`",
        "admin_panel": "⚙️ **پەنێلا ڕێڤەبەری (Admin Panel):**\n\nبێرە دەستهەڵاتا ڕێڤەبەران هەیە بۆ کۆنترۆلکرنا بۆتا **MX DOWNLOAD**.",
        "back_btn": "🔙 پاشڤە (Back)",
        "profile_btn": "👤 پڕۆفایل",
        "admin_btn": "⚙️ پەنێلا ئەدمین",
        "stats_btn": "📊 ئامارێن بۆتی",
        "broadcast_btn": "📢 ڤەگوهاستنا گشتی",
        "change_lang_btn": "🌐 گۆڕینا زمانێ بۆتی",
        "mx_send_btn": "📥 ناردنا لینک یان وێنەی (MX DOWNLOAD)"
    },
    "sorani": {
        "welcome": "✨ بەخێر هاتیت بۆ بۆتی **MX DOWNLOAD**!\n\n📥 لینکەی ڤیدیۆی تیکتۆک، ئینستاگرام یان یوتیوب بنێرە بۆ داگرتن بێ وێنەی ئاو.",
        "join_req": "❌ سڵاو! بۆ بەکارهێنانی بۆت، سەرەتا پێویستە لە کەناڵ بەشدار ببیت:",
        "btn_join": "📢 بەشداربوون لە کەناڵ 🔔",
        "btn_check": "🔄 پشکنینی بەشداربوون ⚡",
        "lang_changed": "✅ زمان گۆڕدرا بۆ (کوردی سۆرانی)!",
        "profile_text": "👤 **پڕۆفایلی تۆ:**\n\n🆔 ئایدی: `{}`\n⭐ خاڵەکانی تۆ: `{}`\n🌐 زمان: **Soranî**\n🔗 لینکەی بانگهێشت: `https://t.me/{}?start={}`",
        "admin_panel": "⚙️ **پەنێڵی بەڕێوەبەر (Admin Panel):**\n\nلێرە دەسەڵاتی بەڕێوەبەران هەیە بۆ کۆنتڕۆڵکردنی بۆتی **MX DOWNLOAD**.",
        "back_btn": "🔙 گەڕانەوە (Back)",
        "profile_btn": "👤 پڕۆفایل",
        "admin_btn": "⚙️ پەنێڵی ئەدمین",
        "stats_btn": "📊 ئامارەکانی بۆت",
        "broadcast_btn": "📢 پەخشکردنی گشتی",
        "change_lang_btn": "🌐 گۆڕینی زمانی بۆت",
        "mx_send_btn": "📥 ناردنی لینک یان وێنە (MX DOWNLOAD)"
    },
    "ar": {
        "welcome": "✨ أهلاً بك في بوت **MX DOWNLOAD**!\n\n📥 أرسل رابط فيديو من تيك توك، إنستغرام أو يوتيوب لتحميله بدون علامة مائية.",
        "join_req": "❌ عذراً! لاستخدام البوت، يجب عليك الاشتراك في القناة أولاً:",
        "btn_join": "📢 الاشتراك في القناة 🔔",
        "btn_check": "🔄 التحقق من الاشتراك ⚡",
        "lang_changed": "✅ تم تغيير اللغة إلى (العربية)!",
        "profile_text": "👤 **ملفك الشخصي:**\n\n🆔 الآيدي: `{}`\n⭐ نقاطك: `{}`\n🌐 اللغة: **العربية**\n🔗 رابط الدعوة: `https://t.me/{}?start={}`",
        "admin_panel": "⚙️ **لوحة التحكم (Admin Panel):**\n\nهنا صلاحيات المشرفين للتحكم ببوت **MX DOWNLOAD**.",
        "back_btn": "🔙 رجوع (Back)",
        "profile_btn": "👤 الملف الشخصي",
        "admin_btn": "⚙️ لوحة الإدارة",
        "stats_btn": "📊 إحصائيات البوت",
        "broadcast_btn": "📢 إذاعة عامة",
        "change_lang_btn": "🌐 تغيير لغة البوت",
        "mx_send_btn": "📥 إرسال رابط أو صورة (MX DOWNLOAD)"
    },
    "en": {
        "welcome": "✨ Welcome to **MX DOWNLOAD** bot!\n\n📥 Send a TikTok, Instagram or YouTube video link to download it without watermark.",
        "join_req": "❌ Hello! To use this bot, you must join our channel first:",
        "btn_join": "📢 Join Channel 🔔",
        "btn_check": "🔄 Check Subscription ⚡",
        "lang_changed": "✅ Language changed to (English)!",
        "profile_text": "👤 **Your Profile:**\n\n🆔 ID: `{}`\n⭐ Points: `{}`\n🌐 Language: **English**\n🔗 Referral Link: `https://t.me/{}?start={}`",
        "admin_panel": "⚙️ **Admin Panel:**\n\nHere are the administrator controls for **MX DOWNLOAD** bot.",
        "back_btn": "🔙 Back",
        "profile_btn": "👤 Profile",
        "admin_btn": "⚙️ Admin Panel",
        "stats_btn": "📊 Bot Stats",
        "broadcast_btn": "📢 Broadcast",
        "change_lang_btn": "🌐 Change Bot Language",
        "mx_send_btn": "📥 Send Link or Photo (MX DOWNLOAD)"
    }
}

def get_main_keyboard(user_id, lang):
    t = TEXTS[lang]
    keyboard = [
        [InlineKeyboardButton(t["mx_send_btn"], callback_data="mx_action")],
        [InlineKeyboardButton(t["profile_btn"], callback_data="profile"), InlineKeyboardButton(t["change_lang_btn"], callback_data="choose_lang")]
    ]
    if user_id in ADMINS:
        keyboard.append([InlineKeyboardButton(t["admin_btn"], callback_data="admin_panel")])
    return InlineKeyboardMarkup(keyboard)

def get_language_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Badînî 🇹🇯", callback_data="set_badini"), InlineKeyboardButton("Soranî 🇹🇯", callback_data="set_sorani")],
        [InlineKeyboardButton("العربية 🇸🇦", callback_data="set_ar"), InlineKeyboardButton("English 🇬🇧", callback_data="set_en")]
    ])

@app.on_message(filters.command("start"))
async def start_command(client, message):
    user_id = message.from_user.id
    
    # پشکنینا ریفرال (Referral) بۆ زێدەکرنا خاڵان
    args = message.command
    if len(args) > 1:
        try:
            referrer_id = int(args[1])
            if referrer_id != user_id and referrer_id in users_data:
                if user_id not in users_data.get(referrer_id, {}).get("referred", []):
                    if referrer_id not in users_data:
                        users_data[referrer_id] = {"lang": "badini", "points": 10, "referred": []}
                    if "referred" not in users_data[referrer_id]:
                        users_data[referrer_id]["referred"] = []
                    
                    users_data[referrer_id]["points"] += 5 # +5 خاڵ بۆ بانگەوازێ
                    users_data[referrer_id]["referred"].append(user_id)
        except Exception:
            pass

    if user_id not in users_data:
        users_data[user_id] = {"lang": "badini", "points": 10, "referred": []}

    lang = users_data[user_id]["lang"]
    t = TEXTS[lang]

    # پشکنینا کەناڵی پێش هەر تشتەکی
    is_joined = await check_subscription(client, user_id)
    if not is_joined:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(t["btn_join"], url=f"https://t.me/{CHANNEL_USERNAME}")],
            [InlineKeyboardButton(t["btn_check"], callback_data="check_sub")]
        ])
        await message.reply_text(f"{t['join_req']}\n👉 @{CHANNEL_USERNAME}", reply_markup=keyboard)
        return

    await message.reply_text(t["welcome"], reply_markup=get_main_keyboard(user_id, lang))

@app.on_callback_query()
async def callback_handler(client, query):
    user_id = query.from_user.id
    data = query.data

    if user_id not in users_data:
        users_data[user_id] = {"lang": "badini", "points": 10, "referred": []}

    lang = users_data[user_id]["lang"]
    t = TEXTS[lang]

    if data == "choose_lang":
        await query.message.edit_text("🌐 **زمانێ خۆ هەلبژێرە / Select Language:**", reply_markup=get_language_keyboard())

    elif data.startswith("set_"):
        new_lang = data.split("_")[1]
        users_data[user_id]["lang"] = new_lang
        new_t = TEXTS[new_lang]
        
        await query.answer(new_t["lang_changed"], show_alert=True)
        
        # پشکنینا کەناڵی ب زمانێ نوو یێ هاتە گۆڕین
        if not await check_subscription(client, user_id):
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton(new_t["btn_join"], url=f"https://t.me/{CHANNEL_USERNAME}")],
                [InlineKeyboardButton(new_t["btn_check"], callback_data="check_sub")]
            ])
            await query.message.edit_text(f"{new_t['join_req']}\n👉 @{CHANNEL_USERNAME}", reply_markup=keyboard)
            return

        await query.message.edit_text(new_t["welcome"], reply_markup=get_main_keyboard(user_id, new_lang))
        
    elif data == "check_sub":
        if await check_subscription(client, user_id):
            await query.answer("✅ سپاس بۆ بەشداربوونا تە!", show_alert=True)
            await query.message.edit_text(t["welcome"], reply_markup=get_main_keyboard(user_id, lang))
        else:
            await query.answer("❌ تو هێشتا لە کەناڵ بەشدار نەکرییە!", show_alert=True)
            
    elif data == "profile":
        points = users_data[user_id].get("points", 10)
        profile_msg = t["profile_text"].format(user_id, points, BOT_USERNAME, user_id)
        back_kb = InlineKeyboardMarkup([[InlineKeyboardButton(t["back_btn"], callback_data="back_main")]])
        await query.message.edit_text(profile_msg, reply_markup=back_kb)

    elif data == "mx_action":
        await query.answer("📥 لینک یان وێنەی خۆ بنێرە دگەل ناڤێ MX DOWNLOAD!", show_alert=True)
        
    elif data == "admin_panel":
        if user_id not in ADMINS:
            await query.answer("❌ تو دەستهەڵاتا ڤێ چەندێ نینە!", show_alert=True)
            return
        
        admin_kb = InlineKeyboardMarkup([
            [InlineKeyboardButton(t["stats_btn"], callback_data="bot_stats")],
            [InlineKeyboardButton(t["broadcast_btn"], callback_data="bot_broadcast")],
            [InlineKeyboardButton(t["back_btn"], callback_data="back_main")]
        ])
        await query.message.edit_text(t["admin_panel"], reply_markup=admin_kb)
        
    elif data == "bot_stats":
        if user_id not in ADMINS:
            return
        total_users = len(users_data)
        stats_msg = f"📊 **ئامارێن بۆتا MX DOWNLOAD:**\n\n👥 هژمارا بکارئینەران: `{total_users}`"
        back_kb = InlineKeyboardMarkup([[InlineKeyboardButton(t["back_btn"], callback_data="admin_panel")]])
        await query.message.edit_text(stats_msg, reply_markup=back_kb)
        
    elif data == "bot_broadcast":
        if user_id not in ADMINS:
            return
        await query.answer("📢 پیامەکێ بنێرە بۆ ڤەگوهاستنێ.", show_alert=True)
        
    elif data == "back_main":
        await query.message.edit_text(t["welcome"], reply_markup=get_main_keyboard(user_id, lang))

@app.on_message((filters.text | filters.photo) & ~filters.command(["start", "kick"]))
async def download_media(client, message):
    user_id = message.from_user.id
    
    if user_id not in users_data:
        users_data[user_id] = {"lang": "badini", "points": 10, "referred": []}
        
    lang = users_data[user_id]["lang"]
    t = TEXTS[lang]

    if not await check_subscription(client, user_id):
        await message.reply_text(f"{t['join_req']}\n👉 @{CHANNEL_USERNAME}")
        return
        
    if message.text and "http" in message.text:
        users_data[user_id]["points"] += 2
        sent = await message.reply_text("⏳ **MX DOWNLOAD**: Downloading video / media...")
        await sent.edit_text("✅ **MX DOWNLOAD**: Media downloaded successfully! (+2 points)")
    elif message.photo:
        users_data[user_id]["points"] += 1
        await message.reply_text("✅ **MX DOWNLOAD**: Photo received and processed successfully!")
    else:
        await message.reply_text("❌ **MX DOWNLOAD**: Please send a valid video link or photo.")

print("MX DOWNLOAD Bot is running...")
app.run()
