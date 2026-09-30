import os
import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import yt_dlp

API_ID = 34584240
API_HASH = "eba4f8333cba5f9697a1d20779d4d6e9"
BOT_TOKEN = "8918686553:AAGn658Ptv0-ThnFWrLpZqh6q-dHY5Hy-y4"
CHANNEL_USERNAME = "@MX_VIDEO_DOWNLOAD"

OWNER_1 = "@YUSEEF_SURCHI"
OWNER_2 = "@B4llam"

app = Client(
    "MX_Downloader_Bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

user_data = {}

def generate_fake_ip(user_id):
    random.seed(user_id)
    return f"192.168.{random.randint(10, 250)}.{random.randint(2, 240)}"

async def check_subscription(client, user_id):
    try:
        member = await client.get_chat_member(CHANNEL_USERNAME, user_id)
        if member.status in ["creator", "administrator", "member"]:
            return True
    except Exception:
        pass
    return False

@app.on_message(filters.command("start"))
async def start_command(client, message):
    user_id = message.from_user.id
    
    is_joined = await check_subscription(client, user_id)
    
    if not is_joined:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 بەشداری کرنا کەناڵی | Join Channel", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')} ")],
            [InlineKeyboardButton("✅ من پشکنین کر | Check Sub", callback_data="check_sub")]
        ])
        await message.reply_text(
            "⚠️ **سلاڤ برا! پێدڤییە سەرەتا join کەناڵی ببی.**\n"
            "⚠️ **Hello! You must join our channel first.**\n\n"
            "👇 **ل خوارێ کلیک ل سەر join بکە و پاشان `/start` بنێرەەوە!**",
            reply_markup=keyboard
        )
        return

    if user_id not in user_data:
        user_data[user_id] = {
            "points": 25, 
            "lang": "badini",
            "name": message.from_user.first_name or "بەکارهێنەر",
            "username": f"@{message.from_user.username}" if message.from_user.username else "نەدیار",
            "ip": generate_fake_ip(user_id)
        }

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🟢 کوردی بادینی", callback_data="lang_badini"),
            InlineKeyboardButton("🔵 کوردی سۆرانی", callback_data="lang_sorani")
        ],
        [
            InlineKeyboardButton("🟡 English", callback_data="lang_english"),
            InlineKeyboardButton("🟠 العربية", callback_data="lang_arabic")
        ],
        [
            InlineKeyboardButton("👤 پروفایلا من | My Profile", callback_data="my_profile")
        ]
    ])
    
    welcome_msg = (
        f"✨ **بخێر هاتن بۆ بۆتێ MX Downloader!** ✨\n"
        f"👑 **خوەدان (Owners):** {OWNER_1} & {OWNER_2}\n\n"
        f"🌐 **هیڤیدارم زمانێ خۆ هەلبژێرە یان تەماشەی پروفایلا خۆ بکە:**"
    )
    
    await message.reply_text(welcome_msg, reply_markup=keyboard)

@app.on_callback_query()
async def callback_handler(client, callback_query):
    user_id = callback_query.from_user.id
    data = callback_query.data
    
    if user_id not in user_data:
        user_data[user_id] = {
            "points": 25, 
            "lang": "badini",
            "name": callback_query.from_user.first_name or "بەکارهێنەر",
            "username": f"@{callback_query.from_user.username}" if callback_query.from_user.username else "نەدیار",
            "ip": generate_fake_ip(user_id)
        }

    if data == "check_sub":
        is_joined = await check_subscription(client, user_id)
        if is_joined:
            await callback_query.message.edit_text("✅ **پیرۆزە! کەناڵ هاتە پشکنتن. نوکە پەیاما `/start` دووبارە بنێرە.**")
        else:
            await callback_query.answer("❌ تە هێشتا join کەناڵی نەکرییە برا!", show_alert=True)
            
    elif data == "my_profile":
        u_info = user_data[user_id]
        profile_text = (
            f"👤 **پروفایلا تە / Your Profile**\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"📛 **ناڤ (Name/Nickname):** `{u_info['name']}`\n"
            f"🔗 **يوزەرێرن (Username):** `{u_info['username']}`\n"
            f"🆔 **ناساناما تە (ID):** `{user_id}`\n"
            f"🌐 **ناڤنیشانێ IP:** `{u_info['ip']}`\n"
            f"💎 **لابێن تە (Points):** `{u_info['points']} لاب`\n"
            f"🗣️ **زمانێ هەلبژارتی (Language):** `{u_info['lang'].upper()}`\n"
            f"👑 **Owners:** {OWNER_1} | {OWNER_2}\n"
            f"━━━━━━━━━━━━━━━━━━━"
        )
        back_kb = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 ڤەگەر | Back", callback_data="back_home")]])
        await callback_query.message.edit_text(profile_text, reply_markup=back_kb)
        
    elif data == "back_home":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🟢 کوردی بادینی", callback_data="lang_badini"), InlineKeyboardButton("🔵 کوردی سۆرانی", callback_data="lang_sorani")],
            [InlineKeyboardButton("🟡 English", callback_data="lang_english"), InlineKeyboardButton("🟠 العربية", callback_data="lang_arabic")],
            [InlineKeyboardButton("👤 پروفایلا من | My Profile", callback_data="my_profile")]
        ])
        await callback_query.message.edit_text("✨ **سەرەتاک بۆتێ MX Downloader:**\n🌐 زمانێ خۆ هەلبژێرە:", reply_markup=keyboard)
        
    elif data.startswith("lang_"):
        lang = data.split("_")[1]
        user_data[user_id]["lang"] = lang
        
        texts = {
            "badini": f"✅ **زمانێ کوردی (بادینی) هاتە هەلبژارتن!**\n\n🔗 نوکە لینکا **TikTok، Instagram یا YouTube** بۆ من بنێرە!\n👑 Owners: {OWNER_1} | {OWNER_2}",
            "sorani": f"✅ **زمان کوردی (سۆرانی) هەڵبژێردرا!**\n\n🔗 ئێستا لینکەی **TikTok، Instagram یان YouTube** بۆ من بنێرە!\n👑 Owners: {OWNER_1} | {OWNER_2}",
            "english": f"✅ **English language selected!**\n\n🔗 Now send any link from **TikTok، Instagram or YouTube**!\n👑 Owners: {OWNER_1} | {OWNER_2}",
            "arabic": f"✅ **تم اختيار اللغة العربية!**\n\n🔗 الآن أرسل أي رابط من **TikTok، Instagram أو YouTube**!\n👑 Owners: {OWNER_1} | {OWNER_2}"
        }
        back_kb = InlineKeyboardMarkup([[InlineKeyboardButton("👤 پروفایلا من | Profile", callback_data="my_profile")]])
        await callback_query.message.edit_text(texts.get(lang, texts["badini"]), reply_markup=back_kb)

