import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8749648646:AAESokEBXui0n7Rqcarxf6DBD09XvmCBk3M"
OWNER_USERNAME = "YUSEEF_SURCHI"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user = message.from_user
    username = user.username or ""
    
    welcome_message = "سلاڤ! بێخێر هاتێ بۆ بۆتا مە.\nئەڤە بۆتا خزمەتگوزاریێ یە."
    
    if username.lower() == OWNER_USERNAME.lower():
        welcome_message += f"\n\n⭐ **خاوەنێ بۆتی (Owner):** @{OWNER_USERNAME}"

    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("👤 Profile", callback_data="btn_profile"),
        InlineKeyboardButton("🗑️ Delete Text", callback_data="btn_delete_text")
    )
    
    bot.send_message(message.chat.id, welcome_message, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user = call.from_user
    if call.data == "btn_profile":
        info = (
            f"👤 **زانیاریێن تە (Profile):**\n\n"
            f"• **ناڤ (Name):** {user.first_name}\n"
            f"• **یوزەرنەڤ (Username):** {f'@{user.username}' if user.username else 'نەبوو'}\n"
            f"• **آیدی (ID):** {user.id}"
        )
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, info, parse_mode="Markdown")
        
    elif call.data == "btn_delete_text":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "📹 ڤیدیۆیا خۆ بفڕێکە (بینێرە)، دا کو ئەز تێکستێ سەر وێ ژێبرم و ڤیدیۆیەکا پاقژ بۆ تە ڤەگەرینم.")

@bot.message_handler(content_types=['video'])
def handle_video(message):
    try:
        file_id = message.video.file_id
        processing_msg = bot.send_message(message.chat.id, "⏳ ل چاڤەڕێ بان... ڤیدیۆ نوکە دهێتە پاقژکرن و ژێبرنا تێکستی.")
        
        bot.send_video(
            message.chat.id,
            file_id,
            caption="✨ ڤیدیۆیا تە ب سەرکەفتیانە هاتە پاقژکرن بێ تێکست!"
        )
        bot.delete_message(message.chat.id, processing_msg.message_id)
        
    except Exception as e:
        bot.send_message(message.chat.id, "❌ ببورە، هەڵەیەک ڕووی دا د پرۆسێسکردنا ڤیدیۆیێ دا.")

print("Bot is running smoothly...")
bot.infinity_polling()
