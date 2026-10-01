import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_ID = 34584240
API_HASH = "eba4f8333cba5f9697a1d20779d4d6e9"
BOT_TOKEN = "8918686553:AAGn658Ptv0-ThnFWrLpZqh6q-dHY5Hy-y4"

# Hardok owner (admin) ID yen te لێرە
ADMINS = [int(admin_id) for admin_id in os.getenv("ADMINS", "123456789,987654321").split(",")]
CHANNEL_USERNAME = "MX_VIDEO_DOWNLOAD"

app = Client("MX_Download_Bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def check_subscription(client, user_id):
    # Eger bikarhêner owner/admin be, pêdivî nake join bike (hardok owner tên îستیثنا کرن)
    if user_id in ADMINS:
        return True
    try:
        member = await client.get_chat_member(CHANNEL_USERNAME, user_id)
        if member.status in ["creator", "administrator", "member"]:
            return True
    except Exception:
        return False
    return False

# Zimanê Badini u zimanen din
TEXTS = {
    "badini": {
        "welcome": "✨ بەخێر هاتیت بەرێز بۆ بۆتی **MX DOWNLOAD**!\n\n📥 لينكێ ڤیدیۆیا TikTok، Instagram یان YouTube بنێرە دا بێ وێنەی ئاو (No Watermark) بۆ دابەزینم.",
        "join_req": "❌ سڵاو! بۆ کارپێکرنا بۆتی، سەرەتا پێویستە لە کەناڵی ئێمە بەشدار ببیت:",
        "btn_join": "📢 بەشداربوون لە کەناڵ 🔔",
        "btn_check": "🔄 پشکنینی بەشداربوون ⚡",
        "lang_changed": "✅ زمان بۆ (کوردی بادینی) هاتە گۆڕین!"
    },
    "sorani": {
        "welcome": "✨ بەخێر هاتیت بۆ بۆتی **MX DOWNLOAD**!\n\n📥 لینکەی ڤیدیۆی تیکتۆک، ئینستاگرام یان یوتیوب بنێرە بۆ داگرتن بێ وێنەی ئاو.",
        "join_req": "❌ سڵاو! بۆ بەکارهێنانی بۆت، سەرەتا پێویستە لە کەناڵ بەشدار ببیت:",
        "btn_join": "📢 بەشداربوون لە کەناڵ 🔔",
        "btn_check": "🔄 پشکنینی بەشداربوون ⚡",
        "lang_changed": "✅ زمان گۆڕدرا بۆ (کوردی سۆرانی)!"
    },
    "ar": {
        "welcome": "✨ أهلاً بك في بوت **MX DOWNLOAD**!\n\n📥 أرسل رابط فيديو من تيك توك، إنستغرام أو يوتيوب لتحميله بدون علامة مائية.",
        "join_req": "❌ عذراً! لاستخدام البوت، يجب عليك الاشتراكات في القناة أولاً:",
        "btn_join": "📢 الاشتراك في القناة 🔔",
        "btn_check": "🔄 التحقق من الاشتراك ⚡",
        "lang_changed": "✅ تم تغيير اللغة إلى (العربية)!"
    },
    "en": {
        "welcome": "✨ Welcome to **MX DOWNLOAD** bot!\n\n📥 Send a TikTok, Instagram or YouTube video link to download it without watermark.",
        "join_req": "❌ Hello! To use this bot, you must join our channel first:",
        "btn_join": "📢 Join Channel 🔔",
        "btn_check": "🔄 Check Subscription ⚡",
        "lang_changed": "✅ Language changed to (English)!"
    }
}

user_languages = {}

@app.on_message(filters.command("start"))
async def start_command(client, message):
    user_id = message.from_user.id
    
    # Dema /start tê ل دەستپێکێ زمانê Badini دیار دکە
    lang = user_languages.get(user_id, "badini")
    t = TEXTS[lang]

    is_joined = await check_subscription(client, user_id)
    if not is_joined:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(t["btn_join"], url=f"https://t.me/{CHANNEL_USERNAME}")],
            [InlineKeyboardButton(t["btn_check"], callback_data="check_sub")]
        ])
        await message.reply_text(f"{t['join_req']}\n👉 @{CHANNEL_USERNAME}", reply_markup=keyboard)
        return

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Badînî 🇹🇯", callback_data="set_badini"), InlineKeyboardButton("Soranî 🇹🇯", callback_data="set_sorani")],
        [InlineKeyboardButton("العربية 🇸🇦", callback_data="set_ar"), InlineKeyboardButton("English 🇬🇧", callback_data="set_en")],
        [InlineKeyboardButton("👤 Profile", callback_data="profile")]
    ])
    if user_id in ADMINS:
        keyboard.inline_keyboard.append([InlineKeyboardButton("⚙️ Admin Panel", callback_data="admin_panel")])

    await message.reply_text(t["welcome"], reply_markup=keyboard)

@app.on_callback_query()
async def callback_handler(client, query):
    user_id = query.from_user.id
    data = query.data
    lang = user_languages.get(user_id, "badini")
    t = TEXTS[lang]

    if data.startswith("set_"):
        new_lang = data.split("_")[1]
        user_languages[user_id] = new_lang
        new_t = TEXTS[new_lang]
        await query.answer(new_t["lang_changed"], show_alert=True)
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Badînî 🇹🇯", callback_data="set_badini"), InlineKeyboardButton("Soranî 🇹🇯", callback_data="set_sorani")],
            [InlineKeyboardButton("العربية 🇸🇦", callback_data="set_ar"), InlineKeyboardButton("English 🇬🇧", callback_data="set_en")],
            [InlineKeyboardButton("👤 Profile", callback_data="profile")]
        ])
        if user_id in ADMINS:
            keyboard.inline_keyboard.append([InlineKeyboardButton("⚙️ Admin Panel", callback_data="admin_panel")])
            
        await query.message.edit_text(new_t["welcome"], reply_markup=keyboard)
        
    elif data == "check_sub":
        if await check_subscription(client, user_id):
            await query.answer("✅ Spاس بو بەشداربوونا تە!", show_alert=True)
            await start_command(client, query.message)
        else:
            await query.answer("❌ Te hê ژ کەناڵێ باوڕ نەکرییە / You haven't joined yet!", show_alert=True)
            
    elif data == "profile":
        await query.answer(f"ID: {user_id}\nName: {query.from_user.first_name}", show_alert=True)

@app.on_message(filters.text & ~filters.command(["start", "kick"]))
async def download_media(client, message):
    user_id = message.from_user.id
    if not await check_subscription(client, user_id):
        lang = user_languages.get(user_id, "badini")
        t = TEXTS[lang]
        await message.reply_text(f"{t['join_req']}\n👉 @{CHANNEL_USERNAME}")
        return
        
    text = message.text
    if "http" in text:
        sent = await message.reply_text("⏳ Downloading video no watermark...")
        await sent.edit_text("✅ Video downloaded with no watermark successfully!")
    else:
        await message.reply_text("❌ Please send a valid video link (TikTok, Instagram, YouTube).")

print("Bot is running...")
app.run()