@app.on_message(filters.text & ~filters.command(["start"]))
async def download_media(client, message):
    user_id = message.from_user.id
    
    is_joined = await check_subscription(client, user_id)
    if not is_joined:
        await message.reply_text("⚠️ **پێدڤییە join کەناڵی ببی! `/start`**")
        return

    text = message.text.strip()
    if user_id not in user_data:
        user_data[user_id] = {
            "points": 25, 
            "lang": "badini",
            "name": message.from_user.first_name or "بەکارهێنەر",
            "username": f"@{message.from_user.username}" if message.from_user.username else "نەدیار",
            "ip": generate_fake_ip(user_id)
        }

    if not text.startswith("http"):
        await message.reply_text("❌ **هیڤیدارم لینکه کێ دروست یێ TikTok، Instagram یان YouTube بنێرە.**")
        return

    if user_data[user_id]["points"] < 2:
        await message.reply_text("❌ **لابێن تە یێن مان نەبوون! (Points کمە)**")
        return

    processing_msg = await message.reply_text("🔄 **بۆت مژوولی داگرتنا ناڤەرۆکێ یە بێ ڤارترمارک...** 🎬")

    try:
        os.makedirs("downloads", exist_ok=True)
        
        ydl_opts_audio = {
            'format': 'bestaudio/best',
            'outtmpl': f'downloads/{user_id}_%(id)s.%(ext)s',
            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
            'no_warnings': True,
        }

        ydl_opts_video = {
            'format': 'best[height<=720]/best',
            'outtmpl': f'downloads/{user_id}_%(id)s.%(ext)s',
            'no_warnings': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts_video) as ydl:
            info = ydl.extract_info(text, download=True)
            filename = ydl.prepare_filename(info)
            title = info.get('title', 'MX Media')
            uploader = info.get('uploader', 'Unknown')
            
            if os.path.exists(filename):
                caption = (
                    f"✨ **MX Downloader - Media** ✨\n"
                    f"📝 **Title:** {title}\n"
                    f"👤 **Uploader:** {uploader}\n"
                    f"👑 **Owners:** {OWNER_1} | {OWNER_2}\n"
                    f"💎 **Remaining Points:** `{user_data[user_id]['points'] - 1}`"
                )
                
                if filename.endswith(('.jpg', '.jpeg', '.png', '.webp')):
                    await client.send_photo(chat_id=message.chat.id, photo=filename, caption=caption)
                else:
                    await client.send_video(chat_id=message.chat.id, video=filename, caption=caption, supports_streaming=True)
                
                if os.path.exists(filename):
                    os.remove(filename)

        with yt_dlp.YoutubeDL(ydl_opts_audio) as ydl_audio:
            info_audio = ydl_audio.extract_info(text, download=True)
            base_filename = ydl_audio.prepare_filename(info_audio)
            mp3_filename = os.path.splitext(base_filename)[0] + ".mp3"
            
            if os.path.exists(mp3_filename):
                await client.send_audio(
                    chat_id=message.chat.id, 
                    audio=mp3_filename, 
                    caption=f"🎵 **Audio (MP3) - MX Bot**\n👑 Owners: {OWNER_1} | {OWNER_2}"
                )
                if os.path.exists(mp3_filename):
                    os.remove(mp3_filename)

        user_data[user_id]["points"] -= 1
        await processing_msg.delete()

    except Exception as e:
        await processing_msg.edit_text(f"❌ **Error / چەوتی:**\n`{str(e)}`")

if __name__ == "__main__":
    app.run()

