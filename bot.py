import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# زانیاریێن بۆتی و ئەپی
TOKEN = "8749648646:AAHQTiavunhsvndF1p45yR3tkYv339CkGYE"
API_ID = 34584240
API_HASH = "eba4f8333cba5f9697a1d20779d4d6e9"

# خوەدیێ بۆتی (Owner)
OWNER_USERNAME = "YUSEEF_SURCHI"

# رێڤەبرنا لاگۆگان
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ١. دەستپێکرنا بۆتی (Start)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = f"@{user.username}" if user.username else "نەدیار"
    
    welcome_message = f"سلاڤ! بێخێر هاتێ بۆ بۆتا مە.\nئەڤە بۆتا خزمەتگوزاریێ یە."
    
    # پشکنینا خاوەنی
    if user.username and user.username.lower() == OWNER_USERNAME.lower():
        welcome_message += f"\n\n⭐ **خاوەنێ بۆتی (Owner):** @{OWNER_USERNAME}"

    # دوو لاب (Profile و Delete Text)
    keyboard = [
        [
            InlineKeyboardButton("👤 Profile", callback_data="btn_profile"),
            InlineKeyboardButton("🗑️ Delete Text", callback_data="btn_delete_text")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_message, reply_markup=reply_markup, parse_mode="Markdown")

# ٢. لابا پرۆفایلی (Profile)
async def profile_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user
    
    info = (
        f"👤 **زانیاریێن تە (Profile):**\n\n"
        f"• **ناڤ (Name):** {user.first_name}\n"
        f"• **یوزەرنەڤ (Username):** {f'@{user.username}' if user.username else 'نەبوو'}\n"
        f"• **آیدی (ID):** {user.id}"
    )
    await query.message.reply_text(info, parse_mode="Markdown")

# ٣. لابا ژێبرنا تێکستێ سەر ڤیدیۆیێ (Delete Text)
async def delete_text_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("📹 ڤیدیۆیا خۆ بفڕێکە (بینێرە)، دا کو ئەز تێکستێ سەر وێ ژێبرم و ڤیدیۆیەکا پاقژ بۆ تە ڤەگەرینم.")

# ٤. وەرگرتنا ڤیدیۆیان و لادانا تێکستێ سەر وێ (Caption)
async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        video = update.message.video
        file_id = video.file_id
        
        processing_msg = await update.message.reply_text("⏳ ل چاڤەڕێ بان... ڤیدیۆ نوکە دهێتە پاقژکرن و ژێبرنا تێکستی.")
        
        # ڤیدیۆ بێ کێپشن (Caption) دهێتە هنارتن (تێکست ژێ دبرێتەڤە، دەنگ و ستران وەکی خۆ دمینن)
        await update.message.reply_video(
            video=file_id,
            caption="✨ ڤیدیۆیا تە ب سەرکەفتیانە هاتە پاقژکرن بێ تێکست!"
        )
        
        # ژێبرنا پەیاما چاڤەڕێبوونێ
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=processing_msg.message_id)
        
    except Exception as e:
        logging.error(e)
        await update.message.reply_text("❌ ببورە، هەڵەیەک ڕووی دا د پرۆسێسکردنا ڤیدیۆیێ دا.")

def main():
    # دروستکرنا ئەپا بۆتی
    application = ApplicationBuilder().token(TOKEN).build()

    # گرێدانا فەرمان و پلاکێن بۆتی
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(profile_callback, pattern="^btn_profile$"))
    application.add_handler(CallbackQueryHandler(delete_text_callback, pattern="^btn_delete_text$"))
    application.add_handler(MessageHandler(filters.VIDEO, handle_video))

    # دەستپێکرنا بۆتی
    print("Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
