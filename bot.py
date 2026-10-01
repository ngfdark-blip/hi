import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_ID = 34584240
API_HASH = "eba4f8333cba5f9697a1d20779d4d6e9"
BOT_TOKEN = os.getenv("BOT_TOKEN", "Lera_Tokna_Boti_Xo_Bnvisa")
ADMINS = [int(admin_id) for admin_id in os.getenv("ADMINS", "123456789,987654321").split(",")]
CHANNEL_USERNAME = "MX_VIDEO_DOWNLOAD"

app = Client("MX_Download_Bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def check_subscription(client, user_id):
    try:
        member = await client.get_chat_member(CHANNEL_USERNAME, user_id)
        if member.status in ["creator", "administrator", "member"]:
            return True
    except Exception:
        return False
    return False

# Transltions fɔ 4 langwej (Badini, Sorani, Arabic, English)
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
    is_joined = await check_subscription(client, user_id)
    
    lang = user_languages.get(user_id, "badini")
    t = TEXTS[lang]

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

    if data.startswith("set_"):
        lang = data.split("_")[1]
        user_languages[user_id] = lang
        t = TEXTS[lang]
        await query.answer(t["lang_changed"], show_alert=True)
        await query.message.edit_text(t["welcome"], reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Badînî 🇹🇯", callback_data="set_badini"), InlineKeyboardButton("Soranî 🇹🇯", callback_data="set_sorani")],
            [InlineKeyboardButton("العربية 🇸🇦", callback_data="set_ar"), InlineKeyboardButton("English 🇬🇧", callback_data="set_en")],
            [InlineKeyboardButton("👤 Profile", callback_data="profile")]
        ]))
    elif data == "check_sub":
        if await check_subscription(client, user_id):
            await query.answer("✅ Thank you for joining!", show_alert=True)
            await start_command(client, query.message)
        else:
            await query.answer("❌ You have not joined the channel yet!", show_alert=True)
    elif data == "profile":
        await query.answer(f"ID: {user_id}\nName: {query.from_user.first_name}", show_alert=True)

# Link grabber fɔ dowload video no watermark (TikTok, Instagram, YouTube)
@app.on_message(filters.text & ~filters.command(["start", "kick"]))
async def download_media(client, message):
    text = message.text
    if "http" in text:
        sent = await message.reply_text("⏳ Dowloading video no watermark...")
        # Leta yu put a bit-dl api yɛ fɔ yanki watermaki
        # Fɔ naw dis dɔmji simplet fɔ test
        await sent.edit_text("✅ Video dɔm downlod wit no watermark! (Pls add downloader API like yt-dlp here)")
    else:
        await message.reply_text("❌ Pls send a valid video link (TikTok, Instagram, YouTube).")

@app.on_message(filters.command("kick") & filters.user(ADMINS))
async def kick_user(client, message):
    if not message.reply_to_message:
        await message.reply_text("⚠️ Reply to user message to kick.")
        return
    target_id = message.reply_to_message.from_user.id
    try:
        await client.ban_chat_member(message.chat.id, target_id)
        await message.reply_text("✅ User kicked successfully!")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

print("Bot is running...")
app.run()
