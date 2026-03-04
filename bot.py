import telebot
import urllib.parse
import os
import threading
from flask import Flask

# APNA BOT TOKEN YAHAN DAALEIN
API_TOKEN = '8516164180:AAFTn62ylXWc0PytqpQP5AfD4RghbbCFpcM'
bot = telebot.TeleBot(API_TOKEN)

# Render ko khush rakhne ke liye ek chota sa Web Server
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
    original_url = message.text
    safe_url = urllib.parse.quote(original_url, safe='')
    watchit_deep_link = f"https://watchit.com/play?url={safe_url}"
    
    response_msg = (
        "🎬 **Ready to Play!** 🎬\n\n"
        "Click the link below to watch this video in Ultra HD on WATCHit Player:\n\n"
        f"👉 {watchit_deep_link}\n\n"
        "_(Note: Agar app installed nahi hai, toh pehle PlayStore se download karein)_"
    )
    bot.reply_to(message, response_msg, parse_mode="Markdown")

# ----------------- START SERVER & BOT -----------------
def run_bot():
    print("Telegram Bot is running...")
    bot.polling(non_stop=True)

if __name__ == "__main__":
    # Bot ko background me chalao
    threading.Thread(target=run_bot).start()
    
    # Render ke liye Web Server chalao
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
