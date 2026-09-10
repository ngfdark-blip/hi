import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8749648646:AAESokEBXui0n7Rqcarxf6DBD09XvmCBk3M"
OWNER_USERNAME = "YUSEEF_SURCHI"

bot = telebot.TeleBot(TOKEN)

# گلەوکرنا دەمکی یا تێکستێن ڤیدیۆیان بۆ هەر بکارهێنەری
video_texts_cache = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user = message.from_user
    username = user.username or ""
    
    welcome_message = "سلاڤ! بێخێر هاتێ بۆ بۆتا مە.\nئەڤە بۆتا پاکژکرنا ڤیدیۆیانە."
    
    if username.lower() == OWNER_USERNAME.lower():
        welcome_message += f"\n\nخاوەنێ بۆتی (Owner): @{OWNER_USERNAME}"

    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("Profile", callback_data="btn_profile"),
        InlineKeyboardButton("Delete Text", callback_data="btn_delete_text")
    )
    
    bot.send_message(message.chat.id, welcome_message, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("del_txt_"))
def delete_specific_text(call):
    bot.answer_callback_query(call.id)
    parts = call.data.split("_")
    msg_id = int(parts[2])
    index = int(parts[3])
    
    if msg_id in video_texts_cache and index < len(video_texts_cache[msg_id]['texts']):
        # ژێبرنا تێکستێ هاتیە دیارکرن
        video_texts_cache[msg_id]['texts'][index] = None
        
        # نووکرنا لابان بێ وێ تێکستێ
        texts = video_texts_cache[msg_id]['texts']
        file_id = video_texts_cache[msg_id]['file_id']
        
        markup = InlineKeyboardMarkup()
        has_active = False
        for i, t in enumerate(texts):
            if t is not None:
                has_active = True
                short_t = (t[:15] + '...') if len(t) > 15 else t
                markup.add(InlineKeyboardButton(f"🗑️ لادان: {short_t}", callback_data=f"del_txt_{msg_id}_{i}"))
        
        if has_active:
            markup.add(InlineKeyboardButton("✨ ڤێرژنا بێ تێکست یا تەمام", callback_data=f"send_clean_{msg_id}"))
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)
        else:
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_video(call.message.chat.id, file_id, caption="✨ ڤیدیۆیا تە ب تەواوی بێ تێکست هاتە ڤەگەراندن!")

@bot.callback_query_handler(func=lambda call: call.data.startswith("send_clean_"))
def send_fully_clean_video(call):
    bot.answer_callback_query(call.id)
    msg_id = int(call.data.split("_")[2])
    if msg_id in video_texts_cache:
        file_id = video_texts_cache[msg_id]['file_id']
        bot.send_video(call.message.chat.id, file_id, caption="✨ ڤیدیۆیا تە ب سەرکەفتیانە بێ تێکست هاتە هنارتن!")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user = call.from_user
    if call.data == "btn_profile":
        info = (
            f"زانیاریێن تە (Profile):\n\n"
            f"• ناڤ: {user.first_name}\n"
            f"• یوزەرنەڤ: {f'@{user.username}' if user.username else 'نەبوو'}\n"
            f"• آیدی: {user.id}"
        )
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, info)
        
    elif call.data == "btn_delete_text":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "📹 ڤیدیۆیا خۆ بفڕێکە (بینێرە)، دا کو ئەز تێکستێ سەر وێ ب دابەشکرنا لەبان بۆ تە پاکژ بکەم.")

@bot.message_handler(content_types=['video'])
def handle_video(message):
    try:
        file_id = message.video.file_id
        caption = message.caption or ""
        
        if not caption:
            bot.send_video(message.chat.id, file_id, caption="✨ ئەڤ ڤیدیۆیە ب خۆ بێ تێکست بوو!")
            return

        # دابەشکرنا تێکستی بۆ پارچەیێن جودا (ل سەر بنەمایێ هێلا نوو یان بۆشاییان)
        split_texts = [t.strip() for t in caption.split("\n") if t.strip()]
        if not split_texts:
            split_texts = [caption]

        msg = bot.send_video(message.chat.id, file_id, caption=f"📝 تێکستێن سەر ڤیدیۆیێ دابەش بوون. کیشکێ دخوازی لادەی؟")
        
        video_texts_cache[msg.message_id] = {
            'file_id': file_id,
            'texts': split_texts
        }

        markup = InlineKeyboardMarkup()
        for i, t in enumerate(split_texts):
            short_t = (t[:15] + '...') if len(t) > 15 else t
            markup.add(InlineKeyboardButton(f"🗑️ لادان: {short_t}", callback_data=f"del_txt_{msg.message_id}_{i}"))
        
        markup.add(InlineKeyboardButton("✨ ڤێرژنا بێ تێکست یا تەمام", callback_data=f"send_clean_{msg.message_id}"))
        bot.edit_message_reply_markup(message.chat.id, msg.message_id, reply_markup=markup)
        
    except Exception as e:
        bot.send_message(message.chat.id, "❌ ببورە، هەڵەیەک ڕووی دا.")

@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    # ئەگەر تشتەکێ هەڵە (نە ڤیدیۆ) هنارت
    bot.send_message(message.chat.id, "❌ شاشیە! ڤیدیۆیا خۆ فڕێکە، ئەڤە نە ڤیدیۆیە.")

print("Bot is running smoothly...")
bot.infinity_polling()
