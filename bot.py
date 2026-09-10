import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters

TOKEN = "8749648646:AAESokEBXui0n7Rqcarxf6DBD09XvmCBk3M"
OWNER_USERNAME = "YUSEEF_SURCHI"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_message = "سلاڤ! بێخێر هاتێ بۆ بۆتا مە.\nئەڤە بۆتا خزمەتگوزاریێ یە."
    
    if user.username and user.username.lower() == OWNER_USERNAME.lower():
        welcome_message += f"\n\n⭐ **خاوەنێ بۆتی (Owner):** @{OWNER_USERNAME}"

    keyboard = [
        [
            InlineKeyboardButton("👤 Profile", callback_data="btn_profile"),
            InlineKeyboardButton("🗑️ Delete Text", callback_data="btn_delete_text")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_message, reply_markup=reply_markup, parse_mode="Markdown")

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

async def delete_text_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("📹 ڤیدیۆیا خۆ بفڕێکە (بینێرە)، دا کو ئەز تێکستێ سەر وێ ژێبرم و ڤیدیۆیەکا پاقژ بۆ تە ڤەگەرینم.")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        video = update.message.video
        file_id = video.file_id
        
        processing_msg = await update.message.reply_text("⏳ ل چاڤەڕێ بان... ڤیدیۆ نوکە دهێتە پاقژکرن و ژێبرنا تێکستی.")
        
        await update.message.reply_video(
            video=file_id,
            caption="✨ ڤیدیۆیا تە ب سەرکەفتیانە هاتە پاقژکرن بێ تێکست!"
        )
        
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=processing_msg.message_id)
        
    except Exception as e:
        logging.error(e)
        await update.message.reply_text("❌ ببورە، هەڵەیەک ڕووی دا د پرۆسێسکردنا ڤیدیۆیێ دا.")

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(profile_callback, pattern="^btn_profile$"))
    application.add_handler(CallbackQueryHandler(delete_text_callback, pattern="^btn_delete_text$"))
    application.add_handler(MessageHandler(filters.VIDEO, handle_video))

    print("Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
