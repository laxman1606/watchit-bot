import telebot
import urllib.parse
import os
import threading
from flask import Flask

# 🚀 APNA ASLI BOT TOKEN YAHAN DAALNA
API_TOKEN = '8516164180:AAFTn62ylXWc0PytqpQP5AfD4RghbbCFpcM'
bot = telebot.TeleBot(API_TOKEN)

# Render server
app = Flask(__name__)

@app.route('/')
def home():
    return "WATCHit Bot is Online and Running 24/7! 🚀"

# ----------------- TELEGRAM BOT LOGIC -----------------
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to WATCHit Bot! 🍿\nMujhe koi bhi direct video link bhejo, main usko WATCHit App me play karne wala link bana dunga.")

@bot.message_handler(func=lambda message: True)
def handle_link(message):
    original_url = message.text.strip()
    
    # URL ko safe banaya
    safe_url = urllib.parse.quote(original_url, safe='')
    
    # 🚀 JADOO YAHAN HAI: HTML code se ugly link ko chhupa diya aur mast button bana diya
    response_msg = f"""🎬 <b>Ready to Play!</b> 🎬

Tap the link below to watch this video directly in your app:

👉 <a href="watchitapp://play?url={safe_url}"><b>▶️ PLAY IN WATCHit APP</b></a> 👈

<i>(Note: Agar app installed nahi hai, toh link kaam nahi karega)</i>"""

    # parse_mode="HTML" use kiya hai taaki design kaam kare
    bot.reply_to(message, response_msg, parse_mode="HTML")

# ----------------- START SERVER & BOT -----------------
def run_bot():
    print("Telegram Bot is running...")
    bot.polling(non_stop=True)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
