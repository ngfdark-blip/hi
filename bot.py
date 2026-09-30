import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import yt_dlp

# زانیاریێن تە یێن ڕاستەقینە ل ڤێرە هاتنە جهگیرکرن
API_ID = 34584240
API_HASH = "eba4f8333cba5f9697a1d20779d4d6e9"
BOT_TOKEN = ""
CHANNEL_USERNAME = "@MX_VIDEO_DOWNLOAD"

app = Client("MX_Downloader_Bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# بیرگەیا دەمکی بۆ لاب و زمانێ بەکارهێنەری
user_data = {}

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
    
    # پشکنین کو ئایا ل کەناڵی بوویە ئەندام
    is_joined = await check_subscription(client, user_id)
    
    if not is_joined:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 بەشداری کرنا کەناڵی (Join)", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')} ")],
            [InlineKeyboardButton("✅ من پشکنین کر (Check)", callback_data="check_sub")]
        ])
        await message.reply_text(
            "⚠️ **سلاڤ برا!** بۆ بکارئینانا ڤی بۆتی، دڤێت پێش هەمی تشتی پێگیری کەناڵێ مە ببی.\n\n"
            "هیڤیدارم ل خوارێ join کەناڵی ببی و پاش دووبارە `/start` بکەڤە!",
            reply_markup=keyboard
        )
        return

    # دانانا لابێن دەستپێکێ ئەگەر نەبن
    if user_id not in user_data:
        user_data[user_id] = {"points": 15, "lang": "badini"}

    welcome_text = (
        f"👋 **بەرخودار بی برا!**\n"
        f"بۆتێ داگرتنا ڤیدیۆیان یێ (MX Downloader) ئامادەیە.\n"
        f"🔗 تنێ لینکەکێ ڤیدیۆیە (TikTok / Instagram) بۆ من بنێرە دا بێ ڤارترمارک و ب کوالیتیا 720p بۆ تە بینم!\n\n"
        f"🆔 ناسناما تە (ID): `{user_id}`\n"
        f"⭐ لابێن تە (Points): `{user_data[user_id]['points']}`"
    )
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🌐 گوهۆڕینا زمانی (Language)", callback_data="change_lang")],
        [InlineKeyboardButton("ℹ️ زانیاریێن من و لاب", callback_data="my_info")]
    ])
    
    await message.reply_text(welcome_text, reply_markup=keyboard)

@app.on_callback_query()
async def callback_handler(client, callback_query):
    user_id = callback_query.from_user.id
    data = callback_query.data
    
    if data == "check_sub":
        is_joined = await check_subscription(client, user_id)
        if is_joined:
            if user_id not in user_data:
                user_data[user_id] = {"points": 15, "lang": "badini"}
            await callback_query.message.edit_text("✅ مەزنە! تە کەناڵ پشکنا. نوکە پەیاما `/start` دووبارە بنێرە و دەست بە کار بی.")
        else:
            await callback_query.answer("❌ تە هێشتا join کەناڵی نەکرییە!", show_alert=True)
            
    elif data == "my_info":
        points = user_data.get(user_id, {}).get("points", 0)
        await callback_query.answer(f"🆔 ID: {user_id}\n⭐ Points: {points} لاب", show_alert=True)
        
    elif data == "change_lang":
        await callback_query.answer("🌐 زمانێ کوردی (بادینی) هاتییە هەلبژارتن.", show_alert=True)

# وەرگرتنا لینکێن ڤیدیۆیان و داگرتن بێ ڤارترمارک
@app.on_message(filters.text & ~filters.command(["start"]))
async def download_media(client, message):
    user_id = message.from_user.id
    
    # پشکنینا کەناڵی بۆ هەر پیامەکێ
    is_joined = await check_subscription(client, user_id)
    if not is_joined:
        await message.reply_text("⚠️ ژ بۆ بکارئینانا بۆتی، دڤێت پێش هەمی تشتی join کەناڵی ببی! `/start`")
        return

    text = message.text.strip()
    if not text.startswith("http"):
        await message.reply_text("❌ هیڤیدارم لینکه کێ دروست یێ TikTok یان Instagram بۆ من بنێرن.")
        return

    processing_msg = await message.reply_text("🔄 **بۆت مژوولی داگرتنا ڤیدیۆیێ یە بێ ڤارترمارک (720p)...** هیڤیدارم بێهنفرەهـ بی.")

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
            like_count = info.get('like_count', 0)
            comment_count = info.get('comment_count', 0)
            share_count = info.get('share_count', 0)
            view_count = info.get('view_count', 0)

            caption = (
                f"🎬 **ڤیدیۆیا تە هاتە داگرتن (بێ ڤارترمارک - 720p)**\n\n"
                f"📝 **ناڤەرۆک:** {title}\n"
                f"👤 **خوەدانێ ڤیدیۆیێ (Username):** {uploader}\n"
                f"❤️ **لایك (Likes):** {like_count}\n"
                f"💬 **کۆمێنت (Comments):** {comment_count}\n"
                f"↗️ **شەیر (Shares):** {share_count}\n"
                f"👁️ **بینین (Views):** {view_count}\n\n"
                f"🚀 *بۆتێ MX Downloader*"
            )

            # هنارتنا ڤیدیۆیێ ب MP4
            await client.send_video(
                chat_id=message.chat.id,
                video=filename,
                caption=caption,
                supports_streaming=True
            )
            
            # پاقژکرنا فایلێ ژ سەرڤەری دا نەهێتە خوار
            if os.path.exists(filename):
                os.remove(filename)
                
            await processing_msg.delete()

    except Exception as e:
        await processing_msg.edit_text(f"❌ چەوتیەک لەوما چێبوو نەهاتە داگرتن:\n`{str(e)}`")

if __name__ == "__main__":
    print("MX Bot is running smoothly...")
    app.run()
