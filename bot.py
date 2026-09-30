import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import yt_dlp

API_ID = 34584240
API_HASH = "eba4f8333cba5f9697a1d20779d4d6e9"
BOT_TOKEN = "8918686553:AAFDPyjatNETW0SpMEeaCoX9pszasbgsUqw"
CHANNEL_USERNAME = "@MX_VIDEO_DOWNLOAD"

app = Client(
    "MX_Downloader_Bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# پشکنینا کەناڵی (Force Subscribe)
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
            [InlineKeyboardButton("📢 بەشداری کرنا کەناڵی (Join)", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')} ")],
            [InlineKeyboardButton("✅ من پشکنین کر (Check)", callback_data="check_sub")]
        ])
        await message.reply_text(
            "⚠️ **سلاڤ برا!** بۆ بکارئینانا ڤی بۆتی، دڤێت پێش هەمی تشتی join کەناڵی ببی.\n\n"
            "ل خوارێ join کەناڵی ببی و پاش دووبارە `/start` بکەڤە!",
            reply_markup=keyboard
        )
        return

    await message.reply_text(
        f"👋 **سلاڤ برا! بۆتێ MX Downloader یێ ئامادەیە.**\n"
        f"🔗 لینکا TikTok یان Instagram بۆ من بنێرە دا بێ ڤارترمارک بۆ تە داگرتم!"
    )

@app.on_callback_query()
async def callback_handler(client, callback_query):
    user_id = callback_query.from_user.id
    if callback_query.data == "check_sub":
        is_joined = await check_subscription(client, user_id)
        if is_joined:
            await callback_query.message.edit_text("✅ مەزنە! تە کەناڵ پشکنا. نوکە پەیاما `/start` دووبارە بنێرە.")
        else:
            await callback_query.answer("❌ تە هێشتا join کەناڵی نەکرییە!", show_alert=True)

@app.on_message(filters.text & ~filters.command(["start"]))
async def download_media(client, message):
    user_id = message.from_user.id
    
    is_joined = await check_subscription(client, user_id)
    if not is_joined:
        await message.reply_text("⚠️ ژ بۆ بکارئینانا بۆتی، دڤێت join کەناڵی ببی! `/start`")
        return

    text = message.text.strip()
    if not text.startswith("http"):
        await message.reply_text("❌ لینکه کێ دروست یێ TikTok یان Instagram بنێرە.")
        return

    processing_msg = await message.reply_text("🔄 **بۆت مژوولی داگرتنا ڤیدیۆیێ یە...**")

    try:
        ydl_opts = {
            'format': 'best[height<=720]',
            'outtmpl': f'downloads/{user_id}_%(id)s.%(ext)s',
            'no_warnings': True,
        }
        
        os.makedirs("downloads", exist_ok=True)
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(text, download=True)
            filename = ydl.prepare_filename(info)
            
            title = info.get('title', 'بێ ناڤ')
            uploader = info.get('uploader', 'نەدیار')

            caption = f"🎬 **ڤیدیۆیا تە هاتە داگرتن (720p)**\n\n📝 **ناڤەرۆک:** {title}\n👤 **کەڤنار:** {uploader}"

            await client.send_video(chat_id=message.chat.id, video=filename, caption=caption)
            
            if os.path.exists(filename):
                os.remove(filename)
                
            await processing_msg.delete()

    except Exception as e:
        await processing_msg.edit_text(f"❌ چەوتیەک چێبوو:\n`{str(e)}`")

if __name__ == "__main__":
    print("Bot is running...")
    app.run()
