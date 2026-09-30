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
        f"🔗 لینکا **TikTok، Instagram یاخود YouTube** بۆ من بنێرە دا:\n"
        f"• ڤیدیۆ بێ ڤارترمارک (720p)\n"
        f"• وێنە / پۆست\n"
        f"• دەنگ (MP3)\n"
        f"بۆ تە داگرتم!"
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
        await message.reply_text("❌ لینکه کێ دروست یێ TikTok، Instagram یان YouTube بنێرە.")
        return

    processing_msg = await message.reply_text("🔄 **بۆت مژوولی داگرتنا ناڤەرۆکێ یە (ڤیدیۆ، وێنە یان MP3)...**")

    try:
        os.makedirs("downloads", exist_ok=True)
        
        # 1. داگرتنا MP3
        ydl_opts_audio = {
            'format': 'bestaudio/best',
            'outtmpl': f'downloads/{user_id}_%(id)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'no_warnings': True,
        }

        # 2. داگرتنا ڤیدیۆیێ (ب کوالیتیا 720p)
        ydl_opts_video = {
            'format': 'best[height<=720]/best',
            'outtmpl': f'downloads/{user_id}_%(id)s.%(ext)s',
            'no_warnings': True,
        }

        # پشکنین و داگرتن ب ڕێکا yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts_video) as ydl:
            info = ydl.extract_info(text, download=True)
            filename = ydl.prepare_filename(info)
            title = info.get('title', 'MX Downloader Media')
            uploader = info.get('uploader', 'نەدیار')
            
            # ئەگەر فایلا ڤیدیۆیێ بوو (یان وێنە بوو)
            if os.path.exists(filename):
                caption = f"🎬 **ناڤەرۆکا هاتە داگرتن**\n\n📝 **ناڤ:** {title}\n👤 **کەڤنار:** {uploader}\n🚀 *@MX_VIDEO_DOWNLOAD*"
                
                # ئەگەر وێنە بیت
                if filename.endswith(('.jpg', '.jpeg', '.png', '.webp')):
                    await client.send_photo(chat_id=message.chat.id, photo=filename, caption=caption)
                else:
                    await client.send_video(chat_id=message.chat.id, video=filename, caption=caption, supports_streaming=True)
                
                if os.path.exists(filename):
                    os.remove(filename)

        # داگرتن و هنارتنا دەنگی (MP3) ژی ب هەڤڕا
        with yt_dlp.YoutubeDL(ydl_opts_audio) as ydl_audio:
            info_audio = ydl_audio.extract_info(text, download=True)
            base_filename = ydl_audio.prepare_filename(info_audio)
            mp3_filename = os.path.splitext(base_filename)[0] + ".mp3"
            
            if os.path.exists(mp3_filename):
                await client.send_audio(
                    chat_id=message.chat.id, 
                    audio=mp3_filename, 
                    caption=f"🎵 **دەنگێ MP3**\n🚀 *@MX_VIDEO_DOWNLOAD*"
                )
                if os.path.exists(mp3_filename):
                    os.remove(mp3_filename)

        await processing_msg.delete()

    except Exception as e:
        await processing_msg.edit_text(f"❌ چەوتیەک لەوما چێبوو:\n`{str(e)}`")

if __name__ == "__main__":
    app.run()
