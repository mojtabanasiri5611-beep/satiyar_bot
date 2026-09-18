import telebot
import google.generativeai as genai

# ==========================================
# ۱. تنظیم توکن‌ها
# ==========================================
TELEGRAM_TOKEN = "8781783433:AAFPWleF3aiJqMH89orTOIfi-LXQlOo144w"
GEMINI_API_KEY = "AQ.Ab8RN6LS1IfLNIetrUlnlny8Lv1NxLhhkpPjJXmvpIp-K4mPwA"

# ==========================================
# ۲. لیست کلماتی که ربات با دیدن آن‌ها بیدار می‌شود
# ==========================================
TRIGGER_WORDS = ["ساتیار", "ربات", "هوش مصنوعی", "بات", "gemini"]

# ==========================================
# ۳. پیکربندی هوش مصنوعی و تلگرام
# ==========================================
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# گرفتن آیدی ربات برای تشخیص منشن
bot_info = bot.get_me()
bot_username = f"@{bot_info.username}".lower()

@bot.message_handler(func=lambda message: True)
def handle_group_messages(message):
    text = message.text or ""
    text_lower = text.lower()
    
    # بررسی ۱: منشن شدن آیدی ربات
    is_mentioned = bot_username in text_lower
    
    # بررسی ۲: ریپلای زدن روی پیام ربات
    is_reply_to_bot = (
        message.reply_to_message is not None and 
        message.reply_to_message.from_user.id == bot_info.id
    )
    
    # بررسی ۳: وجود کلماتی مثل ساتیار یا ربات در متن
    has_trigger_word = any(word in text_lower for word in TRIGGER_WORDS)
    
    # اگر هیچ‌کدام نبود، پیام نادیده گرفته می‌شود
    if not (is_mentioned or is_reply_to_bot or has_trigger_word):
        return

    # اگر ساتیار صدا زده شد:
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        
        # ارسال پیام به هوش مصنوعی
        response = model.generate_content(text)
        
        if response.text:
            bot.reply_to(message, response.text)
            
    except Exception as e:
        print(f"\n[خطا]: {e}\n")

print(f"ربات {bot_info.first_name} روشن شد! حالا با نوشتن 'ساتیار' در گروه بیدار می‌شود...")
bot.polling(non_stop=True)