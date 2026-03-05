import telebot
import os
import threading
from flask import Flask
import yt_dlp
import urllib.parse

# Bot Token
API_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

app = Flask(__name__)

@app.route('/')
def home(): return "WATCHit Bot is Online! 🚀"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "WATCHit Bot Ready! 🍿\nSend any video link (TeraBox, YouTube, Instagram).")

@bot.message_handler(func=lambda message: True)
def handle_link(message):
    url = message.text.strip()
    msg = bot.reply_to(message, "⏳ Extracting... please wait!")

    # 🚀 YT-DLP configuration (Ye TeraBox link ko handle kar sakta hai)
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url')
            
            if video_url:
                safe_url = urllib.parse.quote(video_url, safe='')
                app_link = f"watchitapp://play?url={safe_url}"
                
                response = f"🎬 *Video Extracted!*\n\n👉 <a href=\"{app_link}\"><b>▶️ PLAY IN WATCHit APP</b></a>"
                bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text=response, parse_mode="HTML")
            else:
                bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text="❌ Error: Video extract nahi ho paya.")
    except Exception as e:
        bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text=f"❌ Error: {str(e)}")

if __name__ == "__main__":
    threading.Thread(target=lambda: bot.polling(non_stop=True)).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
